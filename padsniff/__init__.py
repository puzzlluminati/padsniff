import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

from .parallel import parallelize
from .proxy import is_gungho, on, Proxy

__version__ = '1.1.1'
