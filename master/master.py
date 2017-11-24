
from common.models import Blockchain, Block, Transaction
import hashlib


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


    def verifyBlock(self,block): # Should we keep it here or outside the class or even in another file ?
        """
        Verify if the block data correspond to the current state of the blockchain
        
        lastBlock = self.blockchain.getLastBlock()
        previousHash = lastBlock.header
        nonce = block.nonce
        transactionsString = block.getStringOfTransactions()

        currentHash = hashlib.sha256(str.encode(previousHash + transactionsString + str(nonce)))
        if currentHash == block.header:
            pass
        else:
            isValid = False
        """
        # Waiting for Miner's team part
        # For test sake, let's say it's alrdy checked
        isValid = True

        return isValid
