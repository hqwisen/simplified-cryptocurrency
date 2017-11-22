from django.apps import AppConfig

from relay.relay import Relay


class RelayConfig(AppConfig):
    name = 'relay'
    master_ip = "localhost:8000"