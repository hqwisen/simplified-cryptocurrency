import os
import sys
sys.path.append(os.path.dirname(os.getcwd())) # Since wallet isn't a Django app, project dir must be added to import models
import requests
from datetime import datetime
from Crypto.Signature import DSS
import ast

from common.models import Transaction, Address, DSA, ENCODING, SIGNATURE_MODE, Blockchain

RELAY_PORT = 8000
RELAY_IP = "127.0.0.1"
BLOCKCHAIN_ENDPOINT = 'relay/blockchain'
ENCODING = 'utf-8'

class Wallet:

    def __init__(self):
        self.current_address = None
        self.blockchain = None

    def log_in(self, password, label):
        self.current_address = Address.load(password, label)
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
        self.blockchain = Blockchain.parse(ast.literal_eval(str(requests.get('http://{}:{}/{}'.format(RELAY_IP, RELAY_PORT, BLOCKCHAIN_ENDPOINT)).content, ENCODING)))