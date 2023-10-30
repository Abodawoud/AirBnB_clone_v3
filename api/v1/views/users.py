#!/usr/bin/python3
""" users.py that handles all default RestFul API actions"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, request, jsonify


@app_views.route("/users")
def all_users():
    """all users"""
    len = storage.count(User)
    new_list = []
    for i in range(len):
        user = User.to_dict(list(storage.all(User).values())[i])
        new_list.append(user)
    return jsonify(new_list)


@app_views.route("/users/<user_id>")
def get_user(user_id):
    """ get user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    """ delete user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'])
def post_user():
    """ post user"""

    request_data = request.get_json()
    if request_data is None:
        return jsonify('Not a JSON'), 400
    if 'email' not in request_data:
        return jsonify('Missing email'), 400
    if 'password' not in request_data:
        return jsonify('Missing password'), 400

    user = User(**request_data)
    storage.new(user)
    storage.save()

    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'])
def put_user(user_id):
    """ put user"""

    user = storage.get(User, user_id)
    if not user:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        return jsonify('Not a JSON'), 400
    for key, value in request_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
