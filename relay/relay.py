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
            added = super(Relay.__Relay, self).update_blockchain(block)
            if added:
                for transaction in block.get_transactions():
                    logger.debug("Start removal of %s" % transaction.hash)
                    self.remove_transaction(transaction)
            return added

        def remove_transaction(self, transaction):
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
