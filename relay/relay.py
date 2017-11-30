from common.models import Blockchain

import logging

from common.server import Server

logger = logging.getLogger(__name__)


class RelayError(Exception):
    pass


class Relay:
    class __Relay(Server):
        def __init__(self):
            super(Relay.__Relay, self).__init__()
            self.transactions = []

        def transaction_exists(self, transaction):
            for tr in self.transactions:
                if tr.hash == transaction.hash:
                    return True
            return False

        def add_transaction(self, transaction):
            if self.transaction_exists(transaction):
                raise RelayError("Transaction '%s' is already added." % transaction.hash)
            self.transactions.append(transaction)

        def get_transaction(self, exclude):
            for transaction in self.transactions:
                if transaction.hash not in exclude:
                    return transaction
            return None

        def update_blockchain(self, block):
            """
            Update the blockchain by adding the new block.
            If the block cannot be added to the blockchain,
            because the hashes do not fit, it returns False.
            Return True if everything went fine.
            :param block: block to be added
            :return: True if added, False otherwise.
            """
            is_valid = self.verify_hash(block)
            if is_valid:
                self.add_block(block)
                for transaction in block.transactions:
                    logger.debug("Start removal TX of %s" % transaction.hash)
                    self.remove_transaction(transaction)
            return is_valid

        def remove_transaction(self, transaction):
            """
            Remove transaction from the relay list.
            :param transaction: transaction to be removed
            :return: None
            """
            i = 0
            while i < len(self.transactions):
                if transaction.hash == self.transactions[i].hash:
                    logger.debug("Removing transaction %s" % self.transactions[i].hash)
                    del self.transactions[i]
                    i -= 1
                i += 1

    instance = None

    def __init__(self):
        if not Relay.instance:
            Relay.instance = Relay.__Relay()

    def __getattr__(self, name):
        return getattr(self.instance, name)
