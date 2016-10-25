from flask import Flask, jsonify, request
from os import system
import OpenSSL

app = Flask(__name__)

PORT = 443
HOST = '0.0.0.0'

@app.route("/tv", methods=['POST', 'GET'])
def index():
    switch = request.json['request']['intent']['slots']['Switch']['value']
    isOn = True if switch == 'on' else False
    if isOn:
        print(system('irsend SEND_ONCE TV P-On'))
    else:
        print(system('irsend SEND_ONCE TV P-Off'))
    response = {}
    response['version'] = '1.0'
    response['response'] = {
        'outputSpeech': {
            'type': 'PlainText',
            'text': 'Successfully turned {}!'.format(switch)
        },
        'shouldEndSession': True
    }
    return jsonify(response)

@app.route("/tv/on")
def tvOn():
    print(system('irsend SEND_ONCE TV P-On'))
    return jsonify({'success':1, 'message':'TV successfully turned on'})

@app.route("/tv/off")
def tvOff():
    print(system('irsend SEND_ONCE TV P-Off'))
    return jsonify({'success':1, 'message':'TV successfully turned off'})

if __name__ == "__main__":
    context = ('ssl/allcert.crt', 'ssl/cert.key')
    app.run(host=HOST, port=PORT, ssl_context=context)
