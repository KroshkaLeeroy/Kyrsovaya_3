from sqlalchemy import desc

from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_by_email(self, email):
        return self.session.query(User).filter(User.email == email).first()

    def get_by_if(self, id):
        return self.session.query(User).filter(User.id == id).first()

    def create(self, **kwargs):
        ent = User(**kwargs)
        self.session.add(ent)
        self.session.commit()
        return ent

    def update(self, user: User, name=None, surname=None, password=None):

        if name:
            user.name = name

        if surname:
            user.surname = surname

        if password:
            user.password = password

        self.session.commit()
