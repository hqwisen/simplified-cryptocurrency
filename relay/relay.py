from common.models import Blockchain


class Relay:

    _server = None

    @classmethod
    def server(cls):

        if cls._server is None:
            _server = Relay()
        return _server

    def __init__(self):
        self.transactions = []
        self.blockchain = Blockchain()
