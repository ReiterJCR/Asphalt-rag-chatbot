# Asphalt Analytics – RAG Chatbot

This is a Retrieval-Augmented Generation (RAG) chatbot that allows users to ask natural language questions about motorsports pit stop data. The chatbot uses OpenAI’s GPT API to dynamically generate SQL queries, retrieve relevant records from a local SQLite database, and respond with intelligent answers using only the retrieved data.

---

## Features

- **RAG workflow**: Combines GPT reasoning with real-time structured data retrieval.
- **Live chat interface**: Built with Flask and vanilla JS for simplicity and speed.
- **Auto-ingestion**: Load pit stop data from a CSV file into SQLite with one click.
- **Prompt engineering**: Clean, instructive prompts to guide GPT through structured querying and answer generation.

---

## Tech Stack

- Python 3.9+
- Flask
- SQLite3
- OpenAI API
- HTML/CSS/JS (vanilla)

---

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/asphalt-rag.git
cd asphalt-rag
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
### 3. Create asphalt-rag/data and drop your .csv in 

### 4.  Run the app!

```bash
python run.py
```

### Make sure to refresh the database if it is your first time running the app or if you have new data!



<img width="914" height="743" alt="image" src="https://github.com/user-attachments/assets/fe9b8f19-5f3d-4929-a080-5aeee9e12e1a" />

