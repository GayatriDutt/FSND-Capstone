import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
from flask_migrate import Migrate
from flask_moment import Moment
from auth import requires_auth, AuthError

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  
  API_AUDIENCE = os.environ.get('API_AUDIENCE')
  AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
  AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
  AUTH0_CALLBACK_URL = os.environ.get('AUTH0_CALLBACK_URL')

  db_drop_and_create_all()

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  #GET /actors
  @app.route("/actors", methods=["GET"])
  def get_actors():
    actors = Actor.query.all()
    
    formatted_actors = []
    for actor in actors:
      formatted_actors.append(actor.format())
      
    return jsonify({
      "success": True,
      "actors": formatted_actors
    })

  #GET /movies
  @app.route("/movies", methods=["GET"])
  def get_movies():
    movies = Movie.query.all()
    formatted_movies = []
    for movie in movies:
      formatted_movies.append(movie.format())
    return jsonify({
      "success": True,
      "movies": formatted_movies
    })

  #POST /actors
  @app.route("/actors", methods=["POST"])
  def add_actor():
    request_data = request.get_json()
    
    if request_data is None:
      abort(400)
    
    name = request_data.get("name"),
    movie_ids = request_data.get("movies", [])
    
    list_movies = []
    
    for movie_id in movie_ids:
      movie = Movie.query.get(movie_id)
      if movie is None:
        abort(404)
      else:
        list_movies.append(movie)
      
      
    new_actor = Actor(
      name=name,
      movies = list_movies
    )
    
    new_actor.insert()
    
    return jsonify({
      "success": True,
      "actor": new_actor.format() 
    })

  #PATCH /actors/{id}
  @app.route("/actors/<int:actor_id>", methods=["PATCH"])
  def update_actor(actor_id):
    actor = Actor.query.get(actor_id)
    
    if not actor:
      abort(404)
      
    name = request.get_json().get("name", actor.name)
    movies = request.get_json().get("movies", [])
    
    if movies is not None:
      formatted_movies = Movie.query.filter(Movie.id.in_(movies)).all()
    else:
      formatted_movies = actor.movies
      
    actor.name = name
    actor.movies = formatted_movies
    actor.update()
    return jsonify({
      "success": True,
      "actor": actor.format()
    })

  #DELETE /movies/{id}
  @app.route("/movies/<int:movie_id>", methods=["DELETE"])
  def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    
    if movie is None:
      abort(404)
      
    movie.delete()
    
    return jsonify({
      "success": True,
      "deleted": movie.id
    })
  
  '''@app.errorhandler(404)
  def not_found(error):
    return jsonify({"success": False, "error": 404, "message": "Not found"}), 404'''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({"success": True, "message": "Welcome to my capstone project on casting agency"})
  @app.errorhandler(500)
  def internal_server(error):
    return jsonify({"success": False, "error": 500, "message": "Internal server error"}), 500

  return app

app = create_app()

if __name__ == '__main__':
    app.run()