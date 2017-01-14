import logging

from mitmproxy.controller import handler as flow_handler
from mitmproxy.flow import FlowMaster, State
from mitmproxy.options import Options
from mitmproxy.proxy import ProxyConfig, ProxyServer

from .constants import ALL, GUNGHO_API_ENDPOINT, GUNGHO_USER_AGENT
from .structures import CaseInsensitiveDefaultDict


log = logging.getLogger(__name__)


class BaseProxy(FlowMaster):


    def __init__(self, **options):
        opts = Options(**options)
        server = ProxyServer(ProxyConfig(opts))
        super().__init__(opts, server, State())


    def run(self):
        try:
            logging.info('Starting proxy on port %s.', self.options.listen_port)
            super().run()
        except KeyboardInterrupt:
            pass
        finally:
            logging.info('Shutting down.')
            self.shutdown()


class Proxy(BaseProxy):

    handlers = CaseInsensitiveDefaultDict(set)

    def __init__(self, host='0.0.0.0', port=8080):
        super().__init__(listen_host=host, listen_port=port, mode='transparent')
        self.handlers = type(self).handlers.copy()


    @flow_handler
    def response(self, flow):
        request = flow.request

        log.debug('Received response from %s request to %s.', request.method, request.pretty_url)

        if is_gungho(request):
            log.info('Captured %s request to %s. Forwarding flow to routing.', request.method, request.pretty_url)
            self.route(flow)


    def on(self, action):
        """
        Register a function to be called when a response is received from a request to `action`.

        The function will be called with the request and response. The response will not be received by the client
        until the decorated function returns.

        Read about possible actions on the padsniff wiki: https://bitbucket.org/necromanteion/padsniff/wiki/Home
        """
        def wrapper(func):
            self.handlers[action].add(func)
            return func

        return wrapper


    def route(self, flow):
        """
        Route a flow's request and response to a handler function based on its action URL parameter.
        """
        request, response = flow.request, flow.response
        action = request.query.get('action')
        funcs = self.handlers[action] | self.handlers[ALL]

        for func in funcs:
            try:
                func(request, response)
            except:
                log.exception('Error while executing %s.', func.__name__)


def is_gungho(request):
    """Validate that `request` originated from a GungHo app."""
    return (request.headers.get('user-agent') == GUNGHO_USER_AGENT and
            request.path.startswith(GUNGHO_API_ENDPOINT))


def on(action, *, cls=Proxy):
    """
    Register a function to be called when a response is received from a request to `action`.

    This is a shortcut for `Proxy.on`, useful for registering functions before instantiating
    a `Proxy` object.
    """
    return cls.on(cls, action)
