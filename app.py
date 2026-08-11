from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "mina_webhook_2026"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200

        return "Forbidden", 403

    data = request.get_json()
    print(data)

    return "EVENT_RECEIVED", 200

@app.route("/")
def home():
    return "Mina webhook is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
