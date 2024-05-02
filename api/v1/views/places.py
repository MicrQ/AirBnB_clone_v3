#!/usr/bin/python3
""" all routes for places """


from flask import abort, jsonify, request
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places')
def places_of_a_city(city_id):
    """ used to retrive places in a city """
    cities = [city for city in storage.all(City).values()
              if city.id == city_id]
    if len(cities) == 0:
        abort(404)
    places = [place.to_dict()
              for place in storage.all(Place).values()
              if place.city_id == city_id]
    return jsonify(places)


@app_views.route('/places/<place_id>')
def a_place(place_id):
    """ used to retrive a place by its id """
    place = [place.to_dict() for place in storage.all(Place).values()
             if place.id == place_id]
    if len(place) == 0:
        abort(404)
    return jsonify(place[0])


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE'])
def delete_place_by_id(place_id):
    """ used to delete a place """
    places = [place for place in storage.all(Place).values()
              if place.id == place_id]
    if len(places) == 0:
        abort(404)
    storage.delete(places[0])
    storage.save()

    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def create_place(city_id):
    """ used to create a place in a city """
    cities = [city for city in storage.all(City).values()
              if city.id == city_id]

    if len(cities) == 0:
        abort(404)
    given_json = request.get_json()
    if given_json is None:
        abort(400, "Not a JSON")
    elif 'user_id' not in given_json.keys():
        abort(400, 'Missing user_id')
    elif 'name' not in given_json.keys():
        abort(400, "Missing name")

    users = [user for user in storage.all(User).values()
             if user.id == given_json.get('user_id')]
    if len(users) == 0:
        abort(404)

    new_place = Place(name=given_json.get('name'),
                      user_id=given_json.get('user_id'),
                      city_id=cities[0].id)
    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'PUT'])
def update_place(place_id):
    """ used to update a place """
    places = [place for place in storage.all(Place).values()
              if place.id == place_id]
    if len(places) == 0:
        abort(404)
    given_json = request.get_json()
    if given_json is None:
        abort(400, "Not a JSON")
    places[0].name = given_json.get('name')
    storage.save()

    return jsonify(places[0].to_dict())
