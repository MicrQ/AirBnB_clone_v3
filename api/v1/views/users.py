#!/usr/bin/python3
""" all routes for users """


from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users')
def users():
    """ a route to retrive list of all users """
    users = [user.to_dict()
             for user
             in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>')
def get_user_by_id(user_id):
    """ used to retrive an user by its id """
    user = [user.to_dict()
            for user in storage.all(User).values()
            if user.id == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify(user[0])


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE'])
def delete_user_by_id(user_id):
    """ used to delete user by id """
    user = [user for user in storage.all(User).values()
            if user.id == user_id]
    if len(user) == 0:
        abort(404)
    storage.delete(user[0])
    storage.save()

    return jsonify({})


@app_views.route('/users', methods=['GET', 'POST'])
def create_user():
    """ used to create a new user """
    given_json = request.get_json()
    if given_json is None:
        abort(400, "Not a JSON")
    elif 'email' not in given_json.keys():
        abort(400, "Missing email")
    elif 'password' not in given_json.keys():
        abort(400, "Missing password")
    new_user = User(email=given_json.get('email'),
                    password=given_json.get('password'))
    storage.new(new_user)
    storage.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'PUT'])
def update_user(user_id):
    """ used to update user's data(password) """
    user = [user for user in storage.all(User).values()
            if user.id == user_id]
    if len(user) == 0:
        abort(404)
    given_json = request.get_json()
    if given_json is None:
        abort(400, "Not a JSON")
    elif 'password' not in given_json.keys():
        abort(400, "Missing password")
    user[0].password = given_json.get('password')
    storage.save()

    return jsonify(user[0].to_dict())
