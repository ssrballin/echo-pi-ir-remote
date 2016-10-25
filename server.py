from flask import Flask, jsonify, request
from os import system
import OpenSSL
import pprint

app = Flask(__name__)

PORT = 443
HOST = '0.0.0.0'

@app.route("/theatre", methods=['POST'])
def index():
    pprint.pprint(request.json)
    intent = request.json['request']['intent']['name']
    switch = request.json['request']['intent']['slots']['Switch']['value']
    isOn = True if switch == 'on' else False
    if isOn:
        if intent == 'ControlTV':
            print(system('irsend SEND_ONCE TV P-On'))
        elif intent == 'ControlAVR':
            print(system('irsend SEND_ONCE HK KEY_POWER'))
        elif intent == 'ControlXF':
            print(system('irsend SEND_ONCE XF KEY_POWER'))
        elif intent == 'ControlALL':
            print(system('irsend SEND_ONCE TV P-On'))
            print(system('irsend SEND_ONCE HK KEY_POWER'))
            print(system('irsend SEND_ONCE XF KEY_POWER'))
    else:
        if intent == 'ControlTV':
            print(system('irsend SEND_ONCE TV P-Off'))
        elif intent == 'ControlAVR':
            print(system('irsend SEND_ONCE HK off'))
        elif intent == 'ControlXF':
            print(system('irsend SEND_ONCE XF KEY_POWER'))
        elif intent == 'ControlALL':
            print(system('irsend SEND_ONCE TV P-Off'))
            print(system('irsend SEND_ONCE HK off'))
            print(system('irsend SEND_ONCE XF KEY_POWER'))
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



if __name__ == "__main__":
    context = ('ssl/allcert.crt', 'ssl/cert.key')
    app.run(host=HOST, port=PORT, ssl_context=context)
