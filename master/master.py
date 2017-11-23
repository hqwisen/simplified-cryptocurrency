
from common.models import Blockchain

class Master:
    """
    Singleton class which will containt the blockchain
    """
    master = None

    @staticmethod
    def init_master():
        """
        Initialize the master serverapp
        :return: the created Master instance
        """
        print("Init master")
        Master.master = Master()

        return Master.master

    def __init__(self):
        self.blockchain = Blockchain()

    def add_block_in_blockchain(self,block):
        self.blockchain.add_block(block)
