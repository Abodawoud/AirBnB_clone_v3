#!/usr/bin/python3
""" states.py that handles all default RestFul API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.amenity import Amenity
from flask import abort, request, jsonify
import json


@app_views.route("/amenities")
def all_amenities():
    """ all amenities"""
    len = storage.count(Amenity)
    new_list = []
    for i in range(len):
        amenity = Amenity.to_dict(list(storage.all(Amenity).values())[i])
        new_list.append(amenity)
    return jsonify(new_list)


@app_views.route("/amenities/<amenity_id>")
def get_amenity(amenity_id):
    """ get amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def delete_amenity(amenity_id):
    """ delete amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'])
def post_amenity():
    """ post amenity"""

    request_data = request.get_json()
    if request_data is None:
        return jsonify('Not a JSON'), 400
    if 'name' not in request_data:
        return jsonify('Missing name'), 400

    new_amenity = Amenity(**request_data)
    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
def put_amenity(amenity_id):
    """ put amenity"""

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        return jsonify('Not a JSON'), 400
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
