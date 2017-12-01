import os
from Crypto.PublicKey import DSA
from Crypto.Cipher import AES
from Crypto.Hash import RIPEMD160, SHA256
from Crypto.Signature import DSS

P_SIZE = 2048
PASSWORD_LENGTH = 16
ENCODING = 'utf-8'
SEPARATOR = b'\n+==============+\n'
CRLF = b'\r\n'
SAVE_DIR = 'addresses'
SIGNATURE_MODE = 'fips-186-3'


class ParseException(Exception):
    pass


class Blockchain:
    @staticmethod
    def parse(data):
        blockchain = Blockchain()
        try:
            for block in data['blocks']:
                blockchain.add_block(Block.parse(block))
        except KeyError as e:
            raise ParseException("Error: no 'blocks' given while"
                                 " parsing blockchain.")
        return blockchain

    @staticmethod
    def serialize(blockchain):
        data = dict()
        data['blocks'] = []
        for block in blockchain.blocks:
            data['blocks'].append(Block.serialize(block))
        return data

    def __init__(self, blocks=[]):
        self.__blocks = blocks

    def add_block(self, block):
        self.blocks.append(block)

    def part_of(self, start, end):
        """
        Return a part of the blockchain [start:end].
        if both start and end are None: return the full blockchain.
        If start = None: return from the beginning to end.
        If end = None: return from start to last element of the list.
        This method will return a shadow copy of the blockchain.
        :param start: start index of the blocks list or None.
        :param end: end index of the blocks list or None
        :return: Blockchain instance containing only the requested part.
        """
        if start is None and end is None:
            blocks = self.blocks
        elif start is None:
            blocks = self.blocks[:end]
        elif end is None:
            blocks = self.blocks[start:]
        else:
            blocks = self.blocks[start:end]
        return Blockchain(blocks)

    def add_blocks(self, blocks):
        """
        Extends the current blockchain with a list of blocks.
        :param blocks: list of blocks to add in the blockchain
        :return: None
        """
        self.blocks.extend(blocks)

    @property
    def blocks(self):
        return self.__blocks

    def __str__(self):
        return str(self.blocks)

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.blocks)

    def get_balance(self, address):
        balance = 0
        for block in self.blocks:
            for transaction in block.transactions:
                if Address.generate_address(transaction.get_sender_public_key()) == address:
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
        except KeyError as e:
            raise ParseException("Attribute %s was not given "
                                 "while parsing block." % (e))
        return block

    @staticmethod
    def serialize(block):
        data = dict()
        data['header'] = str(block.header)
        data['nonce'] = block.nonce
        data['transactions'] = []
        for transaction in block.transactions:
            transactionDict = Transaction.serialize(transaction)
            data['transactions'].append(transactionDict)
        return data

    def __init__(self, header="", nonce=""):
        self.__header = str(header)
        self.__nonce = nonce
        self.__transactions = list()

    @property
    def header(self):
        return self.__header

    @header.setter
    def header(self, header):
        self.__header = str(header)

    @property
    def nonce(self):
        return self.__nonce

    @nonce.setter
    def nonce(self, nonce):
        self.__nonce = nonce

    @property
    def transactions(self):
        return self.__transactions

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_string_of_transactions(self):
        s = ""
        for transaction in self.transactions:
            s += transaction.to_string()
        return s


class Transaction:
    @staticmethod
    def parse(data):
        transaction = Transaction()
        try:
            transaction.receiver = data['receiver']
            transaction.amount = data['amount']
            transaction.hash = data['hash']
            transaction.sender_public_key = data['sender_public_key']
            transaction.signature = data['signature']
            transaction.timestamp = data['timestamp']
        except KeyError as e:
            raise ParseException("Attribute %s was not given "
                                 "while parsing transaction." % (e))
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
        self.__receiver = receiver
        self.__amount = amount
        self.__timestamp = timestamp
        self.__hash = str()
        self.__sender_public_key = sender_public_key
        self.__signature = str()

    @property
    def receiver(self):
        return self.__receiver

    @receiver.setter
    def receiver(self, receiver):
        self.__receiver = receiver

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, amount):
        self.__amount = amount

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        self.__timestamp = timestamp

    @property
    def hash(self):
        return self.__hash

    @hash.setter
    def hash(self, hash):
        self.__hash = hash

    @property
    def sender_public_key(self):
        return self.__sender_public_key

    @sender_public_key.setter
    def sender_public_key(self, sender_public_key):
        self.__sender_public_key = sender_public_key

    @property
    def signature(self):
        return self.__signature

    @signature.setter
    def signature(self, signature):
        self.__signature = signature

    def generate_hash(self):
        self.hash = SHA256.new(bytes(self.receiver, ENCODING) +
                               bytes(str(self.amount), ENCODING) +
                               bytes(str(self.timestamp), ENCODING) +
                               self.sender_public_key)



    def verify_signature(self):
        try:
            verifier = DSS.new(DSA.import_key(self.sender_public_key), SIGNATURE_MODE)
            verifier.verify(self.hash, self.signature)
            return True
        except ValueError:
            return False



    def to_string(self):

        return self.receiver + str(self.amount) + str(self.hash) + \
               self.sender_public_key.__str__() +\
               self.signature.__str__() +\
               str(self.timestamp)

class Address:
    @staticmethod
    def generate_address(public_key):
        return RIPEMD160.new(public_key).hexdigest()

    @staticmethod
    def load(password, label, dir = SAVE_DIR):
        with open(os.path.join(dir, label), 'rb') as f:
            address = Address()
            address.raw = f.readline().strip(CRLF).decode(ENCODING)
            nonce = f.readline().strip(CRLF)
            cipher_text = b''.join(f.readlines())
            cipher = AES.new(bytes(password, ENCODING), AES.MODE_EAX, nonce)
            keys = cipher.decrypt(cipher_text).split(SEPARATOR)
            address.label = label
            address.public_key = keys[0]
            if Address.generate_address(address.public_key) != address.raw:
                return None
            address.private_key = keys[1]
            return address

    @staticmethod
    def create(password, address_label):
        if len(bytes(password, ENCODING)) != PASSWORD_LENGTH:  # Pw must be of 16 bytes
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
        with open(os.path.join(SAVE_DIR, self.label), 'wb') as f:
            keys = self.public_key + SEPARATOR + self.private_key
            cipher = AES.new(bytes(password, ENCODING), AES.MODE_EAX)
            cipher_text = cipher.encrypt(keys)
            f.write(bytes(self.raw, ENCODING) + CRLF)
            f.write(cipher.nonce + CRLF)
            f.write(cipher_text)
