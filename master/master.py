from common.server import Server
from common.models import Block, Blockchain


class Master:
    class __Master(Server):
        def __init__(self):
            super(Master.__Master, self).__init__()

        def update_blockchain(self, block):
            """
            Add the block from the parameter if it's a valid one,
            otherwise reject it and return the bad transactions that
            made it invalid
            """
            hash_verify = self.verify_block(block)
            results = self.verify_transactions(block)
            if hash_verify and len(results) == 0:
                self.add_block(block)
                return []
            else:
                return results

        def verify_transactions(block):
            """
            Return a list of invalid transactions
            """

            bad_transactions = []

            for transaction in block.get_transactions():
                sender_address = Address.generate_address(transaction.get_sender_public_key())
                if self.blockchain.get_balance(sender_address) < transaction.get_amount():
                    bad_transactions.append(transaction)
                elif not transaction.verify_signature():
                    bad_transactions.append(transaction)
            return bad_transactions





    instance = None

    def __init__(self):
        if not Master.instance:
            Master.instance = Master.__Master()

    def __getattr__(self, name):
        return getattr(self.instance, name)
