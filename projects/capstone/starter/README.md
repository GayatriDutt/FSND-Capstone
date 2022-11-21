## Udacity Full Stack Web Development - Capstone Project
# Project and motivation
The context of this application is a casting agency system that manages actors and movies. I have done this project as part of my Udacity Fullstack web development nanodegree and serves to provide actors and directors with a platform to manage actor details and corresponding movies. The following database tables exist:

Movie
Actor
actor_movies (This is an association table that facilitates the many-to-many relationship between the Actor and Movies tables)

## Tech Stack
# Key technologies used

Python
Flask framework
PostgresSQL
Heroku
Auth0

## Local environment setup
Setup and activate a Python virtual environment. Following steps are using Gitbash CLI
if no python virtul environment previous setup, run this command:

python -m venv myvenv

If there is already a virtual environment created (a folder named myvenv or similiar). Run the following commands to activate the environment:

cd myvenv/Scripts
. activate

Install backend dependencies using PIP (Package Installer for Python). This will install the dependencies within the previously activated virtual environment. Packages will now be installed in myvenv/Lib/site-packages

cd capstone-project

pip install -r requirements.txt

# Run the application locally
export FLASK_APP=app.py
flask run --reload

## API Endpoints

# GET /actors

Sample request
curl http://127.0.0.1:5000/actors

Sample response

{
   "actors":[
      {
         "id":2,
         "name":"bob"
      }
   "success":true
}

# POST /actors
Sample request
curl -X POST http://127.0.0.1:5000/actors
   -H 'Content-Type: application/json'
   -d '{
    "name": "ABC",
    "movies": [1,2]
}'

Sample response
{
    "actor": {
        "id": 3,
        "movies": [
            1,
            2
        ],
        "name": "ABC"
    },
    "success": true
}

# PATCH /actors/{actor_id}
Sample request
curl -X PATCH http://127.0.0.1:5000/actors/1 -H 'Content-Type: application/json'
     -H 'Accept: application/json'
     -d '{"movies": [1]}'
{
    "actor": {
        "id": 1,
        "movies": [
            1
        ],
        "name": "bob"
    },
    "success": true
}

# DELETE /movies/{movie_id}
Sample request
curl -X DELETE http://127.0.0.1:5000/actors/2 -H "Accept: application/json"

Sample response
{

    "success": true
}
# GET /movies
Sample request
curl http://127.0.0.1:5000/movies

Sample response

{
    "movies": [
        {
            "actors": [
                1
            ],
            "id": 12,
            "release_date": "1997",
            "title": "Titanic"
        },
        {
            "actors": [],
            "id": 20,
            "release_date": "1994",
            "title": "Shawshank Redemption"
        }
    ],
    "success": true
}

# RBAC credentials and roles

Auth0 was set up to manage role-based access control for these users:
Director, Actor.

Permissions:
The actor can do the following:: post:actors (allows them to add a new actor), delete:actors (allows them to remove an actor)
The director can do the follwoing:: post:movies (allows them to add movies), patch:actors(allows them to change the details of a particular actor), delete:movies (allows them to delete a movie)

There are 2 endpoints get:actors and get:movies that do not need authorisation.


To deploy on Heroku, the following commands were executed:
- pip install -r requirements.txt
-  chmod +x setup.sh
- source setup.sh
- python manage.py db init, python manage.py db migrate, python manage.py db upgrade
- heroku create capstone10051997 --buildpack heroku/python
- heroku addons:create heroku-postgresql:hobby-dev --app capstone10051997
- heroku config --app capstone10051997
- export DATABASE_URL="postgres://amugtfglhcsuaj:110076319b6270f53d1bccc798dfd0e47f601853637c92eae0032374b1c98c23@ec2-44-205-64-253.compute-1.amazonaws.com:5432/dfvv08sth7v90t"
- git add .
- git status
- git commit -m "someMessage"
- git push heroku master
The application is deployed on Heroku -  https://capstone10051997.herokuapp.com/