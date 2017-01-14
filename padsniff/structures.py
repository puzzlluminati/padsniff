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

        if default_factory is not None and not callable(default_factory):
            raise TypeError('default factory must be callable or None')

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
        rep = '{qualname}(default_factory, contents)'.format(
            qualname=self.__class__.__qualname__,
            default_factory=getattr(self.default_factory, '__qualname__', repr(self.default_factory)),
            contents=dict(self.items()),
        )

        return rep


    def copy(self):
        """Create a shallow copy of `self`."""
        cls = type(self)
        return cls(self.default_factory, self._dict.values())


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