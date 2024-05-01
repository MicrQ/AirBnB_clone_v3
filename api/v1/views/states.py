#!/usr/bin/python3
""" used to retrive states data """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def states():
    """ to retrive list of all state objects """
    state_s = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(state_s), 200


@app_views.route('/states/<state_id>', methods=['GET'])
def state_by_id(state_id):
    """ retrives a state with a given id """
    state_s = [state.to_dict() for state in storage.all('State').values()
               if state.id == state_id]
    if len(state_s) == 0:
        abort(404)
    return jsonify(state_s[0]), 200


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state_by_id(state_id):
    """ deletes a state with the given id """
    a_state = [state for state in storage.all(State).values()]
    if len(a_state) == 0:
        abort(404)
    storage.delete(a_state[0])
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """ creates a state """
    given_json = request.get_json()
    if given_json is None:
        abort(400, "Not a JSON")
    elif 'name' not in given_json.keys():
        abort(400, "Missing name")
    new_state = State(name=given_json['name'])

    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state_by_id(state_id):
    """ updates a state with the given id """
    a_state = [state for state in storage.all(State).values()
               if state.id == state_id]
    given_json = request.get_json()

    if len(a_state) == 0:
        abort(404)
    if given_json is None:
        abort(400, "Not a JSON")

    a_state[0].name = given_json['name']
    storage.save()

    return jsonify(a_state[0].to_dict()), 200
