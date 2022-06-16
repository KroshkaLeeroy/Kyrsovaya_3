import json

from flask import request, jsonify
from flask_restx import Resource, Namespace

from dao.model.movie import MovieSchema
from implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/register')
class AuthView(Resource):

    def post(self):
        req_json = request.json
        user = auth_service.create_new_user(email=req_json.get('email'),
                                            password=req_json.get('password'))

        token = auth_service.encode_auth_token(user.id, days=10)

        return token, 201


@auth_ns.route('/login')
class AuthViews(Resource):
    def post(self):
        req_json = request.json
        user = auth_service.get_by_email(email=req_json.get('email'))

        token = auth_service.decode_auth_token(req_json.get('access_token').encode())

        result = int(token) == int(user.id)

        return json.dumps({"result": result}), 200


    def put(self):

        req_json = request.json

        token = auth_service.decode_auth_token(req_json.get('access_token').encode())
        token2 = auth_service.decode_auth_token(req_json.get('refresh_token').encode())

        if token == token2:
            token = auth_service.encode_auth_token(token, days=10)
            return json.dumps(token), 201

