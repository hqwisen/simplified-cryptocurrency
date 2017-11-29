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

    @property
    def blockchain(self):
        return self.__blockchain

    def add_blocks(self, blocks):
        self.blockchain.add_blocks(blocks)

    def verify_block(self, block):
        """
        Verify if the block data correspond to the current state of the blockchain.
        Verify that the hash of the new block match the current blockchain state.
        It does NOT verify the transaction of the block
        """
        is_valid = True
        # TODO implement verify hash
        return is_valid

    def blockchain_size(self):
        return len(self.blockchain)
