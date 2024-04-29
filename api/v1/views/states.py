#!/usr/bin/python3
""" used to retrive states data """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states')
def states():
    state_s = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(state_s)


@app_views.route('/states/<state_id>')
def state_by_id(state_id):
    """ retrives a state with a given id """
    state_s = [state.to_dict() for state in storage.all(State).values()
               if state.id == state_id]
    if state_s == []:
        abort(404)
    return jsonify(state_s)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state_by_id(state_id):
    """ deletes a state with the given id """
    for state in storage.all(State).values():
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'])
def create_state():
    """ creates a state """
    given_json = request.get_json()
    if given_json is None:
        abort(400, "Not a JSON")
    elif 'name' not in given_json.keys():
        abort(400, "Missing name")
    new_state = State(name=given_json.get('name'))

    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state_by_id(state_id):
    """ updates a state with the given id """
    state_to_update = [state for state in storage.all(State).values()
                       if state.id == state_id]
    update = request.get_json()

    if state_to_update == []:
        abort(404)
    if not update:
        abort(400, 'Not a JSON')

    state_to_update[0].name = update['name']
    storage.save()

    return jsonify(state_to_update[0].to_dict()), 200
