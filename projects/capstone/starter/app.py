import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Actor, Movie, setup_db, db_drop_and_create_all_for_local_test

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  

  #GET /actors
  @app.route("/actors", methods=["GET"])
  def get_actors(payload):
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
  def get_movies(payload):
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
  def add_actor(payload):
    request_data = request.get_json()
    
    if request_data is None:
      abort(400)
    
    name = request_data.get("name"),
    age = request_data.get("age"),
    gender = request_data.get("gender"),
    movie_ids = request_data.get("movies", [])
    
    casted_movies = []
    
    for movie_id in movie_ids:
      movie = Movie.query.get(movie_id)
      if movie is None:
        abort(404)
      else:
        casted_movies.append(movie)
      
      
    new_actor = Actor(
      name=name,
      age=age,
      gender=gender,
      movies = casted_movies
    )
    
    new_actor.insert()
    
    return jsonify({
      "success": True,
      "actor": new_actor.format() 
    })

  #PATCH /actors/{id}
  @app.route("/actors/<int:actor_id>", methods=["PATCH"])
  def update_actor(payload, actor_id):
    actor = Actor.query.get(actor_id)
    
    if not actor:
      abort(404)
      
    name = request.get_json().get("name", actor.name)
    age = request.get_json().get("age", actor.age)
    gender = request.get_json().get("gender", actor.gender)
    movies = request.get_json().get("movies", [])
    
    if movies is not None:
      formatted_movies = Movie.query.filter(Movie.id.in_(movies)).all()
    else:
      formatted_movies = actor.movies
      
    actor.name = name
    actor.age = age
    actor.gender = gender
    actor.movies = formatted_movies
    actor.update()
    return jsonify({
      "success": True,
      "actor": actor.format()
    })
    
  #DELETE /movies/{id}
  @app.route("/movies/<int:movie_id>", methods=["DELETE"])
  def delete_movie(payload, movie_id):
    movie = Movie.query.get(movie_id)
    
    if movie is None:
      abort(404)
      
    movie.delete()
    
    return jsonify({
      "success": True,
      "deleted": movie.id
    })
  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)