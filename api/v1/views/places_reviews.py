#!/usr/bin/python3
""" places.py that handles all default RestFul API actions"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from flask import abort, request, jsonify


@app_views.route("/places/<place_id>/reviews")
def get_reviews(place_id):
    """ get reviews"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route("/reviews/<review_id>")
def get_review(review_id):
    """ get review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'])
def delete_review(review_id):
    """ delete review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'])
def post_review(place_id):
    """ post review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    request_data = request.get_json()
    if request_data is None:
        return jsonify('Not a JSON'), 400
    if 'user_id' not in request_data:
        return jsonify('Missing user_id'), 400
    user = storage.get(User, request_data['user_id'])
    if not user:
        abort(404)
    if 'text' not in request_data:
        return jsonify('Missing text'), 400

    new_review = Review(**request_data)
    setattr(new_review, 'place_id', place_id)
    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'])
def put_review(review_id):
    """ put review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    request_data = request.get_json()
    if request_data is None:
        return jsonify('Not a JSON'), 400
    for key, value in request_data.items():
        if key not in ['id', 'city_id', 'user_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
