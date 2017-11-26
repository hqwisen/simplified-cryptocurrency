
from common.models import Blockchain

class Master:
    """
    Singleton class which will contain the blockchain
    """

    blockchain = Blockchain()

    @classmethod
    def add_block(cls, block):
        cls.blockchain.add_block(block)
