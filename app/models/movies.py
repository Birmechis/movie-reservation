from datetime import datetime, timezone
from app.extension import db


class Movies(db.Model):

    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    language = db.Column(db.String(120), nullable=False)
    poster_url = db.Column(db.String(255))
    trailer_url = db.Column(db.String(255))
    status = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, defualt=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    creator = db.relationship(
        "User",
        back_populates="movies"
    )

    movie_genres = db.relationship(
        "MovieGenres",
        back_populates="movies",
        cascade="all, delete-orphan"
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "duration_minutes": self.duration_minutes,
            "release_date": self.release_date.isoformat() if self.release_date else None,
            "language": self.language,
            "poster_url": self.poster_url,
            "trailer_url": self.trailer_url,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self):
        return f"<Movie {self.title}>"
    