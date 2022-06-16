from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import MovieSchema
from implemented import movie_service, auth_service

movie_ns = Namespace('movies')

def check_authorization(func):

    def check(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if auth_header:
            token = auth_header.split(" ")[1]

        else:
            token = ''

        uid = auth_service.decode_auth_token(token.encode())

        user = auth_service.get_by_id(uid)

        if user:
            return func(*args, **kwargs)
        else:
            return "Not authorized", 403

    return check



@movie_ns.route('/')
class MoviesView(Resource):
    @check_authorization
    def get(self):
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        pagination = int(request.args.get("page"))
        status = request.args.get("status")

        filters = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
            "status": status
        }
        all_movies = movie_service.get_all(filters)
        all_movies = all_movies[:pagination] if pagination else all_movies
        res = MovieSchema(many=True).dump(all_movies)
        return res, 200

    def post(self):
        req_json = request.json
        movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:bid>')
class MovieView(Resource):
    def get(self, bid):
        b = movie_service.get_one(bid)
        sm_d = MovieSchema().dump(b)
        return sm_d, 200

    def put(self, bid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = bid
        movie_service.update(req_json)
        return "", 204

    def delete(self, bid):
        movie_service.delete(bid)
        return "", 204
