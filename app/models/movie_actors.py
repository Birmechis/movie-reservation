from app.extension import db

class MovieActors(db.Model):

    __tablename__ = "movie_actors"

    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), ondelete="CASCADE", primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("actors.id"), ondelete="CASCADE", primary_key=True)

    movie = db.relationship(
        "Movies",
        back_populate = "movie_actors"
    )

    actors = db.relationship(
        "Actors",
        back_populates = "movie_actors"
    )

    def to_dict(self):
        return {
            "movie_id": self.movie_id,
            "actor_id": self.actor_id
        }