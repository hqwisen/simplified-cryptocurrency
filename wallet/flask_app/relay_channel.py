import os
import sys
sys.path.append(os.path.dirname(os.getcwd())) # Since wallet isn't a Django app, project dir must be added to import models
import requests
import ast
from common.models import Transaction, Blockchain

RELAY_PORT = 8000
RELAY_IP = "127.0.0.1"
BLOCKCHAIN_ENDPOINT = 'relay/blockchain'
TRANSACTION_ENDPOINT = 'relay/transactions'

def relay_addr(endpoint) :
	return 'http://{}:{}/{}'.format(RELAY_IP, RELAY_PORT, endpoint)

def get_blockchain() :
	response = requests.get(relay_addr(BLOCKCHAIN_ENDPOINT))
	return Blockchain.parse(ast.literal_eval(response.text))

def send_transaction(transaction) :
	return requests.post(relay_addr(TRANSACTION_ENDPOINT), data=Transaction.serialize(transaction)).status_code