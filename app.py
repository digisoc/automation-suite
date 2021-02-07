from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot: Active'

def run():
    app.run(host='0.0.0.0')

def start_server():
    t = Thread(target=run)
    t.start()
