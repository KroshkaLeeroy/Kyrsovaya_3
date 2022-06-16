from marshmallow import Schema, fields

from setup_db import db


class User(db.Model):
    __table__name = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    favorite_genre = db.Column(db.String(255))
    #favorite_genre_id = db.Column(db.String(255))

class UserSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    password = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Str()