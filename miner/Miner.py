# -*- coding: utf-8 -*-
#
# Cryptographie : cryptocurrency
#
# authors : Huseyin Tektas - Yasin Arslan
#


import hashlib

class Miner:

	def __init__(self, ID):
		self.ID = ID 				# Identify the miner
		self.transactions = list()	# List of transaction object

	def proofOfWork(self, difficulty):
		"""
		Allow to verify the work of the miner. 
		It will check if the hash has a given number of 
		zeros determined by the difficulty at the start of string
		"""

		plaintext = "hahahha"		# Plaintext will be self.transactions transformed 
		nonce = 0
		notFound = True

		while(notFound):
			hash_object = hashlib.sha256(str.encode(plaintext + str(nonce))) # b allows to concert string to binary
			nonce +=1
			hex_hash = hash_object.hexdigest()
			print(hex_hash)
			if(self.isAcceptedByDifficulty(hex_hash, difficulty)):
				notFound = False


	def isAcceptedByDifficulty(self, hash, difficulty):
		firstCharac = hash[:difficulty]
		return firstCharac == "0" * difficulty


if __name__ == "__main__":
	miner = Miner(555)
	miner.proofOfWork(5)