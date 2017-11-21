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
        data = block.__dict__
        transactions = block.transactions
        data['transactions'] = []
        for transaction in transactions:
            data['transactions'].append(transaction.__dict__)
        return data


    def __init__(self):
        self.header = str()
        self.nonce = str()
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
