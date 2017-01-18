from mitmproxy.controller import DummyReply
from mitmproxy.models import (
    ClientConnection,
    HTTPFlow,
    HTTPRequest,
    HTTPResponse,
    ServerConnection,
)
from netlib.tutils import (
    treq as TestRequest,
    tresp as TestResponse,
)
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
def req():
    test_request = TestRequest()
    return HTTPRequest.wrap(test_request)


@fixture
def resp():
    test_response = TestResponse()
    return HTTPResponse.wrap(test_response)


def client_connection():
    conn = ClientConnection.from_state(dict(
        address=dict(address=("address", 22), use_ipv6=True),
        clientcert=None,
        ssl_established=False,
        timestamp_start=1,
        timestamp_ssl_setup=2,
        timestamp_end=3,
    ))
    conn.reply = DummyReply()

    return conn


def server_connection():
    conn = ServerConnection.from_state(dict(
        address=dict(address=("address", 22), use_ipv6=True),
        source_address=dict(address=("address", 22), use_ipv6=True),
        ip_address=None,
        cert=None,
        timestamp_start=1,
        timestamp_tcp_setup=2,
        timestamp_ssl_setup=3,
        timestamp_end=4,
        ssl_established=False,
        sni="address",
        via=None
    ))
    conn.reply = DummyReply()

    return conn


@fixture
def flow(req, resp):
    f = HTTPFlow(client_connection(), server_connection())
    f.request = req
    f.response = resp
    f.reply = DummyReply()

    return f