from flask.json import JSONEncoder


def extend_json(cls):
    """
    Extends the JSONEncoder class with __slots__ support
    :param cls: base JSONEncoder
    :return:
    """
    class DataSlotsEncoder(cls):
        """
        JSON encodes objects defined with __slots__ instead of dict
        """
        def default(self, o):
            if hasattr(o, '__slots__'):
                return {key: self._encode_slots(getattr(o, key)) for key in o.__slots__ if key[0] != '_'}

            return super(DataSlotsEncoder, self).default(o)

        def _encode_slots(self, o):
            return self.default(o) if hasattr(o, '__slots__') else o

    return DataSlotsEncoder
