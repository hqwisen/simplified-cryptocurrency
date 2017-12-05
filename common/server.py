from common.models import Blockchain
from django.conf import settings

import logging
import hashlib

logger = logging.getLogger(__name__)

class Server:
    """
    Basic class implementing a server node that handle
    the blockchain.
    """

    def __init__(self):
        logger.debug("Intiazing server instance")
        self.__blockchain = Blockchain()

    def add_block(self, block):
        self.blockchain.add_block(block)

    def part_of(self, start, end):
        logger.debug("Requesting part of blockchain (%s, %s)" % (start, end))
        return self.blockchain.part_of(start, end)

    def add_blocks(self, blocks):
        self.blockchain.add_blocks(blocks)

    def verify_hash(self, block):
        """
        Verify if the block can be added at the end of the blockchain,
        Using the hashes of the last block, and the given block.
        It does NOT verify the transaction of the block.
        """
        last_block = self.blockchain.last_block()
        transactions_string = block.get_string_of_transactions()
        hash_object = hashlib.sha256(str.encode(
            last_block.header + transactions_string +
            str(block.nonce)))
        complete_hash = hash_object.hexdigest()
        return complete_hash == block.header and block.header[:settings.DIFFICULTY] == "0" * settings.DIFFICULTY

    @property
    def blockchain(self):
        return self.__blockchain

    @blockchain.setter
    def blockchain(self, blockchain):
        self.__blockchain = blockchain

    @property
    def blockchain_size(self):
        return len(self.blockchain)
