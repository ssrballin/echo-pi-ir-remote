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
    if intent == 'ControlTVPower':
        switch = request.json['request']['intent']['slots']['Switch']['value']
        code = 'P-On' if switch == 'on' else 'P-Off'
        print(system('irsend SEND_ONCE TV-Discrete {}'.format(code)))
    elif intent == 'ControlAVRPower':
        switch = request.json['request']['intent']['slots']['Switch']['value']
        code = 'KEY_POWER' if switch == 'on' else 'off'
        print(system('irsend SEND_ONCE HK {}'.format(code)))
    elif intent == 'ControlXFPower':
        print(system('irsend SEND_ONCE XF KEY_POWER'))
    elif intent == 'ControlALLPower':
        switch = request.json['request']['intent']['slots']['Switch']['value']
        code = 'P-On' if switch == 'on' else 'P-Off'
        print(system('irsend SEND_ONCE TV-Discrete {}'.format(code)))
        code = 'KEY_POWER' if switch == 'on' else 'off'
        print(system('irsend SEND_ONCE HK {}'.format(code)))


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
