from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    mobile = db.Column(db.String(15), nullable=True)

    def __init__(self, email, password, mobile=None):
        self.email = email
        self.password = password
        self.mobile = mobile
    def json(self):
        return {
            "id": self.id,
            "email": self.email
        }

    def save_to_db(self):
        print(self)
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_user_from_email(cls, email):
        print("CHECK USER ", email)
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_user_by_id(cls, _id):
        return cls.query.filter_by(_id).first()
