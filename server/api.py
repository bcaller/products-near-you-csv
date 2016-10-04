# -*- coding: utf-8 -*-
import os
from itertools import islice
from string import lower

from flask import Blueprint, current_app, jsonify
from flask import request
from haversine import haversine
from werkzeug.exceptions import BadRequest

from server.geo import query_bounds_tester

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
    radius_km = float(radius_metres) / 1000.

    # We can speed search up by pre-computing a bounding rectangle of min / max latlng and then using haversine just
    # to see if point is within circle
    is_in_rectangular_bounds = query_bounds_tester(lat, lng, radius_km)

    nearby_shops = {shop for shop in data.shops.values() if
                    is_in_rectangular_bounds(shop.lat, shop.lng) and
                    haversine((lat, lng), (shop.lat, shop.lng)) < radius_km
                    and not (tags and tags.isdisjoint(shop.tags))}

    products = islice((p for p in data.products if p.shop in nearby_shops), n_products)

    return jsonify({'products': list(products)})
