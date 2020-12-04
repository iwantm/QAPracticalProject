from flask import Flask, jsonify
from random import choice

app = Flask(__name__)


@app.route('/')
def random_gender():
    resp = {"gender": ""}
    gender = choice('mfff')
    resp["gender"] = gender
    return jsonify(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
