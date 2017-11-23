from wallet import Address

PW = 'aaaaaaaaaaaaaaaa'
LABEL = 'address1'

def main():
    ad = Address.create(PW, LABEL)
    ad2 = Address.load(PW, LABEL)
    print(ad.public_key)
    print(ad.raw)
    print(ad2.public_key)
    print(ad2.raw)
if __name__=='__main__':
    main()