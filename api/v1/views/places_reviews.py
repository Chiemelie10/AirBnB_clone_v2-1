#!/usr/bin/python3

"""View for Review object that handles all default RESTFul API actions"""


from flask import jsonify, request, make_response, abort
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Gets all reviews associated with a place"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    return jsonify([review.to_dict() for review in reviews])


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Gets a review with the id passed"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a review with the id passed"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a new review object"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not request.is_json:
        abort(400, description='Not a JSON')
    if 'user_id' not in data:
        abort(400, description='Missing user_id')
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in data:
        abort(400, dscription='Missing text')
    review = Review(**data)
    review.place_id = place_id
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a review object with review_id"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.is_json:
        abort(400, description='Not a json')
    data = request.get_json()
    ignored = ['id', 'place_id', 'user_id', 'created_at', 'updated_at']
    for key in data.keys():
        if key not in ignored:
            setattr(review, key, data[key])
        else:
            abort(400, description='Illegal request')
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
