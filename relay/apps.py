from django.apps import AppConfig
from django.conf import settings

from common import client
from common.models import Blockchain
from relay.relay import Relay
import logging

log = logging.getLogger(__name__)


class RelayConfig(AppConfig):
    name = 'relay'

    def ready(self):
        log.debug("Initializing relay server by getting blockchain from master")
        server = Relay()
        response = client.get(settings.MASTER_IP, "blockchain")
        server.blockchain = Blockchain.parse(response.data)
