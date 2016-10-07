from mitmproxy.controller import handler as flow_handler
from mitmproxy.flow import FlowMaster, State
from mitmproxy.models import decoded
from mitmproxy.options import Options
from mitmproxy.proxy import ProxyConfig, ProxyServer

from .constants import GUNGHO_API_ENDPOINT, GUNGHO_USER_AGENT
from .structures import CaseInsensitiveDefaultDict


class BaseProxy(FlowMaster):


    def __init__(self, **options):
        opts = Options(**options)
        server = ProxyServer(ProxyConfig(opts))
        super().__init__(opts, server, State())


    def run(self):
        try:
            super().run()
        except KeyboardInterrupt:
            pass
        finally:
            self.shutdown()


class Proxy(BaseProxy):

    handlers = CaseInsensitiveDefaultDict(set)

    def __init__(self, host='0.0.0.0', port=8080):
        super().__init__(listen_host=host, listen_port=port, mode='transparent')
        self.handlers = Proxy.handlers.copy()


    @flow_handler
    def response(self, flow):
        request = flow.request

        if request.headers.get('user-agent') == GUNGHO_USER_AGENT and request.path.startswith(GUNGHO_API_ENDPOINT):
            self.route(flow)


    def on(self, action):
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
        funcs = self.handlers[action]

        for func in funcs:
            func(request, response)


def on(action, *, cls=Proxy):
    return cls.on(cls, action)