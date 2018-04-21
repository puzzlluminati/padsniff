import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

from .meta import version, revision
from .parallel import parallelize
from .proxy import is_gungho, on, Proxy
