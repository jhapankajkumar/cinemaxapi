from flask_restful import Resource, reqparse

from error import Error
from flask import session
from flask_jwt_extended import (jwt_required, get_jwt_identity)

class UserLogout(Resource):
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        session.pop('username')