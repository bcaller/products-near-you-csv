from server.geo import query_bounds_tester


class TestGeo(object):

    def test_normal(self):
        a = (10.0, 10.0)
        b = 111. * 5
        assert query_bounds_tester(a[0], a[1], b)(8, 9)
        assert query_bounds_tester(a[0], a[1], b)(14.99, 14.99)
        assert query_bounds_tester(a[0], a[1], b)(14.99, 5.01)

    def test_border_lng(self):
        offset = 111. * 5
        a = (10.0, -179.0)
        b = (11, -175)
        c = (11, 177)
        assert query_bounds_tester(a[0], a[1], offset)(*b)
        assert query_bounds_tester(b[0], b[1], offset)(*a)
        assert query_bounds_tester(a[0], a[1], offset)(*c)
        assert query_bounds_tester(c[0], c[1], offset)(*a)
        assert not query_bounds_tester(b[0], b[1], offset)(*c)

    def test_border_lat(self):
        offset = 1110.
        a = (-84, 10.0)
        b = (-75, 10.0)
        c = (88, 10.0)
        assert query_bounds_tester(a[0], a[1], offset)(*b)
        assert query_bounds_tester(b[0], b[1], offset)(*a)
        assert query_bounds_tester(a[0], a[1], offset)(*c)
        assert query_bounds_tester(c[0], c[1], offset)(*a)
        assert not query_bounds_tester(b[0], b[1], offset)(*c)
