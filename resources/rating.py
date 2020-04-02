from flask_restful import Resource, reqparse
from error import Error
from models.rating import RateModel
from flask_jwt_extended import (jwt_required,
                                jwt_refresh_token_required,
                                get_jwt_identity)


class MediaRating(Resource):
    _parser = reqparse.RequestParser()

    _parser.add_argument('rating',
                         type=float,
                         required=True,
                         help="rating does not found in request")

    @jwt_required
    def post(self, media_id):
        data = self._parser.parse_args()
        user_id = get_jwt_identity()
        rate_model: RateModel = RateModel.get_rating(user_id, media_id)
        if rate_model:
            rate_model.rating = data['rating']
            rate_model.save_to_db()

        else:
            try:
                rating = RateModel(user_id, media_id, data['rating'])
                rating.save_to_db()
            except:
                return {
                    "message": "Could not save rating"
                }, 500

        return {
            "message": "Rated successfully"
        }

    @jwt_required
    def get(self, media_id):
        user_id = get_jwt_identity()
        rating: RateModel = RateModel.get_rating(user_id, media_id)
        if rating:
            return rating.json()
        return {
            "message": "record not found"
        }, 400




