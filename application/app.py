from flask import Flask, render_template
from os import getenv
from random import randint, choice
import json
import requests
import logging

app = Flask(__name__)


def random_eu_country():
    response = requests.get("https://restcountries.eu/rest/v2/region/europe")
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
    country = choice(list(countries.keys()))
    country_name = country
    country_langauge = countries[country_name]
    return(country_name, country_langauge)


def random_gender():
    gen = choice('mf')
    return gen


def random_name(gender, country):
    country = country
    gender = gender
    code = 'iw455756477'
    response = requests.get("https://www.behindthename.com/api/random.json?usage=" +
                            country[1] + "&gender=" + gender + "&key=iw455756477&number=1&randomsurname=yes")
    app.logger.info(response.status_code)
    return (response)


@ app.route('/')
def index():
    gen = random_gender()
    country_details = random_eu_country()
    person = random_name(gen, country_details).json()['names']
    return(person[0] + ' ' + person[1]+' is from ' + country_details[0] + ', they speak ' + country_details[1] + ', they are ' + gen)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
