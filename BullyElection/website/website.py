import flask
from flask import Flask, render_template, request, jsonify
import random
import json
from threading import Thread

app = Flask(__name__)

# A list of sample fortune cookies
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
    print("Trying to run app")
    app.run(debug=False, host='0.0.0.0', port=4444)
    print("app running")

