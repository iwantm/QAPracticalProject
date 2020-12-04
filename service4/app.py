from flask import Flask, jsonify, request
import requests
from os import getenv
app = Flask(__name__)


@app.route('/', methods=["POST"])
def random_name():
    resp = {"first_name": "",
            "last_name": ""}
    code = getenv('API_CODE')
    country = request.get_json()['country_language']
    gender = request.get_json()['gender']
    if gender == 'm':
        country = 'grem'
    response = requests.get("https://www.behindthename.com/api/random.json?usage=" +
                            country + "&gender=" + gender + "&key=" + code + "&number=1&randomsurname=yes")

    first_name = response.json()["names"][0]
    last_name = response.json()["names"][-1]
    resp["first_name"] = first_name
    resp["last_name"] = last_name
    return jsonify(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
