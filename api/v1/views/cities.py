#!/usr/bin/python3
"""View for City objects that handles all default RESTFul API actions"""

from flask import jsonify, request, make_response, abort
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Gets all cities associated with a state"""

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    return jsonify([city.to_dict() for city in cities])


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Gets a city with the id passed"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes a city with the id passed"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a new city object"""

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not request.is_json:
        abort(400, description='Not a JSON')
    if 'name' not in data:
        abort(400, description='Missing name')
    city = City(**data)
    city.state_id = state_id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a city object with city_id"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400, description='Not a json')
    data = request.get_json()
    ignored = ['id', 'state_id', 'created_at', 'updated_at']
    for key in data.keys():
        if key not in ignored:
            setattr(city, key, data[key])
        else:
            abort(400, description='Illegal request')
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
