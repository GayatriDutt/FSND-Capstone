import datetime
import json
import os
import unittest
from flask import (abort,jsonify,request)
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie

DIRECTOR_TOKEN = os.environ.get('DIRECTOR_TOKEN')
ASSISTANT_TOKEN = os.environ.get('ASSISTANT_TOKEN')
PRODUCER_TOKEN = os.environ.get('PRODUCER_TOKEN')
INVALID_TOKEN = os.environ.get('INVALID_TOKEN')

def generate_auth_header(token):
    return {
        'Authorization': 'Bearer ' + token
    }
class UnitTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get('DATABASE_URL')
        setup_db(self.app)
        
        self.test_actor = {
            "name": "ABC",
        }
        self.test_actor_bad = {
            "name": "XYZ",
            "movies": [1,3,5]
        }
        self.test_movie = {
            "title": "La la land",
            "release_date": "2018",
        }
        
        self.test_movie_bad = {
            "name": "Blah blah",
        }
        self.actor_update = {   
            "movies": [1]
        }
        self.movie_update = {
            "title": "Titanic 2",
            "actors": [1]
        }
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        
    def tearDown(self):
        pass
       
    def test_add_actor(self):
        res = self.client().post("/actors", headers=generate_auth_header(DIRECTOR_TOKEN), json=self.test_actor)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["actor"]["name"], "ABC")

    def test_add_actor_error(self):
        res = self.client().post("/actors", headers=generate_auth_header(DIRECTOR_TOKEN), json=self.test_actor_bad)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_add_movie(self):
        res = self.client().post("/movies", headers=generate_auth_header(PRODUCER_TOKEN), json=self.test_movie)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data["movie"]["title"], "Titanic")
    
    def test_add_movie_error(self):
        res = self.client().post("/movies", headers=generate_auth_header(PRODUCER_TOKEN), json=self.test_movie_bad)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
    
    def test_update_actor(self):
        self.client().post("/actors", headers=generate_auth_header(DIRECTOR_TOKEN), json=self.test_actor)
        self.client().post("/movies", headers=generate_auth_header(PRODUCER_TOKEN), json=self.test_movie)
        res = self.client().patch("/actors/1", headers=generate_auth_header(DIRECTOR_TOKEN), json=self.actor_update)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data["actor"]["movies"], [1])
        
if __name__ == "__main__":
    unittest.main()