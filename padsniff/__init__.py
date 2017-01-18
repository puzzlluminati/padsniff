import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

from .proxy import (
    is_gungho,
    on,
    Proxy,
)
