#!/usr/bin/python3
"""Renders api data using Flask"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})

    app.register_blueprint(app_views)
    return app


if __name__ == '__main__':
    app = create_app()
    port_env = getenv('HBNB_API_PORT', '5000')
    host_env = getenv('HBNB_API_HOST', '0.0.0.0')
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.url_map.strict_slashes = False

    @app.teardown_appcontext
    def shutdown(self):
        """Tear down function for app context"""

        storage.close()

    @app.errorhandler(404)
    def not_found(error):
        """Error response for the 404 status code"""

        return make_response(jsonify({"error": "Not found"}), 404)

    app.run(host=host_env, port=port_env, threaded=True)
