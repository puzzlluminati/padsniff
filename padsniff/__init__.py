import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

from .proxy import Proxy, on