import os
import openai
import sqlite3
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

DB_PATH = "pit_stops.db"

def ask_gpt_for_sql(user_question):
    prompt = f"""
You are a helpful assistant that generates SQL queries to retrieve motorsports pit stop data.

You must only use the following table: `pit_stops`.

Here are the column names:
PitStopID, SeriesName, EventName, TrackName, EventDate, TeamName,
StopNumber, LapNumber, SeasonName, PitStopTime, CarStopToJack,
RSTime, JackTime, LSTime, JackToCarGoes, Other, Other_Sub_Category, PitStopType

Generate a SQL query (for SQLite) to answer the user's question:

User question: "{user_question}"

Return ONLY the SQL query, nothing else.
"""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()


def run_sql_query(query):
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

    # Return a formatted string with the first 10 rows
    formatted = [", ".join(columns)]
    for row in rows[:10]: 
        formatted.append(", ".join(str(cell) if cell is not None else "-" for cell in row))
    
    return "\n".join(formatted)
