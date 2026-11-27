from app.extension import db


class Actors(db.Model):

    __tablename__ = "actors"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    biography = db.Column(db.Text)
    photo_url = db.Column(db.String(255))

    movie_actors = db.relationship(
        "MovieActors",
         back_populates = "actors", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "biography": self.biography,
            "photo_url": self.photo_url
        }

    def __repr__(self):
        return f"<Actors: {self.full_name}>"