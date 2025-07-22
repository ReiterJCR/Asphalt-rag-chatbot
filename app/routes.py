from flask import Blueprint, render_template, request, jsonify
from .rag import ask_gpt_for_sql, run_sql_query

main = Blueprint("main", __name__)
chat_history = []

@main.route("/", methods=["GET"])
def index_get():
    return render_template("index.html", messages=chat_history)

@main.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question")
    chat_history.append({"role": "user", "text": user_question})

    sql = ask_gpt_for_sql(user_question)
    result = run_sql_query(sql)

    chat_history.append({"role": "bot", "text": result})
    return jsonify({"response": result})

