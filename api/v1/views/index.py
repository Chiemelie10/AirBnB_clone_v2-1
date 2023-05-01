#!/usr/bin/python3
"""Handles the logic for the index of the api for the AirBnB clone project"""

from api.v1.views import app_views
from flask import make_response, jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def api_status():
    """Route for api status"""
    response = make_response().status.split()[-1]
    return make_response(jsonify({"status": response}))


@app_views.route('/stats')
def api_stats():
    """Provides json representation of the current statistics"""

    stats = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(stats)
