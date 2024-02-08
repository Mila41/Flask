from flask import Flask, request, render_template
from datetime import datetime
from os import path
import json
app = Flask(__name__)


MAX_MESSAGES = 50

# Формат файла: {"messages": messages_list}
MESSAGES_FILE = "messages.json"


def load_messages():
    global messages_list
    if not path.isfile(MESSAGES_FILE):
        print(f"Can't find file {MESSAGES_FILE}")
        return []

    with open(MESSAGES_FILE, "r") as mess_file:
        json_data = json.load(mess_file)
        return json_data["messages"]


messages_list = load_messages()
def save_messages():
    global messages_list
    with open(MESSAGES_FILE, "w") as mess_file:
        json_data = {
            "messages": messages_list
        }
        json.dump(json_data, mess_file)

# Функция для добавления новых сообщений (имя отправителя, текст сообщений) в список
def add_message(name, text):
    global messages_list
    new_message = {
        "name": name,
        "text": text,
        "time": datetime.now().strftime("%H:%M"),
    }
    messages_list.append(new_message)
    if len(messages_list) > MAX_MESSAGES:
        messages_list = messages_list[-MAX_MESSAGES:]
    save_messages()


# 1. Display all chat messages: JSON
@app.route("/get_messages")
def get_messages():
    return {"messages": messages_list}

# 2. Ability to sent new messages
# HTTP GET
# http://127.0.0.1/send_message?
@app.route("/send_message")
def send_message():
    name = request.args.get("name")
    text = request.args.get("text")
    # name_len = len(name)
    # if len(name) < 3 or len(name) > 100:
    # if not 100 > name_len > 3:
    #    return {"result": False, "error": "Invalid name"}

    add_message(name, text)
    return "OK"

# 3. UI for messenger
@app.route("/chat")
def display_chat():
    return render_template("chat.html")
app.run()

