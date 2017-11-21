from django.apps import AppConfig
from master.master import Master


class MasterConfig(AppConfig):
    name = 'master'

    def ready(self):
        Master.init_master()
