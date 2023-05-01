#!/usr/bin/python3

"""view for Amenity objects that handles all default RESTFul API actions"""


from flask import make_response, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """Retrieves all ``Amenity`` objects"""

    amenities = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in amenities.values()])


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves an ``Amenity`` object based on the id passed"""

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an ``Amenity object with the id passed"""

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """Creates an ``Amenity`` object"""

    if not request.is_json:
        abort(400, description='Not a JSON')
    if 'name' not in request.json:
        abort(400, description='Missing name')
    data = request.get_json()
    amenity = Amenity(**data)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an ``Amenity`` object with the id passed"""

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.is_json:
        abort(400, description='Not a JSON')
    ignored = ['id', 'created_at', 'updated_at']
    data = request.get_json()
    for key in data.keys():
        if key not in ignored:
            setattr(amenity, key, data[key])
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
