from flask_restful import Resource, reqparse
from models.user import UserModel
from error import Error
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (jwt_required,
                                get_jwt_identity,
                                create_access_token,
                                create_refresh_token)

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

_parser.add_argument('mobile',
                     type=str,
                     required=False
                     )

_parser.add_argument('name',
                     type=str,
                     required=True,
                     help="Name can not be empty"
                     )


class UserRegister(Resource):
    def post(self):
        # get data from parser
        data = _parser.parse_args()
        print("NAME", data['name'])
        print("EMAIL", data['email'])
        print("PASSWORD", data['password'])
        print("MOBILE", data['mobile'])
        print(self)
        # # Validate Email
        # if not is_valid_email(data['email']):
        #     return {
        #         "errorCode": Error.INVALID_EMAIL,
        #         "message": "Email address is not valid"
        #     }

        # Check if user is already exists
        if UserModel.get_user_from_email(data['email']):
            print("USER ALREADY EXISTS")
            return {
                       "errorCode": Error.USER_ALREADY_EXISTS,
                       "message": "User already registered"
                   }, 400
        print("NEW USER")
        new_user: UserModel = UserModel(data['name'], data['email'], data['password'], data['mobile'])
        try:
            new_user.save_to_db()

        except:
            return {
                       "errorCode": Error.USER_REGISTRATION_FAILED,
                       "message": "Failed to register user, please try after sometime"
                   }, 500
        return {"message": "You have registered successfully"}, 201


class User(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user: UserModel = UserModel.get_user_by_id(user_id)
        if user:
            return user.json()
        return {
            "message": "User does not exists"
        },404



class UserLogin(Resource):
    def post(self):
        data = _parser.parse_args()
        try:
            user = UserModel.get_user_from_email(data['email'])
            if user and safe_str_cmp(user.password, data['password']):
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(identity=user.id)
                return {
                           "access_token": access_token,
                           "refresh_token": refresh_token
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

class UserLogout(Resource):
    @jwt_required
    def post(self):
        pass
