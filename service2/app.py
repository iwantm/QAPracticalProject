from flask import Flask, jsonify
from random import choice

countries = {'Argentina': 'spa',
             'Bolivia': 'aym',
             'Brazil': 'por',
             'Chile': 'spa',
             'Colombia': 'spa',
             'Ecuador': 'spa',
             'Paraguay': 'spa',
             'Peru': 'spa',
             'Uruguay': 'spa',
             'Venezuela': 'spa'
             }
app = Flask(__name__)


@app.route('/')
def random_country():
    resp = {
        "country_name": "",
        "country_language": ""
    }
    country = choice(list(countries.keys()))
    country_name = country
    country_langauge = countries[country_name]
    resp["country_name"] = country_name
    resp["country_language"] = country_langauge
    return jsonify(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
