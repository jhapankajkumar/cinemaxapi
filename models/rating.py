from db import db


class RateModel(db.Model):
    __tablename__ = "ratings"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float(precision=2), nullable=True)
    # Setting the foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    def __init__(self, user_id, media_id, rating):
        self.user_id = user_id
        self.rating = rating
        self.id = media_id

    def json(self):
        return {
            "id": self.id,
            "rating": self.rating
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_db(self):
        db.session.update(self)
        db.session.commite()

    @classmethod
    def get_rating(cls, user_id, media_id):
        return cls.query.filter_by(user_id=user_id, id=media_id).first()
