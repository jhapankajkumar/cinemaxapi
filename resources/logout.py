from flask_restful import Resource, reqparse
from blacklist import BLACKLIST
from error import Error
from flask import session
from flask_jwt_extended import (jwt_required, get_jwt_identity, get_raw_jwt)

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']  # jti is "JWT ID", a unique identifier for a JWT.
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200