from flask_restful import Resource, reqparse
from models.user import UserModel
from error import Error
from flask import session
from flask_jwt_extended import (create_access_token,
                                create_refresh_token)
from werkzeug.security import safe_str_cmp

class UserLogin(Resource):
    _parser = reqparse.RequestParser()
    _parser.add_argument('email',
                         type=str,
                         required=True,
                         help="Email does not found in request"
                         )
    _parser.add_argument('password',
                         type=str,
                         required=True,
                         help="Password does not found in request")

    def post(self):
        data = self._parser.parse_args()
        session['email'] = data['email']
        try:
            user:UserModel = UserModel.get_user_from_email(data['email'])
            if user and safe_str_cmp(user.password, data['password']):
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(identity=user.id)
                return {
                           "access_token": access_token,
                           "refresh_token": refresh_token,
                            "user" : user.json()
                       }, 200
            else:
                return {
                           "errorCode": Error.INVALID_CREDENTIAL,
                           "message": "Invalid Credential"
                       }, 400

        except:
            return {
                       "errorCode": Error.FAILED_TO_LOGIN,
                       "message": "There is problem while login, please try after some time"
                   }, 500
