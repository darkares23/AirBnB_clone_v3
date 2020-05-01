#!/usr/bin/python3
"""Create a new view for Review object that handles all default RestFul API"""
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.amenity import Amenity
from api.v1.views import app_views
from os import getenv


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
    id_a = "Amenity.{}".format(amenity_id)
    id_p = "Place.{}".format(place_id)
    if (id_a not in del_amenity.keys() or id_p not in place.keys()):
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