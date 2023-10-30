#!/usr/bin/python3
""" states.py that handles all default RestFul API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, request, jsonify


@app_views.route("/states")
def all_states():
    """ all states"""
    len = storage.count(State)
    new_list = []
    for i in range(len):
        state = State.to_dict(list(storage.all(State).values())[i])
        new_list.append(state)
    return jsonify(new_list)


@app_views.route("/states/<state_id>")
def get_state(state_id):
    """ get state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(State.to_dict(state))


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    """ delete state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'])
def post_state():
    """ post state"""

    request_data = request.get_json()
    if request_data is None:
        return jsonify('Not a JSON'), 400
    if 'name' not in request_data:
        return jsonify('Missing name'), 400

    new_state = State(**request_data)
    storage.new(new_state)
    storage.save()

    return jsonify(State.to_dict(new_state)), 201


@app_views.route("/states/<state_id>", methods=['PUT'])
def put_state(state_id):
    """ put state"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        return jsonify('Not a JSON'), 400
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(State.to_dict(state)), 200
