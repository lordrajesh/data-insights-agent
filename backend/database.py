import sqlite3
import pandas as pd
import os
from config import DATABASE_PATH

def load_csv_to_db(file_path: str, table_name: str = "data") -> dict:
    """
    Load a CSV file into SQLite database.
    In production this would be loading into Snowflake/BigQuery.
    """
    # Read CSV
    df = pd.read_csv(file_path)

    # Connect to SQLite and store
    conn = sqlite3.connect(DATABASE_PATH)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    return {
        "status": "success",
        "rows": len(df),
        "columns": list(df.columns),
        "table_name": table_name
    }


def get_schema() -> str:
    """
    Get the database schema — passed to the agent so it knows
    what columns and tables exist before writing SQL.
    In production this would be a metadata catalog query.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    schema = ""
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        col_info = ", ".join([f"{col[1]} ({col[2]})" for col in columns])
        schema += f"Table: {table_name}\nColumns: {col_info}\n\n"

    conn.close()
    return schema


def run_sql(query: str) -> list:
    """
    Execute SQL query and return results.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()

    return {
        "columns": columns,
        "rows": results
    }