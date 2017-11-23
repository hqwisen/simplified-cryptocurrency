# -*- coding: utf-8 -*-
#
# Cryptographie : cryptocurrency
#
# authors : Huseyin Tektas - Yasin Arslan
#


import hashlib
#import sys
#sys.path.append('..')
#from common import models

class Miner:

	def __init__(self, ID):
		self.ID = ID 				# Identify the miner
		self.transactions = list()	# List of transaction object

	def startMining(self, difficulty):
		# request transactions
		# Verify transactions -- Signature + amount
		complete_hash, nonce = self.proofOfWork(difficulty)
		newBlock = self.createBlock(complete_hash, nonce)


	def proofOfWork(self, difficulty):
		"""
		Allow to verify the work of the miner. 
		It will check if the hash has a given number of 
		zeros determined by the difficulty at the start of string
		"""

		# mock - hash of the last block of the blockchain
		hashPrec = "fzf54zfz5ef4z6ef4ze5f4zef54ze5f46zef4z54f56zef"

		transactionsString = self.getStringOfTransactions()		# Plaintext will be self.transactions transformed 
		nonce = 0
		notFound = True

		while(notFound):
			hash_object = hashlib.sha256(str.encode(hashPrec + transactionsString + str(nonce))) # b allows to concert string to binary
			complete_hash = hash_object.hexdigest()
			print(complete_hash)
			if(self.isAcceptedByDifficulty(complete_hash, difficulty)):
				notFound = False
			else:
				nonce+=1


		return complete_hash, nonce

	def isAcceptedByDifficulty(self, hash, difficulty):
		firstCharac = hash[:difficulty]
		return firstCharac == "0" * difficulty

	def addTransaction(self, transaction):
		self.transactions.append(transaction)

	# Need all blockchain and change variable hashPrec
	# Need transactions
	def requestTransaction(self):
		pass

	def getStringOfTransactions(self):
		s=""
		for transaction in self.transactions:
			s+= transaction.toString()
		return s
	
	def createBlock(self, complete_hash, nonce):
		return Block(complete_hash, nonce, self.transactions)


# Only for testing
class Transaction():

	def __init__(self):
		self.txid = "eee"
		self.amount = 80
		self.receiver = "BB"
		self.sender = "AA"
		self.signature = "signature" 
		self.timestamp = "12/12/2012"

	def toString(self):
		return self.txid + str(self.amount) + self.receiver + self.sender + self.signature + self.timestamp

class Block():

	def __init__(self, header, nonce, transactions):
		self.header = header
		self.nonce = nonce
		self.transactions = transactions



if __name__ == "__main__":
	miner = Miner(555)
	miner.addTransaction(Transaction())
	miner.addTransaction(Transaction())
	miner.addTransaction(Transaction())
	miner.addTransaction(Transaction())
	miner.addTransaction(Transaction())

	miner.startMining(3)