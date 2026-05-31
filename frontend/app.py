import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Data Insights Agent", page_icon="📊")
st.title("📊 Data Insights Agent")
st.caption("Upload a CSV and ask questions in plain English")

# --- Section 1: Upload CSV ---
st.header("1. Upload your CSV")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    if st.button("Load into Database"):
        with st.spinner("Loading CSV into database..."):
            response = requests.post(
                f"{BACKEND_URL}/upload",
                files={"file": (uploaded_file.name, uploaded_file, "text/csv")}
            )
            result = response.json()

        if result.get("status") == "success":
            st.success(f"✅ Loaded {result['rows']} rows with columns: {', '.join(result['columns'])}")
        else:
            st.error("Something went wrong")

# --- Section 2: Ask Questions ---
st.header("2. Ask a Question")

# Example questions to guide the user
st.caption("Examples: 'What is the total revenue by category?' / 'Which region had the most units sold?' / 'Top 3 products by revenue?'")

question = st.text_input("Ask anything about your data:")

if st.button("Ask") and question:
    with st.spinner("Agent is thinking..."):
        response = requests.post(
            f"{BACKEND_URL}/ask",
            json={"question": question}
        )
        result = response.json()

    if result.get("error"):
        st.error(result.get("answer"))
    else:
        # Answer
        st.subheader("Answer")
        st.write(result.get("answer"))

        # Chart
        if result.get("chart_path"):
            st.subheader("Chart")
            chart_response = requests.get(f"{BACKEND_URL}/charts/latest_chart.png")
            st.image(chart_response.content)

        # SQL + Raw Results
        with st.expander("View generated SQL and raw results"):
            st.code(result.get("sql_query"), language="sql")
            if result.get("rows"):
                st.write(f"**Columns:** {result.get('columns')}")
                for row in result.get("rows", []):
                    st.write(row)