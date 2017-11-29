from common.models import Blockchain


class Server:
    """
    Basic class implementing a server node that handle
    the blockchain.
    """

    def __init__(self):
        self.__blockchain = Blockchain()

    def add_block(self, block):
        self.blockchain.add_block(block)

    def part_of(self, start, end):
        return self.blockchain.part_of(start, end)


    def add_blocks(self, blocks):
        self.blockchain.add_blocks(blocks)

    def verify_hash(self, block):
        """
        Verify if the block can be added at the end of the blockchain,
        Using the hashes of the last block, and the given block.
        It does NOT verify the transaction of the block.
        """
        # TODO implement verify hash
        return True

    @property
    def blockchain(self):
        return self.__blockchain

    @property
    def blockchain_size(self):
        return len(self.blockchain)
