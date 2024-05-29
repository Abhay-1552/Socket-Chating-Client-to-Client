from flask import Flask, render_template, request
from client import CLIENT

app = Flask(__name__, template_folder='template')

client = CLIENT()


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/message", methods=["POST"])
def message():
    if request.method == "POST":
        chat = request.form.get("messageInput")
        client.send_messages(chat)
        return '', 204


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
