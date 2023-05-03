#!/usr/bin/python3

"""Contains the places_amenities view for the API
    """


from flask import jsonify, make_response, abort
from models import storage
from models.amenity import Amenity
from models.place import Place
from api.v1.views import app_views


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieves all amenities associated with a place"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify([
        amenity.to_dict() for amenity in storage.all(Amenity).values()
        if amenity in place.amenities
    ])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place_amenity(place_id, amenity_id):
    """Returns an empty dictionary with the status code 200"""
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)

    obj_amenity = storage.get(Amenity, amenity_id)
    if obj_amenity is None:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if obj_amenity in obj_place.amenities:
            obj_place.amenities.remove(obj_amenity)
            storage.save()
    else:
        if obj_amenity.id in obj_place.amenity_ids:
            obj_place.amenity_ids.remove(obj_amenity.id)
            storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """Link an amenity object to a place"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenities = place.amenities
    if amenity in amenities:
        place.save()
        return make_response(jsonify(amenity.to_dict()), 200)
    amenities.append(amenity)
    place.amenities = amenity
    # setattr(place, amenity_ids, amenities)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
