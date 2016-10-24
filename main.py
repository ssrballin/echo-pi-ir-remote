from flask import Flask, jsonify
from os import system

app = Flask(__name__)

PORT = 80
HOST = '0.0.0.0'

@app.route("/")
def index():
    return jsonify({'success':1, 'message':'Successfully reached API!'})

@app.route("/tv/on")
def tvOn():
    print(system('irsend SEND_ONCE TV P-On'))
    return jsonify({'success':1, 'message':'TV successfully turned on'})

@app.route("/tv/off")
def tvOff():
    print(system('irsend SEND_ONCE TV P-Off'))
    return jsonify({'success':1, 'message':'TV successfully turned off'})

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, ssl_context='adhoc')
