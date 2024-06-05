# index.py
from flask import Flask, render_template, jsonify, request
import threading
import asyncio
from client import CLIENT

app = Flask(__name__, template_folder='template')
data = []
client = CLIENT()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def get_data():
    return jsonify(data)


@app.route('/message', methods=["POST"])
def message():
    if request.method == "POST":
        chat = request.form.get("messageInput")
        client.send_messages(chat)
        return '', 204


def run_flask():
    app.run(debug=True, use_reloader=False)


async def handle_client():
    while True:
        chat = await client.receive_messages()
        if chat:
            data.append(chat)

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    loop = asyncio.get_event_loop()
    loop.create_task(handle_client())
    loop.run_forever()
