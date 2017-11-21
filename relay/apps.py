from django.apps import AppConfig

from relay.relay import Relay


class RelayConfig(AppConfig):
    name = 'relay'

    def ready(self):
        Relay.init_relay()
