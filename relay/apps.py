import logging
import sys

from django.apps import AppConfig
from django.conf import settings

from common import client
from common.models import Blockchain
from relay.relay import Relay

log = logging.getLogger(__name__)


class RelayConfig(AppConfig):
    name = 'relay'

    def ready(self):
        log.debug("Initializing relay server by getting blockchain from master")
        user = settings.RELAY_CREDENTIALS['username']
        pwd = settings.RELAY_CREDENTIALS['password']
        server = Relay()
        try:
            response = client.get(settings.MASTER_IP, "blockchain", basic_auth=(user, pwd))
        except ConnectionError:
            print("Error: MasterNode is not running at '%s' (check settings file)." % settings.MASTER_IP)
            sys.exit(1)
        server.blockchain = Blockchain.parse(response.data)
