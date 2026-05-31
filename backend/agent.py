import os
import json
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for server
import matplotlib.pyplot as plt
from groq import Groq
from database import get_schema, run_sql
from config import GROQ_API_KEY, GROQ_MODEL, CHARTS_PATH

os.makedirs(CHARTS_PATH, exist_ok=True)

client = Groq(api_key=GROQ_API_KEY)

def generate_chart(columns: list, rows: list, question: str) -> str:
    """
    Ask LLM to write matplotlib code based on actual results.
    Then execute it to generate the chart.
    """
    chart_prompt = f"""Write Python matplotlib code to visualize this data:

Question: {question}
Columns: {columns}
Rows: {rows}

Rules:
- Use only matplotlib, no other libraries
- Data is already in the variables: columns={columns}, rows={rows}
- Save the chart to: {CHARTS_PATH}/latest_chart.png
- Use plt.tight_layout() before saving
- Return ONLY the Python code, no explanation, no backticks"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": chart_prompt}],
        max_tokens=500,
    )

    chart_code = response.choices[0].message.content.strip()
    print(f"Generated chart code:\n{chart_code}")

    try:
        exec(chart_code, {"matplotlib": matplotlib, "plt": plt,
                          "columns": columns, "rows": rows})
        return f"{CHARTS_PATH}/latest_chart.png"
    except Exception as e:
        print(f"Chart generation failed: {e}")
        return None


def run_agent(question: str) -> dict:
    """
    The agent flow:
    1. Get database schema
    2. Ask LLM to write SQL for the question
    3. Run the SQL
    4. Ask LLM to explain the results
    5. Generate chart if applicable
    """

    # Step 1: Get schema so LLM knows what tables/columns exist
    schema = get_schema()

    # Step 2: Ask LLM to write SQL
    sql_prompt = f"""You are a SQL expert. Given this database schema:

{schema}

Write a SQL query to answer this question: {question}

Rules:
- Return ONLY the SQL query, nothing else
- No markdown, no backticks, no explanation
- Use only tables and columns that exist in the schema"""

    sql_response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": sql_prompt}],
        max_tokens=500,
    )

    sql_query = sql_response.choices[0].message.content.strip()
    print(f"Generated SQL: {sql_query}")

    # Step 3: Run the SQL
    try:
        query_result = run_sql(sql_query)
        columns = query_result["columns"]
        rows = query_result["rows"]
        sql_error = None
    except Exception as e:
        return {
            "answer": f"SQL Error: {e}",
            "sql_query": sql_query,
            "chart_path": None,
            "error": True
        }

    # Step 4: Ask LLM to explain results
    explain_prompt = f"""Given this question: {question}

The SQL query returned these results:
Columns: {columns}
Rows: {rows}

Give a clear, concise explanation of what these results mean.
Focus on insights, not just restating the numbers."""

    explain_response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": explain_prompt}],
        max_tokens=500,
    )

    explanation = explain_response.choices[0].message.content.strip()

    # Step 5: Generate chart if results have 2+ columns
    chart_path = None
    if len(columns) >= 2 and len(rows) > 0:
        chart_path = generate_chart(columns, rows, question)

    return {
        "answer": explanation,
        "sql_query": sql_query,
        "columns": columns,
        "rows": rows,
        "chart_path": chart_path,
        "error": False
    }