from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extension import db
from app.models import Movies, Genres, MovieGenres


movie_bp = Blueprint('movie', __name__)

@movie_bp.route('/movies', methods=['GET'])
@jwt_required()
def get_movies():

    page = max(1, request.args.get('page', 1, type=int))
    limit = max(1, min(request.args.get('limit', 10, type=int), 50))

    calculate_offest = (page-1)*limit
    total = Movies.query.count()
    records = Movies.query.offset(calculate_offest).limit(limit).all()

    return jsonify({
          "moveis": [mv.to_dict() for mv in records],
          "page": page,
          "limit": limit,
          "total": total
    }), 200

@movie_bp.route('/movies/<int:movie_id>', methods=['GET'])
@jwt_required()
def get_movie_by_id(movie_id):

     movie = Movies.query.filter_by(id=movie_id).first()

     if not movie:
          return jsonify({
               "error": "Movie not found"
          }), 404

     return jsonify([mv.to_dict() for mv in movie]), 200

@movie_bp.route('/movies',methods=['GET'])
@jwt_required()
def search_movies():

     search = request.args.get("title", "").strip()

     query = Movies.query

     if search:
          query = query.filter(Movies.title.ilike(f"%{search}%"))

     movies = query.all()
     return jsonify([movie.to_dict() for movie in movies]), 200

@movie_bp('/movies', methods=['GET'])
@jwt_required()
def get_movie_by_genre():

    page = max(1, request.args.get('page', 1, type=int))
    limit = max(1, min(request.args.get('limit', 10, type=int), 50))

    genre = request.args.get('genre', '').strip()

    if genre:
         
         genre = Genres.query.filter(Genres.name.ilike(genre)).first()
         if not genre:
              return jsonify({
                   "movies": [],
                   "page": page,
                   "limit": limit,
                   "total": 0
              }), 200

         query = Movies.query.join(MovieGenres).filter(MovieGenres.genre_id == genre.id)
    else:
         query = Movies.query

    calculate_offset = (page-1)*limit
    total = query.count()
    records = query.offset(calculate_offset).limit(limit).all()

    return jsonify({
         "movies": [mv.to_dict() for mv in records],
         "page": page,
         "limit": limit,
         "total": total
    }), 200