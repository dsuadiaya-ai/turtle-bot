from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "turtle123"
PHONE_NUMBER_ID = "1337632159437159"

@app.route('/')
def home():
    return "Turtle Bot Running!"

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    return "Failed", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data)
    try:
        if data['object'] == 'whatsapp_business_account':
            for entry in data['entry']:
                for change in entry['changes']:
                    if 'messages' in change['value']:
                        msg = change['value']['messages'][0]
                        from_number = msg['from']
                        text = msg.get('text', {}).get('body', '')
                        send_message(from_number, f"🐢 Halo! Kamu kirim: {text}")
    except Exception as e:
        print(e)
    return "OK", 200

def send_message(to, text):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    token = os.environ.get("WA_TOKEN")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp","to": to,"type": "text","text": {"body": text}}
    requests.post(url, headers=headers, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
