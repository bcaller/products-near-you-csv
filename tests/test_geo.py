from server.geo import LatLng, in_query_box


class TestGeo(object):

    def test_normal(self):
        a = LatLng(10.0, 10.0)
        b = LatLng(5.0, 5.0)
        assert in_query_box(b, a, LatLng(8, 9))
        assert in_query_box(b, a, LatLng(14.99, 14.99))
        assert in_query_box(b, a, LatLng(14.99, 5.01))

    def test_border_lng(self):
        offset = LatLng(5.0, 5.0)
        a = LatLng(10.0, -179.0)
        b = LatLng(11, -175)
        c = LatLng(11, 177)
        assert in_query_box(offset, a, b)
        assert in_query_box(offset, b, a)
        assert in_query_box(offset, a, c)
        assert in_query_box(offset, c, a)
        assert not in_query_box(offset, b, c)

    def test_border_lat(self):
        offset = LatLng(10.0, 10.0)
        a = LatLng(-84, 10.0)
        b = LatLng(-75, 10.0)
        c = LatLng(88, 10.0)
        assert in_query_box(offset, a, b)
        assert in_query_box(offset, b, a)
        assert in_query_box(offset, a, c)
        assert in_query_box(offset, c, a)
        assert not in_query_box(offset, b, c)