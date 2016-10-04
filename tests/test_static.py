import pytest


@pytest.fixture(params=['/', '/map.css'])
def good_file(request):
    return request.param


@pytest.fixture(params=['/.', '/x.y', '/../client/index.html'])
def bad_file(request):
    return request.param


class TestStatic(object):
    def test_files(self, get, good_file):
        assert get(good_file).status_code == 200

    def test_404(self, get, bad_file):
        assert get(bad_file).status_code == 404
