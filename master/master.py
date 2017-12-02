from common.server import Server
from common.models import Block, Blockchain, Address, Transaction, DSA, DSS, SIGNATURE_MODE
from django.conf import settings
from datetime import datetime
import hashlib



class Master:
    class __Master(Server):
        def __init__(self):
            super(Master.__Master, self).__init__()
            self.balance = settings.MASTER_BALANCE
            self.address = Address.load(settings.MASTER_PASSWORD,settings.MASTER_LABEL, settings.MASTER_ADDRESS_DIRECTORY)
            self.add_first_block()



        def add_first_block(self):
            addresses = settings.FIRST_ADDRESSES
            addresses_size = len(addresses)
            block = Block()
            for i in range(5):      #create the first 5 transactions
                destination_address = addresses[i%addresses_size]
                new_transaction = Transaction(destination_address, settings.FIRST_BALANCE, datetime.now().timestamp(),
                                                self.address.public_key)
                new_transaction.generate_hash()
                signer = DSS.new(DSA.import_key(self.address.private_key), SIGNATURE_MODE)
                new_transaction.signature = signer.sign(new_transaction.hash)
                x = new_transaction.signature.__str__()

                block.add_transaction(new_transaction)

            transactions_string = block.get_string_of_transactions()
            nonce = 0
            found = False
            while not found:  # hashing
                hash_object = hashlib.sha256(str.encode(transactions_string + str(nonce))) # b allows to concert string to binary
                block_header = hash_object.hexdigest()
                if block_header[:settings.DIFFICULTY] == "0" * settings.DIFFICULTY:
                    found = True
                else:
                    nonce += 1
            print(block_header)
            block.header = block_header
            block.nonce = nonce

            self.add_block(block)



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
