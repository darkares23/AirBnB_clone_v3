#!/usr/bin/python3
"""Create a new view for Review object that handles all default RestFul API"""
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities_places(place_id=None):
    """Retrieves the list of all Review objects of a Place"""
    ameni_pla = storage.get('Place', place_id)
    amen = ameni_pla.amenities
    if ameni_pla is None:
        abort(404)
    list_amenities = []
    for amenity in amen:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


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
    place.amenities.append(put_amenity)
    storage.save()
    return jsonify(put_amenity.to_dict()), 201
