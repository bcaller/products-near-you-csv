from collections import namedtuple

import math

LatLng = namedtuple("LatLng", 'lat lng')


def query_box(position, radius_m):
    """
    Find a bounding rectangle of lat and lng to search within
    Very approximate
    :param position: LatLng of starting position
    :param radius_m: Search radius in metres
    :return: LatLng of degrees plus or minus for lat and lng
    """
    d_lat = 111000.0
    d_lng = math.cos(math.radians(position.lat)) * 111320.0  # Approx length in metres of a degree of longitude at this latitude
    radius_m = float(radius_m)
    return LatLng(
        radius_m / d_lat,
        radius_m / d_lng,
    )


def in_query_box(offset, pos_from, to_pos):
    return _check_coordinate_bounds(offset, pos_from, 'lat', to_pos) and _check_coordinate_bounds(offset, pos_from, 'lng', to_pos)


def _check_coordinate_bounds(bounds, centre, coord, object_position):
    k = 0 if coord == 'lat' else 1
    low = centre[k] - bounds[k]
    high = centre[k] + bounds[k]
    obj_pos = getattr(object_position, coord)
    if low < obj_pos < high:
        return True
    boundary = 90 if coord == 'lat' else 180
    if low < -boundary:
        return low < obj_pos - (boundary * 2) < high
    elif high > boundary:
        return low < obj_pos + (boundary * 2) < high
    return False
