import datetime
import jwt
from dao.user import UserDAO
import hashlib


class UserService:
    def __init__(self, dao):
        self.dao = dao

    def create_new_user(self, email, password):
        return self.dao.create(email=email, password=password)

    def check_auth(self, email, password):
        return str(hash(self.dao.get_by_email(email=email).password)) == str(hash(password))

    def get_by_email(self, email):
        return self.dao.get_by_email(email=email)

    def get_by_id(self, id):
        return self.dao.get_by_id(id=id)

    def encode_auth_token(self, user_id, days):
        try:
            payload = {
                "exp": str(datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=30)),
                "int": str(datetime.datetime.utcnow()),
                "sub": user_id
            }
            payload2 = {
                "exp": str(datetime.datetime.utcnow() + datetime.timedelta(days=days)),
                "int": str(datetime.datetime.utcnow()),
                "sub": user_id
            }
            return {"access_token":
                        jwt.encode(
                            payload,
                            "SECRET_KEY",
                            algorithm="HS256"),

                    "refresh_token":
                        jwt.encode(
                            payload2,
                            "SECRET_KEY",
                            algorithm="HS256")
                    }
        except Exception as e:
            return e

    def decode_auth_token(self, auth_token):
        try:
            payload = jwt.decode(auth_token, "SECRET_KEY")
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again'

    def update(self, user, name, surname):
        self.dao.update(user, name, surname)

    def update2(self, user, password_old, password_new):

        if user.password == password_old:
            self.dao.update(user=user,
                            password=password_new)

            return True
        else:
            return False
