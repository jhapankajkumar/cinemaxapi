from db import db


class FavouriteModel(db.Model):

    __tablename__ = "favourites"

    id = db.Column(db.Integer, primary_key=True)
    media_type = db.Column(db.String(80))
    title = db.Column(db.String(80))
    original_title = db.Column(db.String(80), nullable=True)
    release_date = db.Column(db.String(80), nullable=True)
    vote_average = db.Column(db.Float(precision=2), nullable=True)
    poster_path = db.Column(db.String(200), nullable=True)
    backdrop_path = db.Column(db.String(200), nullable=True)

    # Setting the foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    def __init__(self,
                 _id,
                 user_id,
                 media_type,
                 title,
                 original_title,
                 release_date,
                 vote_average,
                 poster_path,
                 backdrop_path):
        print("Getting User")
        self.id = _id
        self.user_id = user_id
        self.title = title
        self.media_type = media_type
        if original_title is None:
            self.original_title = title
        else:
            self.original_title = original_title
        self.release_date = release_date
        self.vote_average = vote_average
        self.poster_path = poster_path
        self.backdrop_path = backdrop_path

    def json(self):
        return {
            "id": self.id,
            "media_type": self.media_type,
            "original_title": self.original_title,
            "title": self.title,
            "vote_average": self.vote_average,
            "release_date": self.release_date,
            "poster_path": self.poster_path,
            "backdrop_path": self.backdrop_path
        }

    # Method to add favorite in database
    def save_to_db(self):
        print("SAVE")
        db.session.add(self)
        db.session.commit()

    # Method to delete favourite from data base
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_favourites(cls, user_id, media_type):
        return cls.query.filter_by(user_id= user_id,
                                   media_type=media_type)

    @classmethod
    def get_favourite(cls, user_id,media_type, media_id):

        return cls.query.filter_by(user_id=user_id,
                                   media_type=media_type,
                                   id=media_id).first()

    @classmethod
    def is_favourite(cls, user_id, media_id):
        return cls.query.filter_by(user_id=user_id,
                                   id=media_id).first()



    

