import logging
from pathlib import Path

from mitmproxy.controller import handler as flow_handler
from mitmproxy.master import Master as FlowMaster
from mitmproxy.options import Options
from mitmproxy.proxy import ProxyConfig, ProxyServer

from .certs import generate_cert_files
from .constants import ALL, CADIR, DEFAULT_ORG, GUNGHO_API_ENDPOINT, GUNGHO_USER_AGENT
from .structures import CaseInsensitiveDefaultDict
from .parallel import parallelize


log = logging.getLogger(__name__)


class BaseProxy(FlowMaster):


    def __init__(self, **options):
        opts = Options(**options)
        server = ProxyServer(ProxyConfig(opts))
        super().__init__(opts, server)


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

    def __init__(self, host='0.0.0.0', port=8080, *, cadir=CADIR):
        # generate certs before initializing to avoid mitmproxy's default cert generation
        # if the specified directory doesn't exist
        generate_cert_files(cadir)

        # expanding the directory path prevents mitmproxy from treating directory paths
        # not suffixed with a `/` as files, thanks to os.path.dirname, and regenerating
        # certs when it can't find them in the specified directory's parent directory
        cadir = Path(cadir).expanduser().resolve()
        logging.info('Using certificate from %s.', cadir)

        super().__init__(listen_host=host, listen_port=port, cadir=str(cadir), mode='transparent')

        self.handlers = type(self).handlers.copy()


    @flow_handler
    def response(self, flow):
        request = flow.request

        log.debug('Received response from %s request to %s.', request.method, request.pretty_url)

        if is_gungho(request):
            log.info('Captured %s request to %s. Forwarding flow to routing.', request.method, request.pretty_url)
            self.route(flow)


    def on(self, action, *, blocking=False):
        """
        Register a function to be called when a response is received from a request to `action`.

        The function will be called with the request and response. The response will not be received by the client
        until the decorated function returns.

        Read about possible actions on the padsniff wiki: https://bitbucket.org/necromanteion/padsniff/wiki/Home
        """
        def wrapper(func):
            self.handlers[action].add(func if blocking else parallelize(func))
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


def on(action, *, blocking=False, cls=Proxy):
    """
    Register a function to be called when a response is received from a request to `action`.

    This is a shortcut for `Proxy.on`, useful for registering functions before instantiating
    a `Proxy` object.
    """
    return cls.on(cls, action, blocking=blocking)


def patch_mitmproxy_certfile_prefix():
    """
    Patch mitmproxy to search for certificates prefixed with 'padsniff' instead of 'mitmproxy'.

    Unfortunately this isn't parameterized in mitmproxy. See:
    https://github.com/mitmproxy/mitmproxy/blob/3d4d580975731215d58a629755e94b5913e67dc3/mitmproxy/proxy/config.py#L95-L98
    """
    import mitmproxy.proxy.config
    mitmproxy.proxy.config.CONF_BASENAME = DEFAULT_ORG
