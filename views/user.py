import json

from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import MovieSchema
from implemented import auth_service

user_ns = Namespace('user')

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

@user_ns.route('/')
class AuthView(Resource):
    @check_authorization
    def post(self):
        auth_header = request.headers.get('Authorization')

        if auth_header:
            token = auth_header.split(" ")[1]

        else:
            token = ''

        uid = auth_service.decode_auth_token(token.encode())

        user = auth_service.get_by_id(uid)

        result = {
            'name':user.name,
            'surname':user.surname,
            'email':user.email
        }

        return json.dumps(result), 200
    @check_authorization
    def patch(self):

        auth_header = request.headers.get('Authorization')

        if auth_header:
            token = auth_header.split(" ")[1]

        else:
            token = ''

        uid = auth_service.decode_auth_token(token.encode())

        user = auth_service.get_by_id(uid)
        auth_service.update(user=user, name="Alex2", surname='Alex')

        result = {
            'name': user.name,
            'surname': user.surname,
            'email': user.email
        }

        return json.dumps(result), 200



@user_ns.route('/password')
class AuthViews(Resource):
    @check_authorization
    def put(self):

        auth_header = request.headers.get('Authorization')

        if auth_header:
            token = auth_header.split(" ")[1]

        else:
            token = ''

        uid = auth_service.decode_auth_token(token.encode())

        user = auth_service.get_by_id(uid)

        password_old = request.args.get('password_old')
        password_new = request.args.get('password_new')
        if auth_service.update2(user=user, password_old=password_old, password_new=password_new):


            result = {
                'name': user.name,
                'surname': user.surname,
                'email': user.email
            }

            return json.dumps(result), 200

        else:
            return 'Старый пароль неверен', 200

