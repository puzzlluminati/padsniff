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
        lookup_key = self._transform(key)
        self._dict[lookup_key] = (key, value)


    def __getitem__(self, key):
        lookup_key = self._transform(key)

        try:
            orig_key, value = self._dict[lookup_key]

        except KeyError:
            # call to __missing__ must be explicit because of overriding __getitem__
            value = self.__missing__(key)

        return value


    def __delitem__(self, key):
        lookup_key = self._transform(key)

        try:
            del self._dict[lookup_key]

        except KeyError:
            raise KeyError(key)


    def __iter__(self):
        return (orig_key for orig_key, value in self._dict.values())


    def __len__(self):
        return len(self._dict)


    def __contains__(self, key):
        # MutableMapping.__contains__ depends on __getitem__ raising a KeyError for missing keys
        # we have to override this behavior to prevent from always returning True unless default_factory is None
        return self._transform(key) in self._dict


    def __missing__(self, key):
        # emulate defaultdict's behavior is no default_factory is supplied
        if self.default_factory is None:
            raise KeyError(key)

        self[key] = self.default_factory()
        return self[key]


    def __repr__(self):
        rep = '{qualname}({default_factory}, {contents})'.format(
            qualname=self.__class__.__qualname__,
            default_factory=getattr(self.default_factory, '__qualname__', repr(self.default_factory)),
            contents=dict(self.items()),
        )

        return rep


    def copy(self):
        """Create a shallow copy of `self`."""
        cls = type(self)
        return cls(self.default_factory, self._dict.values())


    @classmethod
    def fromkeys(cls, default_factory, seq, value=None):
        """Create a new mapping with each key in `seq` set to `value`."""
        return cls(default_factory, dict.fromkeys(seq, value))


    def get(self, key, default=None):
        """
        Return the value associated with `key`, or `default` if `key` is not found.

        This method does not invoke the default factory.
        """
        lookup_key = self._transform(key)
        default_pair = (key, default)

        # _dict.get avoids __getitem__'s defaultdict-like behavior
        orig_key, value = self._dict.get(lookup_key, default_pair)

        return value


    def setdefault(self, key, default=None):
        """
        Return the value associated with `key`, setting it to `default` if `key` is not found.

        This method does not invoke the default factory.
        """
        lookup_key = self._transform(key)
        default_pair = (key, default)

        # _dict.setdefault avoids __getitems__'s defaultdict-like behavior
        orig_key, value = self._dict.setdefault(lookup_key, default_pair)

        return value
