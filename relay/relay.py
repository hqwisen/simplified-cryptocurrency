from common.models import Blockchain


class Relay:

    blockchain = Blockchain()
    transactions = []

    @staticmethod
    def add_block(block):
        Relay.blockchain.add_block(block)

    @staticmethod
    def part_of(start, end):
        return Relay.blockchain.part_of(start, end)

    @staticmethod
    def add_transaction(transaction):
        Relay.transactions.append(transaction)

    @staticmethod
    def get_transaction(exclude):
        for transaction in Relay.transactions:
            if transaction.txid not in exclude:
                return transaction
        return None

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
