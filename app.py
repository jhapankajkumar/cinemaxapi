import os

from flask import Flask
from flask_restful import Api
from resources.user import UserRegister, User, UserLogout
from resources.login import UserLogin
from resources.favourite import Favourite, FavouriteList, FavouriteCheck
from resources.watch import Watch, WatchList, WatchCheck
from resources.rating import MediaRating
from error import Error
from flask_jwt_extended import JWTManager

app = Flask(__name__)
jwt = JWTManager(app)

app.secret_key = 'cinemaxapi'

api = Api(app)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route("/")
def home():
    return "Welcome to Cinemax API"


@jwt.expired_token_loader
def token_expired():
    return {
        "errorCode": Error.TOKEN_EXPIRED,
        "message": "Your token expired "
    }


@jwt.invalid_token_loader
def token_invalid():
    return {
        "errorCode": Error.TOKEN_INVALID,
        "message": "Your token is invalid "
    }


@jwt.revoked_token_loader
def token_revoked():
    return {
        "errorCode": Error.TOKEN_EXPIRED,
        "message": "Your token expired "
    }


# Register API
api.add_resource(UserRegister, "/register")

# User
api.add_resource(User, "/user")

# Login API
api.add_resource(UserLogin, "/login")

# Logout API
api.add_resource(UserLogout, "/logout")

# Favourite API
api.add_resource(FavouriteList, "/favourites/<string:media_type>")
api.add_resource(FavouriteCheck, "/favourite/<int:media_id>")
api.add_resource(Favourite, "/favourite")

# Watchlist API
api.add_resource(WatchList, "/watchlist/<string:media_type>")
api.add_resource(WatchCheck, "/watch/<int:media_id>")
api.add_resource(Watch, "/watch")

# Rate
api.add_resource(MediaRating, "/rate/<int:media_id>")

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()
    app.run(port=5001)
