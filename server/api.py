# -*- coding: utf-8 -*-
import os
from itertools import islice

from flask import Blueprint, current_app, jsonify
from flask import g
from flask import request

from server.geo import query_bounds

api = Blueprint('api', __name__)


def data_path(filename):
    return os.path.join(current_app.config['DATA_PATH'], filename)


@api.route('/search/<float:lat>/<float:lng>/<int:radius_metres>/<int:n_products>', methods=['GET'])
def search(lat, lng, radius_metres, n_products):
    if lat > 90 or lat < -90 or lng > 180 or lng < -180:
        raise Exception("Bad lat/lng")  # TODO:Exception class

    tags = {s for s in (t.strip() for t in request.args['tags'].split(',')) if len(s)} if \
        'tags' in request.args else set()  # Split comma separated tag string

    search_area = query_bounds(lat, lng, radius_metres)

    data = current_app.data
    nearby_shops = {shop for shop in data.shops.values() if
                    search_area.max_lat > shop.lat > search_area.min_lat and
                    search_area.max_lng > shop.lng > search_area.min_lng}

    products = islice((p for p in data.products if p.shop in nearby_shops), n_products)

    return jsonify({'products': list(products)})
