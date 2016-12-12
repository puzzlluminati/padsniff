from padsniff import (
    constants,
    on,
    Proxy,
)

from pytest import fixture


@fixture(autouse=True)
def clear_Proxy_handlers():
    """Clear `Proxy.handlers` before each test case to prevent handlers from persisting."""
    Proxy.handlers.clear()


class TestProxy:


    def test_init(self):
        """Test initialization of Proxy instance with custom options."""
        host, port = '1.2.3.4', 12345
        proxy = Proxy(host=host, port=port)

        assert proxy.options.listen_host == host
        assert proxy.options.listen_port == port
        assert proxy.options.mode == 'transparent'
        assert proxy.handlers == Proxy.handlers


    def test_on_decorator(self):
        endpoint = 'endpoint'
        proxy = Proxy()

        assert not proxy.handlers[endpoint]

        @proxy.on(endpoint)
        def func():
            pass

        assert func in proxy.handlers[endpoint]
        assert func not in Proxy.handlers[endpoint]
        assert proxy.on('endpoint2')(func) is func


    def test_response_filtering(self, mocker, flow):
        """Test capturing only flows that match GungHo's user agent and endpoint URL."""
        route = mocker.patch('padsniff.proxy.Proxy.route')
        proxy = Proxy()

        flow.request.headers['user-agent'] = constants.GUNGHO_USER_AGENT
        flow.request.path = constants.GUNGHO_API_ENDPOINT
        proxy.response(flow)
        assert route.called_once_with(flow)

        route.reset_mock()
        flow.request.headers['user-agent'] = 'PadsniffTesting'
        flow.request.path = constants.GUNGHO_API_ENDPOINT
        proxy.response(flow)
        assert route.not_called()

        route.reset_mock()
        flow.request.headers['user-agent'] = constants.GUNGHO_USER_AGENT
        flow.request.path = '/path/to/success'
        proxy.response(flow)
        assert route.not_called()

        route.reset_mock()
        flow.request.headers['user-agent'] = 'PadsniffTesting'
        flow.request.path = '/path/to/success'
        proxy.response(flow)
        assert route.not_called()


    def test_flow_routing(self, mocker, flow):
        """Test routing flows to the correct handlers."""
        endpoint = 'endpoint1'
        func1 = mocker.Mock()
        func2 = mocker.Mock()
        proxy = Proxy()

        proxy.on(endpoint)(func1)
        proxy.on('endpoint2')(func2)

        flow.request.path = '%s?action=%s' % (constants.GUNGHO_API_ENDPOINT, endpoint)
        proxy.route(flow)

        assert func1.called_once_with(flow.request, flow.response)
        assert func2.not_called()


def test_on_decorator(mocker):
    endpoint = 'endpoint'
    proxy = Proxy()

    @on(endpoint)
    def func1():
        pass

    assert func1 in Proxy.handlers[endpoint]
    assert func1 not in proxy.handlers[endpoint]

    with mocker.patch('padsniff.proxy.Proxy.on') as mock:
        @on(endpoint)
        def func2():
            pass

        assert mock.called_once_with(Proxy, func2)
