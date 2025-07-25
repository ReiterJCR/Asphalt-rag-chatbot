import csv
import os
from .db import get_connection, init_db
import time
CSV_PATH = os.path.join(os.path.dirname(__file__), "../data/pit_stops.csv")

def safe_float(val):
    try:
        return float(val)
    except:
        return None

def safe_int(val):
    try:
        return int(val)
    except:
        return None

def load_csv_to_db():
    """Load data from CSV file into SQLite database."""
    init_db()
    
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("REPLACE INTO metadata (key, value) VALUES (?, ?)", ("last_updated", str(int(time.time()))))
        cursor.execute("DELETE FROM pit_stops")
        print(f"Inserting {len(rows)} rows...")
        print("Sample row:", rows[0])

        for row in rows:
            cursor.execute("""
                INSERT INTO pit_stops (
                    PitStopID, SeriesName, EventName, TrackName, EventDate,
                    TeamName, StopNumber, LapNumber, SeasonName, PitStopTime,
                    CarStopToJack, RSTime, JackTime, LSTime, JackToCarGoes,
                    Other, Other_Sub_Category, PitStopType
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                safe_int(row.get("PitStopID")),
                row.get("SeriesName"),
                row.get("EventName"),
                row.get("TrackName"),
                row.get("EventDate"),
                row.get("TeamName"),
                safe_int(row.get("StopNumber")),
                safe_int(row.get("LapNumber")),
                row.get("SeasonName"),
                safe_float(row.get("PitStopTime")),
                safe_float(row.get("CarStopToJack")),
                safe_float(row.get("RSTime")),
                safe_float(row.get("JackTime")),
                safe_float(row.get("LSTime")),
                safe_float(row.get("JackToCarGoes")),
                row.get("Other"),
                row.get("Other_Sub_Category"),
                row.get("PitStopType")
            ))

        conn.commit()
        print(f"Loaded {len(rows)} rows into pit_stops.db.")
        if not rows:
            print("⚠️No rows found in CSV. Check the file path or format.")

if __name__ == "__main__":
    load_csv_to_db()
