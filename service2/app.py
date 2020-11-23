from flask import Flask, jsonify
from random import choice

countries = {'Russia': 'rus',
             'Germany': 'ger',
             'England': 'eng',
             'Wales': 'wel',
             'France': 'fre',
             'Italy': 'ita',
             'Spain': 'spa',
             'Ukraine': 'rus',
             'Poland': 'pol',
             'Romania': 'rmn',
             'Netherlands': 'dut',
             'Belgium': 'fle',
             'Czech Republic': 'cze',
             'Greece': 'gre',
             'Portugal': 'por',
             'Sweden': 'swe',
             'Hungary': 'hun',
             'Belarus': 'bel',
             'Austria': 'ger',
             'Serbia': 'ser',
             'Switzerland': 'ger',
             'Bulgaria': 'bul',
             'Denmark': 'dan',
             'Finland': 'fin',
             'Slovakia': 'slk',
             'Norway': 'nor',
             'Ireland': 'iri',
             'Croatia': 'cro',
             'Moldova': 'rmn',
             'Bosnia and Herzegovina': 'bos',
             'Albania': 'alb',
             'Lithuania': 'lth',
             'North Macedonia': 'mac',
             'Slovenia': 'sln',
             'Latvia': 'lat',
             'Estonia': 'est',
             'Malta': 'mal',
             'Iceland': 'ice',
             'Andorra': 'cat'
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
