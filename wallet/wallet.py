import os
import sys
sys.path.append(os.path.dirname(os.getcwd())) # Since wallet isn't a Django app, project dir must be added to import models
from datetime import datetime
from Crypto.Signature import DSS

from common.models import Transaction, Address, DSA, ENCODING, SIGNATURE_MODE, Blockchain

from pathlib import Path

my_file = Path("relay_channel.py")
if my_file.is_file(): # Client side
    from relay_channel import get_blockchain
else:   #MasterNode side
    from wallet.relay_channel import get_blockchain

class Wallet:

    def __init__(self):
        self.current_address = None
        self.blockchain = None

    def log_in(self, password, label, dir = None):
        if dir == None:
            self.current_address = Address.load(password, label)
        else:
            self.current_address = Address.load(password, label, dir)
        return self.current_address != None

    def log_out(self):
        self.current_address = None

    def sign_up(self, password, address_label=''):
        self.current_address = Address.create(password, address_label)

    def create_transaction(self, destination_address, amount):
        new_transaction = Transaction(destination_address, amount, datetime.now().timestamp(),
                                        self.current_address.public_key)
        new_transaction.generate_hash()
        self.sign_transaction(new_transaction)
        return new_transaction

    def sign_transaction(self, transaction):
        signer = DSS.new(DSA.import_key(self.current_address.private_key), SIGNATURE_MODE)
        transaction.signature = signer.sign(transaction.hash)

    def update_blockchain(self) :
        self.blockchain = get_blockchain()
