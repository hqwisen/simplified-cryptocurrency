# -*- coding: utf-8 -*-
#
# Cryptographie : cryptocurrency
#
# authors : Huseyin Tektas - Yasin Arslan
#


import hashlib
import sys

import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

sys.path.append('..')

from common.models import *
import requests


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
        self.startMining()

    def startMining(self):
        """
        Requests the 5 transactions, verifies them and proofOfWork with given difficulty
        """

        while (True):
            excludes = list()
            balanceDic = dict()
            responseBl = requests.get(self.url + "/relay/blockchain")
            blockchain = Blockchain.parse(responseBl.json())
            while (len(self.transactions) < 5):
                print("Taille trans : " , len(self.transactions))
                data = {"exclude_hash": excludes}
                responseTr = requests.get(self.url + "/relay/transactions",
                                          data)
                print(responseTr.json())
                # If transaction is not empty ( None )
                log.debug("Receive transaction %s " % responseTr.status_code)
                print("Receive transaction ", responseTr.status_code)
                if responseTr.status_code == 200:
                    balanceKeys = balanceDic.keys()
                    transaction = Transaction.parse(responseTr.json())
                    sender = Address.generate_address(
                        transaction.sender_public_key)
                    receiver = transaction.receiver

                    ####################################################
                    # VERIF SIGNATURE
                    print("transaction sign : " , transaction.signature)
                    print("transaction pkey : ", transaction.sender_public_key)
                    print("verif : ", transaction.verify_signature())
                    if (transaction.verify_signature()):
                        print("Signature ok")
                        # VERIF BALANCE
                        if not (sender in balanceKeys):
                            balanceDic[
                                sender] = blockchain.get_balance(
                                sender)
                        balanceDic[sender] -= transaction.amount
                        if not (receiver in balanceKeys):
                            balanceDic[
                                receiver] = blockchain.get_balance(
                                receiver)
                        balanceDic[receiver] += transaction.amount


                        if (balanceDic.get(sender) >= 0):
                            print("Balance ok")
                            self.transactions.append(transaction)
                        else:
                            balanceDic[transaction.sender] += transaction.amount
                            balanceDic[
                                transaction.receiver] -= transaction.amount
                    # Add this transaction to our excludes
                    excludes.append(transaction.hash)
                ####################################################

            # Once we got all transactions and verifications done.
            # We can start PROOF OF WORK
            # part_of(start, end) , we only need last block's hash
            lastBlockchainHash = blockchain.last_block().header
            complete_hash, nonce = self.proofOfWork(lastBlockchainHash)
            newBlock = self.createBlock(complete_hash, nonce)
            log.debug("New block %s " % str(newBlock))
            print("New block", newBlock)
            print("Complet hash", complete_hash)
            ####################################################

            # Send block to relay
            # Create JSON with format of acceptance by relay. We give the address to get paid if block is accepted
            blockAndaddress = {'block': Block.serialize(newBlock),
                               'miner_address': self.address}
            requests.post(self.url + "/relay/block", blockAndaddress)

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


if __name__ == "__main__":
    # TODO
    # TODO
    # TODO Give legit address ip of relay
    miner = Miner('43463a5a6dea8cd80d616607ab73fa24f4943e3b', "localhost", 8001)
