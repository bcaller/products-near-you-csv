from collections import namedtuple

import math

LatLngBounds = namedtuple("LatLngBounds", 'min_lat max_lat min_lng max_lng')


def query_bounds(lat, lng, radius_m):
    """
    Find a bounding rectangle of lat and lng to search within
    Very approximate
    :param lat: Decimal degrees
    :param lng: Decimal degrees
    :param radius_m: Search radius in metres
    :return: LatLngBounds
    """
    d_lat = 111000.0
    d_lng = math.cos(math.radians(lat)) * 111320.0  # Approx length in metres of a degree of longitude at this latitude
    radius_m = float(radius_m)
    return LatLngBounds(
        lat - radius_m / d_lat,
        lat + radius_m / d_lat,
        lng - radius_m / d_lng,
        lng + radius_m / d_lng
    )
