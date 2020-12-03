from service1.app import app
from flask_testing import TestCase

from unittest.mock import patch

from flask import url_for
import requests_mock

serv2 = "http://service2:5001"
serv3 = "http://service3:5002"


class TestBase(TestCase):
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI="sqlite:///data.db",
            TESTING=True)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestService1(TestBase):
    def test_frontend_male(self):
        with requests_mock.mock() as g:
            with patch("requests.post") as n:
                g.get(serv2, json={
                    "country_name": "Wales",
                    "country_language": "wel"
                })
                g.get(serv3, json={"gender": "m"})
                n.return_value.json.return_value = {"first_name": "Iwan",
                                                    "last_name": "Moreton"}
                response = self.client.get(url_for('index'))
                people = Names.query.all()
                person = Names.query.filter_by(first_name='Iwan').first()
                print(response.data)
                self.assertIn(person, people)
                self.assert200
                self.assertIn(b'Iwan', response.data)
                self.assertIn(b'Moreton', response.data)
                self.assertIn(b'male', response.data)
                self.assertIn(b'Wales', response.data)

    def test_frontend_female(self):
        with requests_mock.mock() as g:
            with patch("requests.post") as n:
                g.get(serv2, json={
                    "country_name": "Wales",
                    "country_language": "wel"
                })
                g.get(serv3, json={"gender": "f"})
                n.return_value.json.return_value = {"first_name": "Iwan",
                                                    "last_name": "Moreton"}
                response = self.client.get(url_for('index'))
                print(response.data)
                self.assert200
                self.assertIn(b'Iwan', response.data)
                self.assertIn(b'Moreton', response.data)
                self.assertIn(b'female', response.data)
                self.assertIn(b'Wales', response.data)
