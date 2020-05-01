#!/usr/bin/python3
"""Create a new view for Review object that handles all default RestFul API"""
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.amenity import Amenity
from api.v1.views import app_views
import os


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
def delete_ameny(place_id, amenity_id):
    """delete amenity"""
    dic_amenity = storage.all(Amenity)
    dic_place = storage.all(Place)
    id_ame = "Amenity." + amenity_id
    id_pla = "Place." + place_id
    if (id_ame not in dic_amenity.keys() or id_pla not in dic_place.keys()):
        abort(404)
    obj_amenity = storage.get(Amenity, amenity_id)
    obj_place = storage.get(Place, place_id)
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        if obj_amenity not in obj_place.amenities:
            abort(404)
        else:
            obj_place.amenities.remove(obj_amenity)
    else:
        if amenity_id not in obj_place.amenity_ids:
            abort(404)
        else:
            obj_place.amenity_ids.delete(amenity_id)
    storage.save()
    return jsonify({})


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
