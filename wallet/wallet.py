import Crypto.PublicKey.DSA as DSA
import Crypto.Cipher.AES as AES
import hashlib

P_SIZE = 2048
RIPEMD160 = 'ripemd160'
PASSWORD_LENGTH = 16
ENCODING = 'utf-8'
SEPARATOR = b'\n+==============+\n'
CRLF = b'\r\n'

class Address:

    def __init__(self):
        self.public_key = None
        self.private_key = None
        self.raw = None
        self.label = None

    def save(self, password):
        with open(self.label,'wb') as f:
            keys = self.public_key + SEPARATOR + self.private_key
            cipher = AES.new(bytes(password, ENCODING), AES.MODE_EAX)
            cipher_text = cipher.encrypt(keys)
            f.write(cipher.nonce+CRLF)
            f.write(cipher_text)

    @staticmethod
    def load(password, label):
        with open(label,'rb') as f:
            address = Address()
            nonce = f.readline().strip(CRLF)
            cipher_text = b''.join(f.readlines())
            cipher = AES.new(bytes(password, ENCODING), AES.MODE_EAX, nonce)
            keys = cipher.decrypt(cipher_text).split(SEPARATOR)
            address.label = label
            address.public_key = keys[0]
            address.private_key = keys[0]
            return address

    @staticmethod
    def create(password, address_label=''):
        if len(bytes(password, ENCODING)) != PASSWORD_LENGTH:
            return None
        address = Address()
        new_key = DSA.generate(P_SIZE)
        address.public_key = new_key.publickey().exportKey()
        address.private_key = new_key.exportKey()
        hasher = hashlib.new(RIPEMD160)
        hasher.update(address.public_key)
        address.raw = hasher.hexdigest()
        if address_label == '':
            address_label = address.raw
        address.label = address_label
        address.save(password)
        return address
