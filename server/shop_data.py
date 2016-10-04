import csv
from operator import attrgetter


class ShopData:
    def __init__(self, path_getter):
        """
        Load shop data into memory
        :param path_getter: A function taking a csv filename and returning a path
        """
        self.shops = self._get_shops(path_getter('shops.csv'))
        self._get_tags(path_getter('tags.csv'), path_getter('taggings.csv'))
        # Do the sorting by popularity once
        self.products = sorted(self._get_products(path_getter('products.csv')),
                               key=attrgetter('popularity'), reverse=True)

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

    def _get_tags(self, tags_file, taggings_file):
        tags_dict = None
        with open(tags_file, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            assert next(reader) == ['id', 'tag']
            tags_dict = {_id: tag for _id, tag in reader}

        with open(taggings_file, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            assert next(reader) == ['id', 'shop_id', 'tag_id']
            for _, shop_id, tag_id in reader:
                self.shops[shop_id].add_tag(tags_dict[tag_id])

    @staticmethod
    def _generate_shops(csv_reader):
        for row in csv_reader:
            yield row[0], Shop(*row[1:])

    @staticmethod
    def _generate_products(csv_reader, shops):
        for row in csv_reader:
            yield Product(shops, *row)


class Shop(object):
    __slots__ = 'name', 'lat', 'lng', '_tags'

    def __init__(self, name, lat, lng):
        self.name, self.lat, self.lng = name, float(lat), float(lng)
        self._tags = set()

    @property
    def tags(self):
        return self._tags

    def add_tag(self, t):
        self._tags.add(t)


class Product(object):
    __slots__ = 'id', 'shop', 'title', 'popularity', 'quantity'

    def __init__(self, shop_lookup, _id, shop_id, title, popularity, quantity):
        self.id, self.title, self.popularity, self.quantity = _id, title, float(popularity), int(quantity)
        self.shop = shop_lookup[shop_id]
