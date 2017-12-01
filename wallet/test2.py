import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from common.models import Address
from wallet import Wallet
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS

PW = 'MasterPassworddd'
PW2 = "CryptoPassworddd"
PW3 = "RtosPassworddddd"
PW4 = "CompilingPasswor"
PW5 = "ComputabilityPwd"
PW6 = "DatabasePassword"
LABEL = "MasterAddress"
LABEL2 = "CrypoAddress"
LABEL3 = "RtosAddress"
LABEL4 = "CompilingAddress"
LABEL5 = "ComputabilityAddress"
LABEL6 = "DatabaseAddress"

def main():

    # Creating and loading tests
    ad = Address.create(PW, LABEL)
    ad = Address.create(PW2, LABEL2)
    ad = Address.create(PW3, LABEL3)
    ad = Address.create(PW4, LABEL4)
    ad = Address.create(PW5, LABEL5)
    ad = Address.create(PW6, LABEL6)


def verify_signature(transaction):
    verifier = DSS.new(DSA.import_key(transaction.sender_public_key), 'fips-186-3')
    try:
        verifier.verify(transaction.hash, transaction.signature)
        print('Correct signature')
    except ValueError:
        print('Incorrect signature')

if __name__=='__main__':
    main()
