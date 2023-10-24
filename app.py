import json
import os
import stripe 
# import psycopg2  # assuming you're using PostgreSQL
# from dotenv import load_dotenv
from flask import Flask, jsonify, request, abort
import logging
# from database import handle_checkout_session_completed, handle_invoice_payment_succeeded
from datetime import datetime
# В файле app.py
# import database


# logging.basicConfig(level=logging.DEBUG)
# Load environment variables from the .env file
# load_dotenv()
# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
stripe.api_key = os.getenv('STRIPE_API_KEY')
# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = os.getenv('ENDPOINT_SECRET')

app = Flask(__name__)

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({"error": "Bad Request", "message": str(error)}), 400 

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        print("Invalid payload")
        abort(400)
    except stripe.error.SignatureVerificationError as e:
        print("Invalid signature")
        abort(400)

    # Handle the event - подключено эвентов из страйпа
    # event_type = event['type']
    # if event_type == 'checkout.session.completed':
    #     handle_checkout_session_completed(event, app)
    # elif event_type == 'invoice.payment_succeeded':
    #     handle_invoice_payment_succeeded(event, app)

    return '', 200


@app.route('/')
def home():
    return 'Hello, World!'


# # ПОТОМ ВЫКЛЮЧИТЬ debug=True НУЖНО
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=False)