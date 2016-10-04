import csv
from operator import attrgetter


class ShopData:
    def __init__(self, data_path_f):
        print("Loading data")
        self.shops = self._get_shops(data_path_f('shops.csv'))
        self.products = sorted(self._get_products(data_path_f('products.csv')), key=attrgetter('popularity'),
                               reverse=True)

    def _get_shops(self, filename):
        with open(filename, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            assert next(reader) == ['id', 'name', 'lat', 'lng']
            return {_id: shop for _id, shop in self._generate_shops(reader)}

    def _get_products(self, filename):
        with open(filename, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            assert next(reader) == ['id', 'shop_id', 'title', 'popularity', 'quantity']
            return [p for p in self._generate_products(reader, self.shops)]

    def _generate_shops(self, csv_reader):
        for row in csv_reader:
            yield row[0], Shop(*row[1:])

    def _generate_products(self, csv_reader, shops):
        for row in csv_reader:
            yield Product(shops, *row)


class Shop(object):
    __slots__ = 'name', 'lat', 'lng'

    def __init__(self, name, lat, lng):
        self.name, self.lat, self.lng = name, float(lat), float(lng)


class Product(object):
    __slots__ = 'id', 'shop', 'title', 'popularity', 'quantity'

    def __init__(self, shop_lookup, _id, shop_id, title, popularity, quantity):
        self.id, self.title, self.popularity, self.quantity = _id, title, float(popularity), int(quantity)
        self.shop = shop_lookup[shop_id]
