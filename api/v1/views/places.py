#!/usr/bin/python3
""" places.py that handles all default RestFul API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from flask import abort, request, jsonify


@app_views.route("/cities/<city_id>/places")
def get_places(city_id):
    """ get places"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>")
def get_place(place_id):
    """ get place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'])
def delete_place(place_id):
    """ delete place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=['POST'])
def post_place(city_id):
    """ post place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    request_data = request.get_json()
    if request_data is None:
        return jsonify('Not a JSON'), 400
    if 'user_id' not in request_data:
        return jsonify('Missing user_id'), 400
    user = storage.get(User, request_data['user_id'])
    if not user:
        abort(404)
    if 'name' not in request_data:
        return jsonify('Missing name'), 400

    new_place = Place(**request_data)
    setattr(new_place, 'city_id', city_id)
    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'])
def put_place(place_id):
    """ put place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    request_data = request.get_json()
    if request_data is None:
        return jsonify('Not a JSON'), 400
    for key, value in request_data.items():
        if key not in ['id', 'city_id', 'user_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
