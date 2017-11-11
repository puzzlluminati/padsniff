from unittest.mock import patch

from pytest import fixture

from padsniff import constants, is_gungho, on, parallelize, Proxy


@fixture(autouse=True)
def clear_Proxy_handlers():
    """Clear `Proxy.handlers` before each test case to prevent handlers from persisting."""
    Proxy.handlers.clear()


class TestProxy:


    def test_init(self):
        """Test initialization of Proxy instance with custom options."""
        host, port, cadir = '1.2.3.4', 12345, '~/.padsniff'

        with patch('padsniff.proxy.generate_cert_files') as mocked:
            proxy = Proxy(host=host, port=port, cadir=cadir)

        assert mocked.called_once_with(cadir)

        # test that parent class initializes with proper arguments
        assert proxy.options.listen_host == host
        assert proxy.options.listen_port == port
        assert proxy.options.mode == 'transparent'

        # test that the handlers are equivalent, but not the same reference
        assert proxy.handlers == Proxy.handlers
        assert proxy.handlers is not Proxy.handlers


    def test_inst_on_decorator(self, mocker):
        """Test basic functionality of the class-level on decorator."""
        endpoint = 'endpoint'
        proxy = Proxy()

        # test that instance decorator adds only to instance variable
        @proxy.on(endpoint, blocking=True)
        def func():
            pass

        assert func in proxy.handlers[endpoint]
        assert func not in Proxy.handlers[endpoint]

        # test that padsniff.parallel.parallelize is only called for blocking=False
        with mocker.patch('padsniff.parallel.parallelize') as mock:
            proxy.on(endpoint, blocking=True)(func)
            assert mock.not_called()

            proxy.on(endpoint, blocking=False)(func)
            assert mock.called_once_with(func)

        # test that decorated function is returned invariant
        assert proxy.on(endpoint, blocking=True)(func) is func
        assert proxy.on(endpoint, blocking=False)(func) is func


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
    """Test basic functionality of the module-level on decorator."""
    endpoint = 'endpoint'
    proxy = Proxy()

    # test that module-level decorator adds only to class variable
    @on(endpoint, blocking=True)
    def func():
        pass

    assert func in Proxy.handlers[endpoint]
    assert func not in proxy.handlers[endpoint]

    # test that padsniff.parallel.parallelize is only called for blocking=False
    with mocker.patch('padsniff.parallel.parallelize') as mock:
        on(endpoint, blocking=True)(func)
        assert mock.not_called(func)

        on(endpoint, blocking=False)(func)
        assert mock.called_once_with(func)

    # test that decorated function is returned invariant
    assert on(endpoint, blocking=True)(func) is func
    assert on(endpoint, blocking=False)(func) is func

    # test that an arbitrary class can be specified
    class NewProxy:
        on = mocker.Mock()

    on(endpoint, blocking=True, cls=NewProxy)

    assert NewProxy.on.called_once_with(endpoint, blocking=True)


def test_is_gungho(flow):
    flow.request.headers['user-agent'] = constants.GUNGHO_USER_AGENT
    flow.request.path = constants.GUNGHO_API_ENDPOINT
    assert is_gungho(flow.request)

    flow.request.headers['user-agent'] = 'PadsniffTesting'
    flow.request.path = constants.GUNGHO_API_ENDPOINT
    assert not is_gungho(flow.request)

    flow.request.headers['user-agent'] = constants.GUNGHO_USER_AGENT
    flow.request.path = '/path/to/success'
    assert not is_gungho(flow.request)

    flow.request.headers['user-agent'] = 'PadsniffTesting'
    flow.request.path = '/path/to/success'
    assert not is_gungho(flow.request)
