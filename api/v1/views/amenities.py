#!/usr/bin/python3
""" all routes for amenities """


from flask import abort, jsonify, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'])
def amenities():
    """ a route to retrive list of all amenities """
    amenitie_s = [amenity.to_dict()
                  for amenity
                  in storage.all(Amenity).values()]
    return jsonify(amenitie_s)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_by_id(amenity_id):
    """ used to retrive an amenity by its id """
    amenity = [amenity.to_dict()
               for amenity in storage.all(Amenity).values()
               if amenity.id == amenity_id]
    if len(amenity) == 0:
        abort(404)
    return jsonify(amenity[0])


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE'])
def delete_amenity_by_id(amenity_id):
    """ used to delete amenity by id """
    amenity = [amenity for amenity in storage.all(Amenity).values()
               if amenity.id == amenity_id]
    if len(amenity) == 0:
        abort(404)
    storage.delete(amenity[0])
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities', methods=['GET', 'POST'])
def create_amenity():
    """ used to create a new amenity """
    given_json = request.get_json()
    if given_json is None:
        abort(400, "Not a JSON")
    elif 'name' not in given_json.keys():
        abort(400, "Missing name")

    new_amenity = Amenity(name=given_json['name'])
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT'])
def update_amenity(amenity_id):
    """ used to update an amenity by id """
    amenity = [amenity for amenity in storage.all(Amenity).values()
               if amenity.id == amenity_id]
    if len(amenity) == 0:
        abort(404)
    given_json = request.get_json()
    if given_json is None:
        abort(400, "Not a JSON")
    elif 'name' not in given_json.keys():
        abort(400, "Missing name")
    amenity[0].name = given_json.get('name')
    storage.save()

    return jsonify(amenity[0].to_dict()), 200
