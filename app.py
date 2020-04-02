import os

from flask import Flask, session,jsonify
from flask_restful import Api
from resources.user import UserRegister, User
from resources.login import UserLogin
from resources.logout import UserLogout
from resources.favourite import Favourite, FavouriteList, FavouriteCheck
from resources.watch import Watch, WatchList, WatchCheck
from resources.rating import MediaRating
from resources.change_password import ChangePassword
from error import  Error

from blacklist import BLACKLIST
from flask_jwt_extended import JWTManager

app = Flask(__name__)
jwt = JWTManager(app)



app.secret_key = 'cinemaxapi'

api = Api(app)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens


@app.route("/")
def home():
    return "Welcome to Cinemax API"


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST  # Here we blacklist particular JWTs that have been created in the past.


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired',
        'code': Error.TOKEN_EXPIRED
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token',
        'code': Error.TOKEN_INVALID
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required',
        'code': Error.TOKEN_MISSING
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked',
        'code': Error.TOKEN_REVOKED
    }), 401


# Register API
api.add_resource(UserRegister, "/register")

# User
api.add_resource(User, "/user")

# Login API
api.add_resource(UserLogin, "/login")

# Logout API
api.add_resource(UserLogout, "/logout")

api.add_resource(ChangePassword, "/password")

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
