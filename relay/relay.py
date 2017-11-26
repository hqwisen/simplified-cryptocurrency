from common.models import Blockchain

import logging

logger = logging.getLogger(__name__)

class RelayError(Exception):
    pass

class Relay:

    blockchain = Blockchain()
    transactions = []

    @classmethod
    def add_block(cls, block):
        cls.blockchain.add_block(block)

    @classmethod
    def part_of(cls, start, end):
        return cls.blockchain.part_of(start, end)

    @classmethod
    def transaction_exists(cls, transaction):
        for tr in cls.transactions:
            if tr.hash == transaction.hash:
                return True
        return False

    @classmethod
    def add_transaction(cls, transaction):
        if cls.transaction_exists(transaction):
            raise RelayError("Transaction '%s' is already added." % transaction.hash)
        cls.transactions.append(transaction)

    @classmethod
    def get_transaction(cls, exclude):
        for transaction in cls.transactions:
            if transaction.hash not in exclude:
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

    @classmethod
    def update_blockchain(cls, block):
        cls.blockchain.add_block(block)
        for transaction in block.get_transactions():
            logger.debug("Start removal of %s" % transaction.hash)
            cls.remove_transaction(transaction)

    @classmethod
    def remove_transaction(cls, transaction):
        i = 0
        while i < len(cls.transactions):
            if transaction.hash == cls.transactions[i].hash:
                logger.debug("Removing transaction %s" % cls.transactions[i].hash)
                del cls.transactions[i]
                i-=1
            i+=1

