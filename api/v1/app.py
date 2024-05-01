#!/usr/bin/python3
""" a flask app """

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(self):
    """ closing the storage after everything is done """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ custom 404 page """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
    port = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else 5000

    app.run(host=host, port=port, threaded=True)
