import sqlite3

DB_PATH = "pit_stops.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pit_stops (
                PitStopID INTEGER PRIMARY KEY,
                SeriesName TEXT,
                EventName TEXT,
                TrackName TEXT,
                EventDate TEXT,
                TeamName TEXT,
                StopNumber INTEGER,
                LapNumber INTEGER,
                SeasonName TEXT,
                PitStopTime REAL,
                CarStopToJack REAL,
                RSTime REAL,
                JackTime REAL,
                LSTime REAL,
                JackToCarGoes REAL,
                Other TEXT,
                Other_Sub_Category TEXT,
                PitStopType TEXT
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        conn.commit()
        

