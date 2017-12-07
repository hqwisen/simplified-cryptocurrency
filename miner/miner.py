# -*- coding: utf-8 -*-
#
# Cryptographie : cryptocurrency
#
# authors : Huseyin Tektas - Yasin Arslan
#


import hashlib
import json
import logging
import sys

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

sys.path.append('..')

from common.models import *
from common import client

CONFIG_FILE = "config.json"


class Miner:
    # Static variable which represent the mining difficulty
    DIFFICULTY = 5
    TX_PER_BLOCK = 5

    def __init__(self, address, relay_url):
        """

        :param address: address used to reward the miner.
        :param relay_url: url of the relay to request
        """
        self.address = address
        self.url = relay_url
        self.transactions = list()

    def get_blockchain(self):
        """
        :return: The blockchain received from the relay.
        """
        print("Getting blockchain")
        response = client.get(self.url, "blockchain")
        if response.status == 200:
            print("Blockchain successfully received")
        else:
            print("A problem occured while getting the blockchain from %s" % self.url)
        return Blockchain.parse(response.data)

    def get_transaction(self, excludes_list):
        """
        Get transaction from relay.
        :param excludes: TX hashes to be excluded on the request.
        :return: The transaction received if exist, otherwise None.
        """
        print("Requesting new transaction to %s" % self.url, end =": ")
        response = client.get(self.url, "transactions", {"exclude_hash": excludes_list})
        if response.status == 200:
            print("successfully received")
            return Transaction.parse(response.data)
        elif response.status == 404:
            print("no request to be received")
            return None
        else:
            print("unknown error")
            return None

    def add_transaction(self, transaction):
        print("New transaction added: %s" % transaction.hash)
        self.transactions.append(transaction)

    def reset_transaction(self):
        print("Reseting transactions list")
        self.transactions = []

    def sender_has_enough_balance(self, sender, amount, balance_dict):
        return balance_dict[sender] - amount >= 0

    def request_transactions(self, blockchain):
        """
        Requests TX_PER_BLOCK transactions from the relay.
        :return: The TX_PER_BLOCK transactions.
        """
        excludes_list, balance_dict = list(), dict()
        while len(self.transactions) < Miner.TX_PER_BLOCK:
            transaction = self.get_transaction(excludes_list)
            if transaction and transaction.verify_signature():
                balance_keys = balance_dict.keys()
                sender = Address.generate_address(transaction.sender_public_key)
                receiver, amount = transaction.receiver, transaction.amount
                if not (sender in balance_keys):
                    balance_dict[sender] = blockchain.get_balance(sender)
                if not (receiver in balance_keys):
                    balance_dict[receiver] = blockchain.get_balance(receiver)
                if self.sender_has_enough_balance(sender, amount, balance_dict):
                    balance_dict[sender] -= transaction.amount
                    balance_dict[receiver] += transaction.amount
                    self.add_transaction(transaction)
                excludes_list.append(transaction.hash)
        print("Received %s transactions" % Miner.TX_PER_BLOCK)

    def send_block(self, block):
        print("Sending block to relay %s" % self.url)
        data = {'block': Block.serialize(block),
                'miner_address': self.address}
        response = client.post(self.url, "block", data)
        print("Send block response %s" % response.status)

    def inner_start_mining(self):
        """
        Requests the 5 transactions, verifies them and proofOfWork with given difficulty.
        """
        print("Mining a new block")
        blockchain = self.get_blockchain()
        self.request_transactions(blockchain)
        last_block_hash = blockchain.last_block().header
        complete_hash, nonce = self.proof_of_work(last_block_hash)
        new_block = self.create_block(complete_hash, nonce)
        self.send_block(new_block)
        self.reset_transaction()

    def start_mining(self):
        mining = True
        while mining:
            try:
                self.inner_start_mining()
            except ConnectionError as e:
                # TODO maybe wait a few seconds before restarting the loop, instead of exit ?
                print("Error: connection error occured while requesting '%s'" % self.url)
                print(e)
                sys.exit(1)


    def proof_of_work(self, last_block_hash):
        """
        Allow to verify the work of the miner.
        It will check if the hash has a given number of
        zeros determined by the difficulty at the start of string.
        """
        transactions_string = self.get_string_of_transactions()  # Plaintext will be self.transactions transformed
        nonce = 0
        found = False
        print("Starting proof of work with difficulty %s" % Miner.DIFFICULTY)
        while not found:
            hash_object = hashlib.sha256(str.encode(
                last_block_hash + transactions_string + str(
                    nonce)))  # b allows to concert string to binary
            complete_hash = hash_object.hexdigest()

            if self.is_accepted_by_difficulty(complete_hash):
                found = True
            else:
                nonce += 1
        print("Hash found: '%s'" % complete_hash)
        return complete_hash, nonce

    def is_accepted_by_difficulty(self, hash):
        """
        Checks if difficulty is reached by given hash and difficulty
        """
        first_charac = hash[:Miner.DIFFICULTY]
        return first_charac == "0" * Miner.DIFFICULTY

    def get_string_of_transactions(self):
        """
        Creates string for the list of transactions
        """
        s = ""
        for transaction in self.transactions:
            s += transaction.to_string()
        return s

    def create_block(self, complete_hash, nonce):
        """
        Create and returns a block with given complete_hash and nonce
        """
        print("Creating block with hash: '%s'" % complete_hash)
        block = Block(complete_hash, nonce)
        for transaction in self.transactions:
            block.add_transaction(transaction)
        return block


def check_address(address):
    """
    Check if the address is a RIPEMD160 Hash.
    If the address is not correct, the script is aborted.
    The function only verify that the address is encoded
    in hexadecimal and contains 160 bits.
    :param address: address to be checked
    """
    try:
        int(address, 16)  # check if hex
        if (len(address) * 4) != 160: raise ValueError("Address is not 160 bits long.")
    except ValueError as e:
        print("Invalid address '%s'." % address)
        print(e)
        sys.exit(1)


def print_welcome():
    print("#" * 46)
    print("# Mining ULBCoin, Are you ready to be rich ? #")
    print("#" * 46)
    print("Quit the miner with CONTROL-C.")


def main():
    print_welcome()
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    address = config['address']
    relay_url = config['relay_url']
    check_address(address)
    miner = Miner(address, relay_url)
    miner.start_mining()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Mining stopped.")
