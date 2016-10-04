import pytest

from server.geo import LatLng


@pytest.fixture(params=[(0, 0), (32.163213, -48.750002), (3.637690, -132.832035)])
def empty_lat_lng(request):
    return request.param


@pytest.fixture(params=[(-1000, 10), (100, 40), (0, -190)])
def invalid_lat_lng(request):
    return request.param


@pytest.fixture
def stockholm():
    return LatLng(59.3325800, 18.0649000)


class TestSearch(object):
    def test_empty(self, get, empty_lat_lng):
        url = '/search/{0}/{1}/10/1'.format(*empty_lat_lng)
        data = get(url).json
        assert 'products' in data
        assert len(data['products']) == 0

    def test_out_of_bounds(self, get, invalid_lat_lng):
        url = '/search/{0}/{1}/10/1'.format(*invalid_lat_lng)
        assert get(url).status_code == 400

    def test_many(self, get, stockholm):
        url = '/search/{0}/{1}/100/10'.format(*stockholm)
        data = get(url).json
        assert 'products' in data
        assert len(data['products']) == 10
