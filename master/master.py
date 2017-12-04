import hashlib

from django.conf import settings

from common.models import Block, Address
from common.server import Server
from wallet.wallet import Wallet
import json

import logging

log = logging.getLogger(__name__)


class Master:
    class __Master(Server):
        def __init__(self):
            super(Master.__Master, self).__init__()
            self.balance = settings.MASTER_BALANCE
            self.wallet = Wallet()
            self.wallet.log_in(settings.MASTER_PASSWORD, settings.MASTER_LABEL, settings.MASTER_ADDRESS_DIRECTORY)
            self.hardcoded_genesis_block()
            # self.add_genesis_block()

        def hardcoded_genesis_block(self):
            log.debug("Initializing genesis block (from file %s)" % settings.GENESIS_BLOCK_FILE)
            with open(settings.GENESIS_BLOCK_FILE, 'r') as f:
                data = json.load(f)
            self.add_block(Block.parse(data))

        def add_genesis_block(self):
            addresses = settings.FIRST_ADDRESSES
            addresses_size = len(addresses)
            block = Block()
            for i in range(5):  # create the first 5 transactions
                destination_address = addresses[i % addresses_size]  # if there's less than 5
                new_transaction = self.wallet.create_transaction(destination_address, settings.FIRST_BALANCE)

                block.add_transaction(new_transaction)

            transactions_string = block.get_string_of_transactions()
            nonce = 0
            found = False
            while not found:  # hashing
                hash_object = hashlib.sha256(
                    str.encode(transactions_string + str(nonce)))  # b allows to concert string to binary
                block_header = hash_object.hexdigest()
                if block_header[:settings.DIFFICULTY] == "0" * settings.DIFFICULTY:
                    found = True
                else:
                    nonce += 1
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

    def __setattr__(self, name, value):
        setattr(self.instance, name, value)
