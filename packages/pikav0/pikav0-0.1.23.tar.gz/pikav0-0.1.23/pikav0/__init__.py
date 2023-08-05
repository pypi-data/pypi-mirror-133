__version__ = '0.12.0'

import logging
from logging import NullHandler

# Add NullHandler to prevent logging warnings
logging.getLogger(__name__).addHandler(NullHandler())

from pikav0.connection import ConnectionParameters
from pikav0.connection import URLParameters
from pikav0.connection import SSLOptions
from pikav0.credentials import PlainCredentials
from pikav0.spec import BasicProperties

from pikav0.adapters import BaseConnection
from pikav0.adapters import BlockingConnection
from pikav0.adapters import SelectConnection
from pikav0.adapters import TornadoConnection
from pikav0.adapters import TwistedConnection
