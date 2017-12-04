from django.apps import AppConfig
from django.conf import settings

from common import client
from common.models import Blockchain
from relay.relay import Relay


class RelayConfig(AppConfig):
    name = 'relay'

    def ready(self):
        server = Relay()
        response = client.get(settings.MASTER_IP, "blockchain")
        server.blockchain = Blockchain.parse(response.data)