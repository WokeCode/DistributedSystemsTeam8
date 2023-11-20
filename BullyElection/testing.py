from flask import Flask, render_template, request, jsonify
import random
import json
import threading
from werkzeug.serving import run_simple

app = Flask(__name__)

fortune_cookies = json.load(open('website/fortunes.json'))
fortune_cookies = fortune_cookies['fortunes']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_fortune', methods=['POST'])
def get_fortune():
    fortune = random.choice(fortune_cookies)
    return jsonify({'fortune': fortune})

def run_flask_app():
    run_simple('0.0.0.0', 5000, app, use_reloader=False, use_debugger=True)

def main_logic():
    while True:
        # Your main logic here
        print("Running main logic")
        time.sleep(5)

if __name__ == "__main__":
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    # Run your main logic in the main thread
    main_logic()
