from flask import Flask
app = Flask(__name__)

PORT = 80
HOST = '0.0.0.0'

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)