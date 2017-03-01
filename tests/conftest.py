from mitmproxy.test.tflow import tflow as TestFlow
from pytest import fixture
from pytest_mock import mocker


class MockSocket:
    """A Mock `socket.socket` to prevent opening connections."""

    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, method_name):
        # mock all method names to return called parameters
        # prevents sockets from binding and connecting
        return lambda *args, **kwargs: (args, kwargs)


@fixture(autouse=True)
def mock_proxy_server(monkeypatch):
    """Prevent networking libraries that use `socket.socket` from opening connections."""
    monkeypatch.setattr('socket.socket', MockSocket)


@fixture
def flow():
    return TestFlow()
