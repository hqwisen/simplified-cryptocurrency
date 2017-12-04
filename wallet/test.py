import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from common.models import Address, Transaction
from wallet import Wallet
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS

PW = 'aaaaaaaaaaaaaaaa'
PW2 = 'tttttttttttttttt'
LABEL = 'address1'
LABEL2 = 'address2'

def main():

    # Creating and loading tests
    ad = Address.create(PW, LABEL)
    ad_b = Address.load(PW, LABEL)
    print(ad.public_key == ad_b.public_key)
    print(ad.raw == ad_b.raw)

    # Wallet tests
    wallet = Wallet()
    wallet.sign_up(PW2, LABEL2)
    print(wallet.current_address.label)
    wallet2 = Wallet()
    wallet2.log_in(PW2, LABEL2)
    print(wallet2.current_address.label)

    # Transaction test
    transaction = wallet.create_transaction(ad.raw, 20)
    print('\tReceiver: {0}\n\tAmount: {1}\n\tSignature: {2}\n\t Timestamp: {3}'.format(transaction.receiver, transaction.amount, transaction.signature, transaction.timestamp))
    
    # Signature verification example (and therefore test)
    verify_signature(transaction)
    transaction2 = Transaction.parse(Transaction.serialize(transaction))

    transaction.sender_public_key = ad.public_key # Changing the public key so signature shouldn't be correct
    verify_signature(transaction)
    print("TX2 verify", transaction2.verify_signature())
    # verify_signature(transaction2)


def verify_signature(transaction):
    verifier = DSS.new(DSA.import_key(transaction.sender_public_key), 'fips-186-3')
    try:
        verifier.verify(transaction.get_hash(), transaction.signature)
        print('Correct signature')
    except ValueError:
        print('Incorrect signature')

if __name__=='__main__':
    main()