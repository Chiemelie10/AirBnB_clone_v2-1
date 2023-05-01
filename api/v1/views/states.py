#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions"""

from flask import make_response, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieves all State objects"""

    states_list = [state.to_dict() for state in storage.all(State).values()]
    return make_response(jsonify(states_list))


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object with an id passed in ``state_id``"""

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return make_response(jsonify(state.to_dict()))


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state with the id passed"""

    states = storage.all(State).values()
    state = [state for state in states if state.id == state_id]
    if len(state) == 0:
        abort(404)
    storage.delete(state[0])
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def post_state():
    """Creates a state object"""

    data = request.get_json()
    if not request.is_json:
        abort(400, description='Not a JSON')
    if 'name' not in request.json:
        abort(400, description='Missing name')
    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    name = request.get_json()['name']
    if name:
        state.name = name
        state.save()
    return make_response(jsonify(state.to_dict()), 200)
