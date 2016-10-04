import math


def query_bounds_tester(lat, lng, radius_km):
    """
    Make a bounding rectangle of lat and lng to search within
    Very approximate
    :param lat: Decimal degrees of centre
    :param lng: Decimal degrees of centre
    :param radius_km: Search radius in kilometres (float)
    :return: Callable[[float, float], bool] takes lat, lng and returns whether in bounding rectangle
    """
    radius_km = min(radius_km, 6371.0 / 2)  # Max radius is half way round Earth

    lat_checker = _lat_bounds(lat, radius_km)
    lng_checker = _lng_bounds(lat, lng, radius_km)

    def query(latitude, longitude):
        return lat_checker(latitude) and lng_checker(longitude)

    return query


def _lat_bounds(lat, radius_m):
    d_lat = radius_m / 111.0  # Number of degrees for radius_metres
    min_lat = lat - d_lat
    max_lat = lat + d_lat
    if min_lat >= -90 and max_lat <= 90:
        return lambda x: (min_lat < x < max_lat)
    elif min_lat < -90:
        return lambda x: (x < max_lat or x > min_lat + 180)
    else:
        return lambda x: (x < max_lat - 180 or x > min_lat)


def _lng_bounds(lat, lng, radius_m):
    # Approx length in metres of a degree of longitude at this latitude
    length_lng = math.cos(math.radians(lat)) * 111.32
    d_lng = radius_m / length_lng
    min_lng = lng - d_lng
    max_lng = lng + d_lng
    if min_lng >= -180 and max_lng <= 180:
        return lambda x: (min_lng < x < max_lng)
    elif min_lng < -180:
        return lambda x: (x < max_lng or x > min_lng + 360)
    else:
        return lambda x: (x < max_lng - 360 or x > min_lng)
