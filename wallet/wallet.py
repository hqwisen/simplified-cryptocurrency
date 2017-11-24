from Crypto.PublicKey import DSA
from Crypto.Cipher import AES
from Crypto.Signature import DSS
from Crypto.Hash import RIPEMD160, SHA256
import os
import sys
sys.path.append(os.path.dirname(os.getcwd())) # Since wallet isn't a Django app, project dir must be added to import models
from common.models import Transaction

P_SIZE = 2048
PASSWORD_LENGTH = 16
ENCODING = 'utf-8'
SEPARATOR = b'\n+==============+\n'
CRLF = b'\r\n'
SAVE_DIR = 'addresses'
SIGNATURE_MODE = 'fips-186-3'

class Address:

    def __init__(self):
        self.public_key = None
        self.private_key = None
        self.raw = None
        self.label = None

    def save(self, password):
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        with open(os.path.join(SAVE_DIR, self.label),'wb') as f:
            keys = self.public_key + SEPARATOR + self.private_key
            cipher = AES.new(bytes(password, ENCODING), AES.MODE_EAX)
            cipher_text = cipher.encrypt(keys)
            f.write(bytes(self.raw, ENCODING)+CRLF)
            f.write(cipher.nonce+CRLF)
            f.write(cipher_text)

    @staticmethod
    def load(password, label):
        with open(os.path.join(SAVE_DIR, label),'rb') as f:
            address = Address()
            address.raw = f.readline().strip(CRLF).decode(ENCODING)
            nonce = f.readline().strip(CRLF)
            cipher_text = b''.join(f.readlines())
            cipher = AES.new(bytes(password, ENCODING), AES.MODE_EAX, nonce)
            keys = cipher.decrypt(cipher_text).split(SEPARATOR)
            address.label = label
            address.public_key = keys[0]
            address.private_key = keys[0]
            return address

    @staticmethod
    def create(password, address_label):
        if len(bytes(password, ENCODING)) != PASSWORD_LENGTH: #Pw must be of 16 bytes
            return None
        new_key = DSA.generate(P_SIZE)
        address = Address()
        address.private_key = new_key.exportKey()
        address.public_key = new_key.publickey().exportKey()
        address.raw = RIPEMD160.new(address.public_key).hexdigest()
        if address_label == '':
            address_label = address.raw
        address.label = address_label
        address.save(password)
        return address

class Wallet:

    def __init__(self):
        self.current_address = None

    def log_in(self, password, label):
        self.current_address = Address.load(password, label)

    def sign_up(self, password, address_label=''):
        self.current_address = Address.create(password, address_label)

    def create_transaction(self, destination_address, amount):
        new_transaction = Transaction()
        new_transaction.receiver = destination_address
        new_transaction.amount = amount
        new_transaction.sender = self.current_address.raw
        new_transaction.hash = SHA256.new(bytes(new_transaction.receiver, ENCODING) + bytes(new_transaction.sender, ENCODING) + bytes(new_transaction.amount, ENCODING))
        new_transaction.sender_public_key = self.current_address.public_key
        self.sign_transaction(new_transaction)
        return new_transaction

    def sign_transaction(self, transaction):
        signer = DSS.new(DSA.import_key(self.current_address.private_key), SIGNATURE_MODE)
        transaction.signature = signer.sign(transaction.hash)

