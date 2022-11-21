import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from flask_migrate import Migrate

#database_path = "postgresql://postgres:1234@localhost:5432/capstone"

database_path = os.environ.get('DATABASE_URL')

if database_path is None:
    database_path = "postgresql://postgres:1234@localhost:5432/capstone"
    

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    
actor_movie = db.Table("actor_movie",
    db.Column("actor_id", db.Integer, db.ForeignKey("movie.id")),
    db.Column("movie_id", db.Integer, db.ForeignKey("actor.id"))
 )


class Movie(db.Model):
    #__tablename__="movies"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.String, nullable=False)
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        formatted_actors = []
        for actor in self.actors:
            formatted_actors.append(actor.id)
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "actors": formatted_actors,
        }
    

class Actor(db.Model):
    #__tablename__="actors"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    movies = db.relationship("Movie", secondary=actor_movie, backref=db.backref("actors", lazy=True))
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def format(self):
        formatted_movies = []
        for movie in self.movies:
            formatted_movies.append(movie.id)
        return {
            "id": self.id,
            "name": self.name,
            "movies": formatted_movies
        }
    
