#!/usr/bin/python3
""" holds class Places-Amenity"""
from models.review import Review
from models.amenity import Amenity
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from api.v1.views import app_views
from os import getenv


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenity(place_id=None):
    """get amenities list"""
    places = "Place." + place_id
    my_dic = storage.all()
    dict_amenities = []
    if (places in my_dic.keys()):
        list_amenities = my_dic[places].amenities
        for amenitie in list_amenities:
            dict_amenities.append(amenitie.to_dict())
        return jsonify(dict_amenities)
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_ameny(place_id=None, amenity_id=None):
    """delete amenity"""
    dic_amenities = storage.all(Amenity)
    dic_places = storage.all(Place)
    amenities_id = "Amenity." + amenity_id
    places_id = "Place." + place_id
    ob_amenities = storage.get(Amenity, amenity_id)
    ob_places = storage.get(Place, place_id)
    if (amenities_id not in dic_amenities.keys() or
       places_id not in dic_places.keys()):
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if ob_amenities not in ob_places.amenities:
            abort(404)
        else:
            ob_places.amenities.remove(ob_amenities)
    else:
        if amenity_id not in ob_places.amenity_ids:
            abort(404)
        else:
            ob_places.amenity_ids.delete(amenity_id)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_revi(place_id, amenity_id):
    """POST amenity list"""
    d_amenities = storage.all(Amenity)
    d_places = storage.all(Place)
    id_amenities = "Amenity." + amenity_id
    id_places = "Place." + place_id
    amenities_ob = storage.get(Amenity, amenity_id)
    places_ob = storage.get(Place, place_id)
    if (id_amenities not in d_amenities.keys() or
       id_places not in d_places.keys()):
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenities_ob in places_ob.amenities:
            return jsonify(amenities_ob.to_dict())
        else:
            places_ob.amenities.append(amenities_ob)
            storage.save()
            return jsonify(amenities_ob.to_dict(), 201)
    else:
        if amenity_id in places_ob.amenity_ids:
            places_ob.amenity_ids.append(amenity_id)
            storage.save()
            return jsonify(amenities_ob.to_dict(), 201)
