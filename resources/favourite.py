from flask_restful import Resource, reqparse
from error import Error
from models.favourite import FavouriteModel
from flask_jwt_extended import (jwt_required,
                                jwt_refresh_token_required,
                                get_jwt_identity)

parser = reqparse.RequestParser()
parser.add_argument('media_type',
                    type=str,
                    required=True,
                    help="Media type can not be empty")

parser.add_argument('id',
                    type=int,
                    required=True,
                    help="Media Id can not be empty")
parser.add_argument('title',
                    type=str)

parser.add_argument('poster_path',
                    type=str)

parser.add_argument('release_date',
                    type=str)

parser.add_argument('vote_average',
                    type=str)

parser.add_argument('backdrop_path',
                    type=str)

parser.add_argument('original_title',
                    type=str)


class Favourite(Resource):
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        data = parser.parse_args()
        media_id = data['id']
        media_type = data['media_type']
        print("USER_ID", user_id)
        print("Media_ID", media_id)
        if FavouriteModel.get_favourite(user_id,
                                        media_type,
                                        media_id):
            return {
                "message" : "Item Already added to favourites"
            }

        try:
            new_favourite: FavouriteModel = FavouriteModel(media_id,
                                                           user_id,
                                                           media_type,
                                                           data['title'],
                                                           data['original_title'],
                                                           data['release_date'],
                                                           data['vote_average'],
                                                           data['poster_path'],
                                                           data['backdrop_path'])
            print("NEW FAVOURITE", new_favourite)
            new_favourite.save_to_db()
        except:
            return {
                "errorCode": Error.FAILED_TO_MARK_FAVOURITE,
                "message": "Failed to mark favourite , please try after some time"
            }, 500

        return {
            "message": "Favourite marked",
            "id": media_id,
            "media_type": media_type
        }, 201

    @jwt_required
    def delete(self):
        user_id = get_jwt_identity()
        data = parser.parse_args()
        media_id = data['id']
        media_type = data['media_type']
        media:FavouriteModel = FavouriteModel.get_favourite(user_id,
                                                            media_type,
                                                            media_id)
        if media:
            try:
                media.delete_from_db()
            except:
                return {
                           "errorCode": Error.FAILED_TO_DELETE_FAVOURITE,
                           "message": "Failed to delete favourite , please try after some time"
                       }, 500
            return {
                       "message": "Favourite deleted",
                       "id": media_id,
                       "media_type": media_type
                   }, 201
        return {
                   "errorCode": Error.FAILED_TO_FETCH_DATA,
                   "message": "No Record found , please try after some time"
               }, 201


class FavouriteList(Resource):
    @jwt_required
    def get(self, media_type):
        if media_type is None:
            return {
                       "errorCode": Error.FAVOURITE_MISSING_REQUEST,
                       "message": "There is problem while login, please try after some time"
                   }, 400
        user_id = get_jwt_identity()

        try:
            results: [FavouriteModel] = FavouriteModel.get_favourites(media_type=media_type,
                                                                      user_id=user_id)
            if results:
                return {
                           "results": [result.json() for result in results]
                       }, 200

            return {
                "results": []
            }

        except:
            return {
                       "errorCode": Error.FAILED_TO_FETCH_DATA,
                       "message": "Failed to fetch records, please try after some time"
                   }, 500


class FavouriteCheck(Resource):
    @jwt_required
    def get(self, media_id):
        user_id = get_jwt_identity()
        media = FavouriteModel.is_favourite(user_id, media_id)
        if media:
            return {
                "result" : True,
                "media":media.json()
            }

        return {
            "result": False
        }

