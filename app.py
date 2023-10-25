import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/flexbe_webhook', methods=['POST'])
def receive_from_flexbe():
    data = request.json
    email = data.get("client", {}).get("email")

    if not email:
        return jsonify({"status": "error", "message": "Email not provided!"})

    send_email_to_sendpulse(email)
    return jsonify({"status": "success"})

SENDPULSE_CLIENT_ID = '9a2ab93315d7bff8084901a2ef513fc2'
SENDPULSE_CLIENT_SECRET = '6bc6636dc1a5ea55299f0923e9024ef8'

def get_access_token():
    AUTH_URL = "https://api.sendpulse.com/oauth/access_token"
    auth_data = {
        "grant_type": "client_credentials",
        "client_id": SENDPULSE_CLIENT_ID,
        "client_secret": SENDPULSE_CLIENT_SECRET
    }
    response = requests.post(AUTH_URL, json=auth_data)
    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("access_token")
    else:
        return None

def send_email_to_sendpulse(email):
    access_token = get_access_token()
    if not access_token:
        return "Error: Failed to get token for sending email."

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    url = "https://api.sendpulse.com/addressbooks/647205/emails"
    data = {
        "emails": [email]
    }
    
    response = requests.post(url, headers=headers, json=data)
    print("Sending email...")
    print("Response status code:", response.status_code)
    print("Response text:", response.text)
    
    if response.json().get("result"):
        return "Email successfully sent!"
    else:
        return "Error when sending email."

if __name__ == '__main__':
    app.run(debug=True, port=5000)
