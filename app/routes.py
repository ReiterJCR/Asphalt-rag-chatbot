from flask import jsonify, Blueprint, render_template, request, redirect, url_for
from .gpt import ask_gpt


main = Blueprint("main", __name__)
info  = Blueprint("info", __name__)
chat_history = []

@main.route("/", methods=["GET"])
def index_get():
    return render_template("index.html", messages=chat_history)


@main.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question")
    bot_response = ask_gpt(user_question)
    return jsonify({"response": bot_response})


