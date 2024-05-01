#!/usr/bin/python3
""" used to retrive cities data """


from api.v1.views import app_views
from models.city import City
from flask import abort, jsonify, request
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities_of_state(state_id):
    """ route to retrive cities of a state """
    states = [state.to_dict() for state in storage.all(State).values()
              if state.id == state_id]
    if len(states) == 0:
        abort(404)
    cities = [city.to_dict() for city in storage.all(City).values()
              if city.state_id == state_id]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def cities(city_id):
    """ route to retrive a city information by its id """
    a_city = [city.to_dict() for city in storage.all(City).values()
              if city.id == city_id]
    if len(a_city) == 0:
        abort(404)
    return jsonify(a_city[0])


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE'])
def delete_city(city_id):
    """ used to delete a city with a given id """
    a_city = [city for city in storage.all(City).values()
              if city.id == city_id]
    if len(a_city) == 0:
        abort(404)
    storage.delete(a_city[0])
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def create_city(state_id):
    """ used to post/create a city """
    a_state = [state for state in storage.all(State).values()
               if state.id == state_id]
    if len(a_state) == 0:
        abort(404)
    given_json = request.get_json()
    if given_json is None:
        abort(400, "Not a JSON")
    elif 'name' not in given_json.keys():
        abort(400, 'Missing name')

    new_city = City(name=given_json.get('name'), state_id=state_id)
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def update_city(city_id):
    a_city = [city for city in storage.all(City).values()
              if city.id == city_id]
    if len(a_city) == 0:
        abort(404)
    given_json = request.get_json()
    if given_json is None:
        abort(400, "Not a JSON")

    a_city[0].name = given_json['name']
    storage.save()
    return jsonify(a_city[0].to_dict()), 200
