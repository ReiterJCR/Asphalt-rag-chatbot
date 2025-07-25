import os
import openai
import sqlite3
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

DB_PATH = "pit_stops.db"

def ask_gpt_for_sql(user_question, context_window=None):
    """Generate a SQL query based on the user's question and context window.
    Args:
        user_question (str): The user's question to generate a SQL query for.
        context_window (list, optional): Previous messages to provide context. Defaults to None.
    """
    context_window = context_window or []

    instructions = f"""
    You are a helpful assistant that generates SQL queries to retrieve motorsports pit stop data.

    You must only use the following table: `pit_stops`.

    Here are the column names(types):
    | Column               | Type
    | -------------------- | ------- 
    | `PitStopID`          | INTEGER 
    | `SeriesName`         | TEXT    
    | `EventName`          | TEXT    
    | `TrackName`          | TEXT    
    | `EventDate`          | TEXT   
    | `TeamName`           | TEXT (NUMBER ONLY)
    | `StopNumber`         | INTEGER
    | `LapNumber`          | INTEGER 
    | `SeasonName`         | TEXT   
    | `PitStopTime`        | REAL 
    | `CarStopToJack`      | REAL  
    | `RSTime`             | REAL   
    | `JackTime`           | REAL  
    | `LSTime`             | REAL 
    | `JackToCarGoes`      | REAL   
    | `Other`              | INTEGER
    | `Other_Sub_Category` | TEXT   
    | `PitStopType`        | TEXT

    If the question is about specific years, teams, tracks, etc, ALWAYS select those columns.

    Generate a SQL query (for SQLite) to answer the user's question, assuming they want all relevant data from the pit_stops table:
    No row with relevant data that is Null or empty should be included in the answer.
    
    Chat history is provided to help you understand the context of the question
    Chat History:
    )
    {context_window if context_window else "No previous messages."}    
    Return ONLY the SQL query, nothing else. If the message is not a data retrieval question, respond with "no query needed".

    """
    prompt = f"""
    User question: "{user_question}"

    """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "developer", "content": instructions}, {"role": "user", "content": prompt}],
        temperature=0.1
    )

    return response.choices[0].message.content.strip()

def generate_answer_from_data(user_question, data_query, data_text, context_window=None):
    """Generate a natural language answer based on the SQL query results and user question.
    Args:
        user_question (str): The user's question to answer.
        data_query (str): The SQL query that was run to retrieve the data.
        data_text (str): The text representation of the data retrieved by the SQL query.
        context_window (list, optional): Previous messages to provide context. Defaults to None.
    """
    context_window = context_window or []

    instructions = f"""
    You are a motorsports data analyst.

    Answer the user's question using only the provided pit stop data.
    Use a helpful and professional tone, and refer to past questions and answers when helpful.

    ---

    Chat History:
    {context_window}
    ---
    If the user message is not a data retrieval question, respond intelligently.
    If for some reason you cannot answer the question, explain why.
    Data(If data is not available, respond with "No data available."):
    {data_text}
    
    Obtained via SQL query:
    {data_query}
    ---
    """
    question = f"""
    Based on the data: {user_question}

    """
    response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "developer", "content": instructions},{"role": "user", "content": question}],
            temperature=0.2,
    )

    return response.choices[0].message.content.strip()


def run_sql_query(query):
    """Run a SQL query against the SQLite database and return the results."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
    except Exception as e:
        return f"⚠️ Error running query: {e}"

    if not rows:
        return "No results found."
    formatted = [", ".join(columns)]
    for row in rows[:10]: 
        formatted.append(", ".join(str(cell) if cell is not None else "-" for cell in row))
    
    return "\n".join(formatted)
