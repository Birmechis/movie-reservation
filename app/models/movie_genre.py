from app.extension import db


class MovieGenres(db.Model):

    __tablename__ = "movie_genre"

    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), ondelete="CASCADE", primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), ondelete="CASCADE", primary_key=True)

    movie = db.relationship(
        "Movies",
        back_populates="movie_genre"
    )

    genre = db.relationship(
        "Genres",
        back_populates="movie_genres"
    )

    def to_dict(self):
        return {
            "movie_id": self.movie_id,
            "genre_id": self.genre_id,
            "genre_name": self.genre.name if self.genre else None
        }