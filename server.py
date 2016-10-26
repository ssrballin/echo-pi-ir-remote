from flask import Flask, jsonify, request
from os import system
import OpenSSL
import pprint

app = Flask(__name__)

PORT = 443
HOST = '0.0.0.0'

class TV:
    @staticmethod
    def power(switch):
        switch = switch.lower()
        if switch == 'on':
            print(system('irsend SEND_ONCE TV-Discrete P-On'))
            return True
        elif switch == 'off':
            print(system('irsend SEND_ONCE TV-Discrete P-Off'))
            return True
        return False

    @staticmethod
    def volume(direction, level):
        direction = direction.lower()
        amount = int(level)
        if amount < 1 or amount > 99:
            return False
        if direction in ['up', 'increase', 'raise']:
            for i in range(amount):
                print(system('irsend SEND_ONCE TV KEY_VOLUMEUP'))
            return True
        elif direction in ['down', 'decrease', 'lower']:
            for i in range(amount):
                print(system('irsend SEND_ONCE TV KEY_VOLUMEDOWN'))
            return True
        return False

    @staticmethod
    def input(tvinput):
        tvinput = tvinput.upper()
        if tvinput in ['HDMI 1', 'APPLE TV']:
            print(system('irsend SEND_ONCE TV-Discrete HDMI1'))
            return True
        elif tvinput in ['HDMI 2', 'PLAY STATION 4', 'PLAY STATION', 'PS4']:
            print(system('irsend SEND_ONCE TV-Discrete HDMI2'))
            return True
        elif tvinput in ['HDMI 3', 'CABLE', 'COMCAST']:
            print(system('irsend SEND_ONCE TV-Discrete HDMI3'))
            return True
        return False

class AVR:
    @staticmethod
    def power(switch):
        switch = switch.lower()
        if switch == 'on':
            print(system('irsend SEND_ONCE HK KEY_POWER'))
            return True
        elif switch == 'off':
            print(system('irsend SEND_ONCE HK off'))
            return True
        return False

class XF:
    @staticmethod
    def power(switch):
        switch = switch.lower()
        if switch == 'on':
            print(system('irsend SEND_ONCE XF KEY_POWER'))
            return True
        elif switch == 'off':
            print(system('irsend SEND_ONCE XF KEY_POWER'))
            return True
        return False

@app.route("/theatre", methods=['POST'])
def index():
    intent = request.json['request']['intent']['name']
    isSuccessful = False

    if intent == 'ControlTVPower':
        switch = request.json['request']['intent']['slots']['Switch']['value']
        isSuccessful = TV.power(switch)
    elif intent == 'ControlAVRPower':
        switch = request.json['request']['intent']['slots']['Switch']['value']
        isSuccessful = AVR.power(switch)
    elif intent == 'ControlXFPower':
        isSuccessful = XF.power('on')
    elif intent == 'ControlALLPower':
        switch = request.json['request']['intent']['slots']['Switch']['value']
        isSuccessful = TV.power(switch) and AVR.power(switch)
    elif intent == 'ControlTVVolume':
        direction = request.json['request']['intent']['slots']['Direction']['value']
        level = request.json['request']['intent']['slots']['Level']['value']
        isSuccessful = TV.volume(direction, level)
    elif intent == 'ControlTVInput':
        tvinput = request.json['request']['intent']['slots']['Input']['value']
        isSuccessful = TV.input(tvinput)


    response = {}
    response['version'] = '1.0'
    response['response'] = {
        'outputSpeech': {
            'type': 'PlainText',
            'text': 'Done!' if isSuccessful else 'Unable to complete request.'
        },
        'shouldEndSession': True
    }
    return jsonify(response)



if __name__ == "__main__":
    context = ('ssl/allcert.crt', 'ssl/cert.key')
    app.run(host=HOST, port=PORT, ssl_context=context)
