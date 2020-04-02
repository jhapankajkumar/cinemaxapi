from flask_restful import Resource, reqparse
from models.user import UserModel
from error import Error
from flask import session
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (jwt_required, get_jwt_identity)


class ChangePassword(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('current_password',
                        type=str,
                        required=True,
                        help="Password  can not be empty")

    parser.add_argument('new_password',
                        type=int,
                        required=True,
                        help="Password can not be empty")

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        if user_id:
            data = self.parser.parse_args()
            user: UserModel = UserModel.get_user_by_id(user_id)
            if user and safe_str_cmp(user.password, data['current_password']):
                user.password = data['new_password']
                user.save_to_db()
                return {
                    "message": "Password changed successfully"
                }
            else:
                return {
                    "message": "Password does not match"
                }

        return {
            "message": "Token Expired"
        }






