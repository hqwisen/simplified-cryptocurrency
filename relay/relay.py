from common.models import Blockchain


class Relay:

    blockchain = Blockchain()

    @staticmethod
    def add_block(block):
        Relay.blockchain.add_block(block)

    @staticmethod
    def part_of(start, end):
        return Relay.blockchain.part_of(start, end)


    # @classmethod
    # def server(cls):
    #     if cls._server is None:
    #         _server = Relay()
    #     return _server
    # @staticmethod
    # def add_block(block):
    #     Relay._server.add_block(block)
    #
    # def __init__(self):
    #     self.transactions = []
    #     self.blockchain = Blockchain()
    #
    # def add_block(self, block):
    #     return self.blockchain.add_block(block)
