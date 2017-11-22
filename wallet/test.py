from wallet import Address

PW = 'aaaaaaaaaaaaaaaa'
LABEL = 'address1'

def main():
    ad = Address.create(PW, LABEL)
    ad2 = Address.load(PW, LABEL)
    print(ad.public_key)
    print(ad2.public_key)
if __name__=='__main__':
    main()