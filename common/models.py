import os
from Crypto.PublicKey import DSA
from Crypto.Cipher import AES
from Crypto.Hash import RIPEMD160, SHA256

P_SIZE = 2048
PASSWORD_LENGTH = 16
ENCODING = 'utf-8'
SEPARATOR = b'\n+==============+\n'
CRLF = b'\r\n'
SAVE_DIR = 'addresses'

class ParseException(Exception):
    pass


class Blockchain:

    @staticmethod
    def parse(data):
        blockchain = Blockchain
        try:
            for block in data['blocks']:
                blockchain.add_block(Block.parse(block))
        except (KeyError, ParseException) as e:
            raise ParseException("Error while parsing blockchain %s" % (e))
        return blockchain


    @staticmethod
    def serialize(blockchain):
        data = dict()
        blocks = blockchain.blocks
        data['blocks'] = []
        for block in blocks:
            data['blocks'].append(Block.serialize(block))
        return data

    def __init__(self, blocks = []):
        self.blocks = blocks

    def add_block(self,block):
        self.blocks.append(block)

    def part_of(self, start, end):
        if end != -1:
            blocks = self.blocks[start:end]
        else:
            block = self.blocks[start:]
        blockchain = Blockchain(blocks)
        return blockchain

    def add_blocks(self, blocks):
        self.blocks.extend(blocks)

    def __str__(self):
        return str(self.blocks)

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.blocks)

    def get_balance(self, address):
        balance = 0
        for block in self.blocks:
            for transaction in block.get_transactions():
                if Address.generate_address(transaction.sender_public_key) == address:
                    balance -= transaction.amount
                elif transaction.receiver == address:
                    balance += transaction.amount
        return balance

class Block:

    @staticmethod
    def parse(data):
        block = Block()
        try:
            block.header = data['header']
            block.nonce = data['nonce']
            for transaction in data['transactions']:
                block.add_transaction(Transaction.parse(transaction))
        except (KeyError, ParseException) as e:
            raise ParseException("Error while parsing block %s" % (e))
        return block

    @staticmethod
    def serialize(block):
        data = dict()
        data['header'] = block.header
        data['nonce'] = block.nonce
        transactions = block.transactions
        data['transactions'] = []
        for transaction in transactions:
            transactionDict = Transaction.serialize(transaction)
            data['transactions'].append(transactionDict)
        return data


    def __init__(self, header="", nonce=""):
        self.header = header
        self.nonce = nonce
        self.transactions = list()

    def get_transactions(self):
        return self.transactions

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_string_of_transactions(self):
        s = ""
        for transaction in self.transactions:
            s += transaction.toString()
        return s

class Transaction:

    @staticmethod
    def parse(data):
        transaction = Transaction()
        attrs = transaction.__dict__.keys()
        try:
            for attr in attrs:
                transaction.__dict__[attr] = data[attr]
        except KeyError as e:
            raise ParseException("Error while parsing transaction %s" % (e))
        return transaction

    @staticmethod
    def serialize(transaction):
        transactionDict = dict()
        transactionDict['receiver'] = transaction.receiver
        transactionDict['amount'] = transaction.amount
        transactionDict['hash'] = transaction.hash
        transactionDict['sender_public_key'] = transaction.sender_public_key
        transactionDict['signature'] = transaction.signature
        transactionDict['timestamp'] = transaction.timestamp
        return transactionDict

    def __init__(self, receiver=str(), amount=0,
                        timestamp=str(), sender_public_key=str()):
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp
        self.hash = str()
        self.sender_public_key = sender_public_key
        self.signature = str()

    def generate_hash(self):
        self.hash = SHA256.new(bytes(self.receiver, ENCODING) +
                                bytes(self.amount, ENCODING) +
                                bytes(str(self.timestamp), ENCODING) +
                                self.sender_public_key)

class Address:

    @staticmethod
    def generate_address(public_key):
        return RIPEMD160.new(public_key).hexdigest()

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
        address.raw = Address.generate_address(address.public_key)
        if address_label == '':
            address_label = address.raw
        address.label = address_label
        address.save(password)
        return address

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

    def to_string(self):
        return self.receiver + self.sender + str(self.amount) + self.hash + \
               self.sender_public_key + self.signature + self.timestamp
