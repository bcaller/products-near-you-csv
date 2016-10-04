import pytest
from flask import current_app


@pytest.fixture(params=[(0, 0), (32.163213, -48.750002), (3.637690, -132.832035)])
def empty_lat_lng(request):
    return request.param


@pytest.fixture(params=[(-1000, 10), (100, 40), (0, -190)])
def invalid_lat_lng(request):
    return request.param


@pytest.fixture
def stockholm():
    return 59.3325800, 18.0649000

@pytest.fixture(params=['jasdfljl', 'ksdgdfj,fgdflvj,sdgdsfl'])
def bad_tag(request):
    return request.param

@pytest.fixture(params=['shirts', 'cool'])
def good_tag(request):
    return request.param

@pytest.fixture(params=[3, 10, 54])
def n_results(request):
    return request.param


class TestSearch(object):
    def test_empty(self, get, empty_lat_lng):
        url = '/search/{0}/{1}/10/1'.format(*empty_lat_lng)
        data = get(url).json
        assert 'products' in data
        assert len(data['products']) == 0

    def test_massive_radius(self, get):
        # 100km away
        off_coast = (58.955674359706016, 19.6051025390625)
        url = '/search/{0}/{1}/100000/1'.format(*off_coast)
        data = get(url).json
        assert len(data['products']) == 1
        # 10km away
        url = '/search/{0}/{1}/10000/1'.format(*off_coast)
        data = get(url).json
        assert len(data['products']) == 0

    def test_out_of_bounds(self, get, invalid_lat_lng):
        url = '/search/{0}/{1}/10/1'.format(*invalid_lat_lng)
        assert get(url).status_code == 400

    def test_many(self, get, stockholm, n_results):
        url = '/search/{1}/{2}/100/{0}'.format(n_results, *stockholm)
        data = get(url).json
        assert 'products' in data
        assert len(data['products']) == n_results
        for p in data['products']:
            assert set(p.keys()) == {'id', 'popularity', 'quantity', 'shop', 'title'}
            assert set(p['shop'].keys()) == {'name', 'lat', 'lng'}
            assert isinstance(p['shop']['lat'], float)
            assert isinstance(p['shop']['lng'], float)
            assert isinstance(p['popularity'], float)
            assert isinstance(p['quantity'], int)
            assert isinstance(p['title'], unicode)

    def test_bad_tags(self, get, stockholm, bad_tag):
        url = '/search/{1}/{2}/100/10?tags={0}'.format(bad_tag, *stockholm)
        data = get(url).json
        assert 'products' in data
        assert len(data['products']) == 0

    def test_good_tags(self, get, stockholm, good_tag, n_results):
        url = '/search/{2}/{3}/100/{0}?tags={1}'.format(n_results, good_tag, *stockholm)
        data = get(url).json
        assert 'products' in data
        assert len(data['products']) == n_results
        for product in data['products']:
            shop = next(p.shop for p in current_app.data.products if p.id == product['id'])
            assert good_tag in shop.tags

    def test_multi_tags(self, get, stockholm, good_tag, bad_tag, n_results):
        url = '/search/{3}/{4}/100/{0}?tags={1},{2}'.format(n_results, good_tag, bad_tag, *stockholm)
        data = get(url).json
        assert 'products' in data
        assert len(data['products']) == n_results
        for product in data['products']:
            shop = next(p.shop for p in current_app.data.products if p.id == product['id'])
            assert good_tag in shop.tags

