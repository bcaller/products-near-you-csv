# -*- coding: utf-8 -*-
import os
from itertools import islice
from string import lower

from flask import Blueprint, current_app, jsonify
from flask import request
from haversine import haversine
from werkzeug.exceptions import BadRequest

api = Blueprint('api', __name__)


def data_path(filename):
    return os.path.join(current_app.config['DATA_PATH'], filename)


@api.route('/search/<float:lat>/<float:lng>/<int:radius_metres>/<int:n_products>', methods=['GET'])
def search(lat, lng, radius_metres, n_products):
    if lat > 90 or lat < -90 or lng > 180 or lng < -180:
        raise BadRequest("Bad lat/lng")

    tags = {s for s in (t.strip() for t in lower(request.args['tags']).split(',')) if len(s)} if \
        'tags' in request.args else set()  # Split comma separated tag string

    data = current_app.data

    # We can speed this up by making a bounding rectangle of min / max latlng and then using haversine just to see
    # if point is within circle
    nearby_shops = {shop for shop in data.shops.values() if
                    haversine((lat, lng), (shop.lat, shop.lng)) * 1000. < radius_metres
                    and (not tags or not tags.isdisjoint(shop.tags))}

    products = islice((p for p in data.products if p.shop in nearby_shops), n_products)

    return jsonify({'products': list(products)})
