#!/usr/bin/python3
"""Create a new view for Review object that handles all default RestFul API"""


from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views
from os import getenv


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def review_places(place_id=None):
    """Retrieves the list of all Review objects of a Place"""
    review_pla = storage.get('Place', place_id)
    if review_pla is None:
        abort(404)
    all_review = review_pla.reviews
    list_review = []
    for rev in all_review:
        list_review.append(rev.to_dict())
    return jsonify(list_review)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def one_review(review_id=None):
    """Retrieves a Review object."""
    a_review = storage.get('Review', review_id)
    if a_review is None:
        abort(404)
    return jsonify(a_review.to_dict())


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id=None, amenity_id=None):
    """Deletes a amenity object"""
    place = storage.get('Place', place_id)
    del_amenity = storage.get('Amenity', amenity_id)
    if del_amenity is None:
        abort(404)
    if place is None:
        abort(404)
    for amen in place.amenities:
        if amenity_id not in amen.id:
            abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if del_amenity not in place.amenities:
            abort(404)
        else:
            place.amenities.remove(del_amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        else:
            place.amenity_ids.delete(amenity_id)
    place.amenities.remove(del_amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_amenityw(place_id=None, amenity_id=None):
    """Creates a amenity"""
    place = storage.get('Place', place_id)
    put_amenity = storage.get('Amenity', amenity_id)
    if put_amenity is None:
        abort(404)
    if place is None:
        abort(404)
    for amen in place.amenities:
        if amenity_id not in amen.id:
            abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if put_amenity not in place.amenities:
            abort(404)
        else:
            place.amenities.remove(put_amenity)
    else:
        if amenity_id in place.amenity_ids:
            place.amenity_ids.append(amenity_id)
            storage.save()
            return jsonify(put_amenity.to_dict(), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id=None):
    """Updates a Review object"""
    id_review = storage.get('Review', review_id)
    if id_review is None:
        abort(404)
    res = request.get_json()
    if res is None:
        abort(400, "Not a JSON")
    for k, v in res.items():
        if k != 'id' and k != 'created_at' and \
           k != 'updated_at' and k != 'user_id' and k != 'place_id':
            setattr(id_review, k, v)
    storage.save()
    return jsonify(id_review.to_dict()), 200
