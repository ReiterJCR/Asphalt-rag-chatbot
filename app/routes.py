from flask import Blueprint, render_template, request, jsonify
from .rag import ask_gpt_for_sql, run_sql_query, generate_answer_from_data

main = Blueprint("main", __name__)
chat_history = []

@main.route("/", methods=["GET"])
def index_get():
    return render_template("index.html", messages=chat_history)

@main.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question")
    chat_history.append({"role": "user", "text": user_question})

    sql = ask_gpt_for_sql(user_question, chat_history[-10:])
    print(sql)
    if sql != "no query needed":
        data = run_sql_query(sql)
        print(data)
    else:
        data = "No results found."
    
    if data == "No results found.":
        response = data
    else:
        response = generate_answer_from_data(user_question, sql, data, chat_history[-10:])

    chat_history.append({"role": "asphaltai", "text": response})
    return jsonify({"response": response})

@main.route("/refresh", methods=["POST"])
def refresh_dataset():
    try:
        from .load_data import load_csv_to_db
        load_csv_to_db()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@main.route("/last_updated", methods=["GET"])
def last_updated():
    from .db import get_connection
    import datetime

    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT value FROM metadata WHERE key = 'last_updated'")
            row = cur.fetchone()
        except Exception as e:
            return jsonify({"error": str(e)})

    if row:
        timestamp = datetime.datetime.fromtimestamp(int(row[0]))
        return jsonify({"last_updated": timestamp.strftime("%Y-%m-%d %H:%M:%S")})
    else:
        return jsonify({"last_updated": "Never"})

@main.route("/clear", methods=["POST"])
def clear_chat():
    global chat_history
    chat_history = []
    return jsonify({"success": True})

