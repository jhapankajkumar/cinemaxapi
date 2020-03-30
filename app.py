import os

from flask import Flask
from flask_restful import Api
from resources.user import UserRegister

app = Flask(__name__)

api = Api(app)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route("/")
def home():
    return "Welcome to Cinemax API"


# Register API
api.add_resource(UserRegister, "/register")


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()
    app.run(port=5001)
