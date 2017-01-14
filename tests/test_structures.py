from padsniff.structures import CaseInsensitiveDefaultDict

import pytest


class TestCaseInsensitiveDefaultDict:


    def test_get_set_delitem(self):
        d = CaseInsensitiveDefaultDict(default_factory=None)
        key = 'key'
        value = object()

        d[key] = value

        assert d[key] is value

        del d[key]

        assert key not in d


    def test_contains(self):
        d = CaseInsensitiveDefaultDict(default_factory=None)
        key = 'key'

        assert key not in d

        d[key] = object()

        assert key in d


    def test_case_insensitivity(self):
        d = CaseInsensitiveDefaultDict(default_factory=None)
        key = 'KeY'
        d[key] = object()

        assert d[key] is d[key.upper()]
        assert d[key] is d[key.lower()]
        assert d[key] is d[key.casefold()]


    def test_original_capitalization(self):
        d = CaseInsensitiveDefaultDict(default_factory=None)
        key = 'KeY'
        d[key] = object()
        d_as_dict = dict(d)

        assert key in d_as_dict
        assert key.upper() not in d_as_dict
        assert key.lower() not in d_as_dict
        assert key.casefold() not in d_as_dict


    def test_key_transform(self):
        transform = CaseInsensitiveDefaultDict._transform

        assert transform('StRiNg') == 'string'
        assert transform(1) == 1
        assert transform(range(10)) == range(10)
        assert transform(set('AbC')) == set('AbC')

        obj = object()

        assert transform(obj) is obj


    def test_valid_default_factory(self, mocker):
        mock_default_factory = mocker.Mock()
        mock_default_factory.return_value = object()

        d = CaseInsensitiveDefaultDict(default_factory=mock_default_factory)
        key = 'key'

        assert d.default_factory is mock_default_factory
        assert d[key] == mock_default_factory.return_value
        assert mock_default_factory.called_once_with(key)


    def test_non_callable_default_factory(self):
        with pytest.raises(TypeError):
            CaseInsensitiveDefaultDict(default_factory=True)


    def test_no_default_factory(self):
        d = CaseInsensitiveDefaultDict(default_factory=None)
        key = 'key'

        assert d.default_factory is None
        assert key not in d

        with pytest.raises(KeyError):
            d[key]


    def test_repr(self):
        d = CaseInsensitiveDefaultDict(default_factory=int)
        assert repr(d) == 'CaseInsensitiveDefaultDict(int, {})'

        d.update(A=1)
        assert repr(d) == "CaseInsensitiveDefaultDict(int, {'A': 1})"


    def test_copy(self):
        d = CaseInsensitiveDefaultDict(default_factory=None, a=1, b=2, c=3)

        assert d == d.copy()


    def test_get(self, mocker):
        mock_default_factory = mocker.Mock()
        d = CaseInsensitiveDefaultDict(default_factory=mock_default_factory)
        key = 'key'
        obj = object()
        d[key] = obj

        assert d.get(key) is obj
        assert mock_default_factory.not_called()

        key2 = 'key2'
        obj2 = object()

        assert d.get(key2) is None
        assert d.get(key2, obj2) is obj2
        assert key2 not in d
        assert mock_default_factory.not_called()


    def test_setdefault(self, mocker):
        mock_default_factory = mocker.Mock()
        d = CaseInsensitiveDefaultDict(default_factory=mock_default_factory)
        key = 'key'
        obj = object()
        d[key] = obj

        assert d.setdefault(key) is obj
        assert mock_default_factory.not_called()

        key2 = 'key2'
        obj2 = object()

        assert d.setdefault(key2) is None
        assert d.setdefault(key2, obj2) is None
        assert key2 in d
        assert mock_default_factory.not_called()



    def test_fromkeys(self):
        obj = object()
        d = CaseInsensitiveDefaultDict.fromkeys(default_factory=None, seq='abc', value=obj)

        assert d.default_factory is None
        assert d == CaseInsensitiveDefaultDict(None, a=obj, b=obj, c=obj)
