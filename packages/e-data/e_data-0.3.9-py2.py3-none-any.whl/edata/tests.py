import sys
import logging
from .connectors import DatadisConnector
from .data import EdataError

_LOGGER = logging.getLogger ()

if len(sys.argv) != 3:
    _LOGGER.error ("Wrong parameters\nUsage: tests.py <USER> <PASSWD> <CUPS>")
    sys.exit (0)

api = DatadisConnector (sys.argv[0], sys.argv[1])

try:
    if not api.login():
        _LOGGER.error ("could not retrieve a valid token")
except Exception as e:
    _LOGGER.exception ("got exception %s", e)