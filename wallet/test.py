from wallet import Address, Wallet
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
    print(ad.public_key)
    print(ad.raw)
    print(ad_b.public_key)
    print(ad_b.raw)

    # Wallet tests
    wallet = Wallet()
    wallet.sign_up(PW2, LABEL2)
    print(wallet.current_address.label)
    wallet2 = Wallet()
    wallet2.log_in(PW2, LABEL2)
    print(wallet2.current_address.label)

    # Transaction test
    transaction = wallet.create_transaction(ad.raw, 20)
    print('Receiver: {0} ; Amount: {1} ; Signature: {2}'.format(transaction.receiver, transaction.amount, transaction.signature))

    # Signature verification example (and therefore test)
    verify_signature(transaction)

    transaction.sender_public_key = ad.public_key # Changing the public key so signature shouldn't be correct
    verify_signature(transaction)


def verify_signature(transaction):
    verifier = DSS.new(DSA.import_key(transaction.sender_public_key), 'fips-186-3')
    try:
        verifier.verify(transaction.hash, transaction.signature)
        print('Correct signature')
    except ValueError:
        print('Incorrect signature')

if __name__=='__main__':
    main()