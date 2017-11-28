from common.models import Blockchain


class Server:

    def __init__(self):
        self.blockchain = Blockchain()

    def add_block(self, block):
        self.blockchain.add_block(block)

    def part_of(self, start, end):
        return self.blockchain.part_of(start, end)

    def get_blockchain(self):
        return self.blockchain

    def update_blockchain(self, block):
        """
        Update the blockchain by adding the new block
        if the block cannot be added, it will return false.
        :param block: the block to add
        :return: true if block added, false otherwise
        """
        is_valid = self.verify_block(block)
        if is_valid:
            self.add_block(block)
        return is_valid

    def verify_block(self, block):
        """
        Verify if the block data correspond to the current state of the blockchain.
        Verify that the hash of the new block match the current blockchain state.
        It does NOT verify the transaction of the block
        """
        is_valid = True
        # TODO implement verify hash
        return is_valid
