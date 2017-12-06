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

    def __init__(self, address, ip, port):
        self.address = address  # Identify the miner with an adress, this adress will be used for paiment by masternode
        self.transactions = list()  # List of transaction object
        self.ip = ip
        self.port = port
        self.url = "http://" + ip + ":" + str(port)

    def test(self):
        self.printStartMining()
        for i in range(5):
            self.printAddedNewTransaction()
        self.printSendBlock()

    def startMining(self):
        """
        Requests the 5 transactions, verifies them and proofOfWork with given difficulty
        """
        while (True):
            excludes = list()
            balanceDic = dict()
            responseBl = client.get(self.url + "/relay","blockchain")
            blockchain = Blockchain.parse(responseBl.data)
            self.printStartMining()
            while (len(self.transactions) < 5):
                transactionsToExclude = {"exclude_hash": excludes}
                responseTr = client.get(self.url + "/relay","transactions",transactionsToExclude)
                # If transaction is not empty ( None )
                if (responseTr.status == 200):
                    transaction = Transaction.parse(responseTr.data)
                    # VERIF SIGNATURE
                    if (transaction.verify_signature()):
                        balanceKeys = balanceDic.keys()
                        sender = Address.generate_address(transaction.sender_public_key)
                        receiver = transaction.receiver
                        amount = transaction.amount
                        print(amount)
                        # VERIF BALANCE
                        if not (sender in balanceKeys):
                            balanceDic[sender] = blockchain.get_balance(sender)
                        if not (receiver in balanceKeys):
                            balanceDic[receiver] = blockchain.get_balance(receiver)

                        if (self.senderHasEnoughBalance(sender, amount, balanceDic)):
                            balanceDic[sender] -= transaction.amount
                            balanceDic[receiver] += transaction.amount
                            self.transactions.append(transaction)
                            self.printAddedNewTransaction()
                    # Add this transaction to our excludes
                    excludes.append(transaction.hash)
            # Once we got all transactions and verifications done.
            # We can start PROOF OF WORK
            # part_of(start, end) , we only need last block's hash
            lastBlockchainHash = blockchain.last_block().header
            complete_hash, nonce = self.proofOfWork(lastBlockchainHash)
            newBlock = self.createBlock(complete_hash, nonce)
            ####################################################
            # Send block to relay
            # Create JSON with format of acceptance by relay. We give the address to get paid if block is accepted
            blockAndaddress = {'block': Block.serialize(newBlock),
                               'miner_address': self.address}
            client.post(self.url + "/relay", "block", blockAndaddress)
            self.printSendBlock()
            self.transactions = []

    def printStartMining(self):
        print("##\n## Starting new block")

    def printAddedNewTransaction(self):
        print("\t-> Added new Transaction")

    def printSendBlock(self):
        print("\t\t-> New block has been created and sent to Server")

    def senderHasEnoughBalance(self,sender, amount, balanceDic):
        return balanceDic.get(sender) - amount >= 0

    def proofOfWork(self, lastBlockchainHash):
        """
        Allow to verify the work of the miner.
        It will check if the hash has a given number of
        zeros determined by the difficulty at the start of string
        """

        transactionsString = self.getStringOfTransactions()  # Plaintext will be self.transactions transformed
        nonce = 0
        notFound = True

        while (notFound):
            hash_object = hashlib.sha256(str.encode(
                lastBlockchainHash + transactionsString + str(
                    nonce)))  # b allows to concert string to binary
            complete_hash = hash_object.hexdigest()

            if (self.isAcceptedByDifficulty(complete_hash)):
                print(complete_hash)
                notFound = False
            else:
                nonce += 1

        return complete_hash, nonce

    def isAcceptedByDifficulty(self, hash):
        """
        Checks if difficulty is reached by given hash and difficulty
        """
        firstCharac = hash[:Miner.DIFFICULTY]
        return firstCharac == "0" * Miner.DIFFICULTY

    def getStringOfTransactions(self):
        """
        Creates string for the list of transactions
        """
        s = ""
        for transaction in self.transactions:
            s += transaction.to_string()
        return s

    def createBlock(self, complete_hash, nonce):
        """
        Create and returns a Block with given complete_hash and nonce
        """
        block = Block(complete_hash, nonce)
        for transaction in self.transactions:
            block.add_transaction(transaction)
        return block

def printWelcome():
    print("#" *25)
    print("# Mining ULBCoin, Are you ready to be rich ?")
    print("#" *25)

def main():
    printWelcome()
    # TODO Maybe check if address exists in the blockchain.
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    address = config['address']
    ip, port = config['relay']['ip'], config['relay']['port']
    miner = Miner(address, ip, port)
    miner.startMining()

if __name__ == "__main__":
    main()