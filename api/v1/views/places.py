#!/usr/bin/python3

"""View for Place objects that handles all default RESTFul API actions"""


from flask import make_response, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves all places linked to a city with the id passed"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    return jsonify([city.to_dict() for city in places])


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Gets a place with the id passed"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place with the id passed"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a new place object"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not request.is_json:
        abort(400, description='Not a JSON')
    if 'user_id' not in data:
        abort(400, description='Missing user_id')
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, description='Missing name')
    place = Place(**data)
    place.city_id = city_id
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a place object with place_id"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, description='Not a json')
    data = request.get_json()
    ignored = ['id', 'city_id', 'user_id', 'created_at', 'updated_at']
    for key in data.keys():
        if key not in ignored:
            setattr(place, key, data[key])
        else:
            abort(400, description='Illegal request')
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
