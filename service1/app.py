from flask import Flask, render_template
import requests
from os import getenv, wait
import time
from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@database:3306/name-db'
app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 28700


serv2 = "http://service2:5001"
serv3 = "http://service3:5002"
serv4 = "http://service4:5003"


class Names(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(6), nullable=False)


@app.route('/')
def index():
    country = requests.get(serv2).json()
    gender = requests.get(serv3).json()
    if gender["gender"] == 'f':
        gender_name = 'female'
    elif gender["gender"] == 'm':
        gender_name = 'male'
    try:
        name = requests.post(serv4, json={"country_language": country["country_language"],
                                          "gender": gender["gender"]}).json()
    except:
        name = requests.post(serv4, json={"country_language": country["country_language"],
                                          "gender": gender["gender"]}).json()
    country_name = country["country_name"]
    try:
        new_person = Names(
            first_name=name["first_name"], last_name=name["last_name"], gender=gender_name)
        db.session.add(new_person)
        db.session.commit()
    except (AttributeError, exc.SQLAlchemyError):
        db.session.rollback()
        new_person = Names(
            first_name=name["first_name"], last_name=name["last_name"], gender=gender_name)
        db.session.add(new_person)
        db.session.commit()
    return render_template('index.html', name=name, country=country_name, gender=gender_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
