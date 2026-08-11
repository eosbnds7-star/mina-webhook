import os
import requests
from flask import Flask, request
from openai import OpenAI
app = Flask(__name__)
VERIFY_TOKEN = "mina_webhook_2026"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
INSTAGRAM_ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
client = OpenAI(api_key=OPENAI_API_KEY)
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
    print("GELEN VERİ:", data)
    try:
        for item in data.get("entry", []):
            for message_event in item.get("messaging", []):
                sender_id = message_event.get("sender", {}).get("id")
                message = message_event.get("message", {})
                text = message.get("text")
                if not sender_id or not text:
                    continue
                print("GELEN MESAJ:", text)
                response = client.responses.create(
                    model="gpt-5-mini",
                    instructions=(
                        "Sen Mina'sın. Instagram'da doğal, samimi ve "
                        "arkadaş canlısı konuşan bir AI karakterisin. "
                        "Kısa, doğal ve sohbet havasında cevap ver."
                    ),
                    input=text
                )
                reply = response.output_text
                print("MINA CEVABI:", reply)
                url = "https://graph.facebook.com/v23.0/me/messages"
                payload = {
                    "recipient": {"id": sender_id},
                    "message": {"text": reply},
                    "access_token": INSTAGRAM_ACCESS_TOKEN
                }
                result = requests.post(url, json=payload)
                print("INSTAGRAM CEVAP SONUCU:", result.status_code)
                print(result.text)
    except Exception as e:
        print("HATA:", str(e))
    return "EVENT_RECEIVED", 200
@app.route("/")
def home():
    return "Mina AI webhook is running!"
@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Code bulunamadı", 400
    return "Instagram bağlantısı başarılı! Artık bu pencereyi kapatabilirsiniz.", 200
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
