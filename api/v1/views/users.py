#!/usr/bin/python3

"""View for User object that handles all default RESTFul API actions"""


from flask import make_response, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """Retrieves all ``user`` objects"""

    users = storage.all(User)
    return jsonify([obj.to_dict() for obj in users.values()])


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves an ``user`` object based on the id passed"""

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes an ``user object with the id passed"""

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """Creates an ``user`` object"""

    if not request.is_json:
        abort(400, description='Not a JSON')
    if 'email' not in request.json:
        abort(400, description='Missing email')
    if 'password' not in request.json:
        abort(400, description='password')
    data = request.get_json()
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates an ``user`` object with the id passed"""

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.is_json:
        abort(400, description='Not a JSON')
    ignored = ['id', 'email', 'created_at', 'updated_at']
    data = request.get_json()
    for key in data.keys():
        if key not in ignored:
            setattr(user, key, data[key])
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
