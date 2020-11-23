from flask import Flask, render_template
import requests
app = Flask(__name__)

serv2 = "http://localhost:5001"
serv3 = "http://localhost:5002"
serv4 = "http://localhost:5003"


@app.route('/')
def index():
    country = requests.get(serv2).json()
    gender = requests.get(serv3).json()
    name = requests.post(serv4, json={"country_language": country["country_language"],
                                      "gender": gender["gender"]}).json()
    country_name = country["country_name"]
    if gender["gender"] == 'f':
        gender_name = 'female'
    else:
        gender_name = 'male'
    return render_template('index.html', name=name, country=country_name, gender=gender_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
