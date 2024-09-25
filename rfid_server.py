from flask import Flask, request, jsonify
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Setup logging
# File handler (rotating logs)
file_handler = RotatingFileHandler('rfid_server.log', maxBytes=10000, backupCount=3)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Add both handlers to the app's logger
app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)

# In-memory database for authorized cards
authorized_cards = {
    "976665881085": "White Sample Card",
    "594317259082": "Blue Key",
    "38355375961": "Durga Store Card"
}

@app.route('/verify', methods=['POST'])
def verify_card():
    card_id = request.json.get('card_id')
    if not card_id:
        app.logger.error("Card ID is missing in the request")
        return jsonify({"error": "Card ID is required"}), 400

    # Check if the card ID is authorized
    user = authorized_cards.get(card_id)
    if user:
        app.logger.info(f"Card ID {card_id} is authorized for {user}")
        return jsonify({"authorized": True, "user": user}), 200
    else:
        app.logger.warning(f"Card ID {card_id} is not authorized")
        return jsonify({"authorized": False}), 403

@app.route('/door-status', methods=['POST'])
def door_status():
    status = request.json.get('status')
    if not status:
        app.logger.error("Door status is missing in the request")
        return jsonify({"error": "Status is required"}), 400

    # Log the door status
    app.logger.info(f"Door status received: {status}")
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
