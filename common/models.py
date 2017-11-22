
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

    def __init__(self):
        self.blocks = []

    def add_block(self,block):
        self.blocks.append(block)

    def part_of(self, start, end):
        blocks = self.blocks[start:end]
        blockchain = Blockchain()
        blockchain.blocks = blocks
        return blockchain

    def __str__(self):
        return str(self.blocks)

    def __repr__(self):
        return str(self)

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
        transactionDict['txid'] = transaction.txid
        transactionDict['amount'] = transaction.amount
        transactionDict['receiver'] = transaction.receiver
        transactionDict['sender'] = transaction.sender
        transactionDict['block_hash'] = transaction.block_hash
        transactionDict['timestamp'] = transaction.timestamp
        return transactionDict

    def __init__(self):
        self.txid = str()
        self.amount = 0
        self.receiver = str()
        self.sender = str()
        self.block_hash = str()
        self.timestamp = str()
