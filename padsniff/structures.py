from collections.abc import MutableMapping


class CaseInsensitiveDefaultDict(MutableMapping):
    """
    A mashup of a case-insensitive keyed dict and collections.defaultdict.

    Write an example for me!
    """


    @staticmethod
    def _transform(key):
        """Supports non-string keys."""

        try:
            return key.casefold()

        except AttributeError:
            return key


    def __init__(self, default_factory, data=None, **kwargs):
        self._dict = {}

        self.default_factory = default_factory

        if data is None:
            data = {}

        self.update(data, **kwargs)


    def __setitem__(self, key, value):
        self._dict[self._transform(key)] = (key, value)


    def __getitem__(self, key):
        try:
            origkey, value = self._dict[self._transform(key)]

        except KeyError:
            # call to __missing__ must be explicit because of overloading __getitem__
            value = self.__missing__(key)

        return value


    def __delitem__(self, key):
        del self._dict[self._transform(key)]


    def __iter__(self):
        return (origkey for origkey, value in self._dict.values())


    def __len__(self):
        return len(self._dict)


    def __missing__(self, key):
        # emulate defaultdict's behavior is no default_factory is supplied
        if self.default_factory is None:
            raise KeyError(key)

        self[key] = self.default_factory()
        return self[key]


    def __repr__(self):
        line = '{0.__class__.__qualname__}('
        line += (repr(None) if self.default_factory is None
                 else '{0.default_factory.__qualname__}')
        line += ', {1})'
        return line.format(self, dict(self.items()))


    def copy(self):
        return CaseInsensitiveDefaultDict(self.default_factory, self._dict.values())


    def get(self, key, default=None):

        try:
            # _dict.get avoids __getitem__'s defaultdict-like behavior
            origkey, value = self._dict.get(self._transform(key))

        except TypeError:
            value = default

        return value


    @classmethod
    def fromkeys(cls, default_factory, seq, value=None):
        return cls(default_factory, dict.fromkeys(seq, value))