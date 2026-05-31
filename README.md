# Data Insights Agent 📊

A production-inspired AI agent that lets you upload a CSV and ask questions in plain English — getting back SQL, charts, and explanations automatically.

## How It Works

    User asks question in plain English
           ↓
    Agent gets database schema
           ↓
    LLM writes SQL query
           ↓
    SQL runs on SQLite
           ↓
    LLM writes matplotlib chart code
           ↓
    Code executes → chart saved
           ↓
    LLM explains the results
           ↓
    Answer + Chart + SQL shown to user

## Key Concept — AI Agents

Unlike a fixed pipeline, the agent **decides what to do** at runtime:
- What SQL to write based on the question
- Whether a chart makes sense
- What chart type fits the data best
- How to explain the results

This is the same pattern used by ChatGPT Code Interpreter and Microsoft Copilot for Power BI.

## Tech Stack

| Component | Free (This Project) | Production Equivalent |
|---|---|---|
| Database | SQLite | Snowflake / BigQuery / Redshift |
| LLM | Groq llama-3.3-70b-versatile | Azure OpenAI GPT-4 / AWS Bedrock |
| Agent | Custom LLM pipeline | LangGraph / Azure AI Agents |
| Charts | LLM-generated matplotlib | Power BI / Tableau Embedded |
| UI | Streamlit | React + Enterprise Portal |
| Backend | FastAPI | AWS Lambda / Azure Functions |
| File Storage | Local | AWS S3 / Azure Data Lake |

## Project Structure

    data-insights-agent/
    ├── backend/
    │   ├── main.py          # FastAPI app + endpoints
    │   ├── agent.py         # LLM agent - SQL + chart + explanation
    │   ├── database.py      # CSV loading + SQLite queries
    │   └── config.py        # Settings and environment variables
    ├── frontend/
    │   └── app.py           # Streamlit UI
    ├── data/                # Uploaded CSVs (gitignored)
    └── requirements.txt

## Run Locally

### Prerequisites
- Python 3.10+
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Setup
```bash
git clone https://github.com/YOUR_USERNAME/data-insights-agent.git
cd data-insights-agent
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

### Configure

GROQ_API_KEY=your_groq_api_key_here

### Start
```bash
# Terminal 1
cd backend && uvicorn main:app --reload

# Terminal 2
cd frontend && streamlit run app.py
```

## Key Concepts Demonstrated
- **AI Agents** — LLM plans and executes multi-step tasks
- **Code generation + execution** — LLM writes matplotlib code, we execute it
- **Text to SQL** — natural language converted to database queries
- **Production mapping** — every component maps to enterprise equivalent
