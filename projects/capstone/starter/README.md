## Udacity Full Stack Web Development - Capstone Project
# Project
The context of this application is a casting agency system that manages actors and movies. The following database tables exist:

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


The application is deployed on Heroku -  https://capstone10051997.herokuapp.com/