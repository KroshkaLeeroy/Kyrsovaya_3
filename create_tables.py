from app import *


app = create_app(Config())

with app.app_context():
    db.drop_all()
    db.create_all()