# -*- coding: utf-8 -*-
import os
from itertools import islice

from flask import Blueprint, current_app, jsonify
from flask import request
from werkzeug.exceptions import BadRequest

from server.geo import query_box, in_query_box, LatLng

api = Blueprint('api', __name__)


def data_path(filename):
    return os.path.join(current_app.config['DATA_PATH'], filename)


@api.route('/search/<float:lat>/<float:lng>/<int:radius_metres>/<int:n_products>', methods=['GET'])
def search(lat, lng, radius_metres, n_products):
    if lat > 90 or lat < -90 or lng > 180 or lng < -180:
        raise BadRequest("Bad lat/lng")
    position = LatLng(lat, lng)

    tags = {s for s in (t.strip() for t in request.args['tags'].split(',')) if len(s)} if \
        'tags' in request.args else set()  # Split comma separated tag string

    area_plus_minus = query_box(position, radius_metres)

    data = current_app.data
    nearby_shops = {shop for shop in data.shops.values() if
                    in_query_box(area_plus_minus, position, shop)}

    products = islice((p for p in data.products if p.shop in nearby_shops), n_products)

    return jsonify({'products': list(products)})
