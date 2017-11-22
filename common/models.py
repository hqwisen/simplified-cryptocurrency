class Blockchain:

    @staticmethod
    def parse(data):
        blockchain = Blockchain
        try:
            for block in data['blocks']:
                blockchain.add_block(Block.parse(block))
        except KeyError as e:
            raise Exception("Error while parsin %s" % (e))

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
            raise Exception("Error while parsing %s" % (e))
        return block

    @staticmethod
    def serialize(block):
        data = dict()
        data['header'] = block.header
        data['nonce'] = block.nonce
        transactions = block.transactions
        data['transactions'] = []
        for transaction in transactions:
            transactionDict = dict()
            transactionDict['txid'] = transaction.txid
            transactionDict['amount'] = transaction.amount
            transactionDict['receiver'] = transaction.receiver
            transactionDict['sender'] = transaction.sender
            transactionDict['block_hash'] = transaction.block_hash
            transactionDict['timestamp'] = transaction.timestamp

            data['transactions'].append(transactionDict)
        return data


    def __init__(self, header="", nonce=""):
        self.header = header
        self.nonce = nonce
        self.transactions = list()

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
            raise Exception("Error while parsing %s" % (e))
        return transaction

    def __init__(self):
        self.txid = str()
        self.amount = 0
        self.receiver = str()
        self.sender = str()
        self.block_hash = str()
        self.timestamp = str()
