from common.server import Server
from common.models import Block, Blockchain, Address


class Master:
    class __Master(Server):
        def __init__(self):
            super(Master.__Master, self).__init__()

        def update_blockchain(self, block):
            """
            Add the block from the parameter if it's a valid one,
            otherwise reject it and return the bad transactions that
            made it invalid.
            """
            hash_verify = self.verify_hash(block)
            results = self.verify_transactions(block)
            if hash_verify and len(results) == 0:
                self.add_block(block)
                return []
            else:
                return results

        def verify_transactions(self, block):
            """
            Return a list of invalid transactions
            """
            # TODO write tests method to verify this.
            bad_transactions = []
            senders_balance = dict()
            for transaction in block.transactions:
                if transaction.verify_signature():
                    sender_address = Address.generate_address(transaction.sender_public_key)
                    if sender_address not in senders_balance:
                        senders_balance[sender_address] = self.blockchain.get_balance(sender_address)
                    if senders_balance[sender_address] >= transaction.amount:
                        senders_balance[sender_address] -= transaction.amount
                        if transaction.receiver not in senders_balance:
                            senders_balance[transaction.receiver] = self.blockchain.get_balance(transaction.receiver)
                        senders_balance[transaction.receiver] += transaction.amount
                    else:
                        bad_transactions.append(transaction)
                else:
                    bad_transactions.append(transaction)

            return bad_transactions

    instance = None

    def __init__(self):
        if not Master.instance:
            Master.instance = Master.__Master()

    def __getattr__(self, name):
        return getattr(self.instance, name)
