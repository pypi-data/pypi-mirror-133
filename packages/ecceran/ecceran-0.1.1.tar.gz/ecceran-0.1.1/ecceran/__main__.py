import os

from coincurve.keys import PrivateKey
from .utils import generate_key

from . import encrypt

def main():
    lock = '.private_key'

    if os.path.exists(lock):
        with open(lock, 'rb') as pk:
            private_key = PrivateKey(pk.read())
            print('public key :', private_key.public_key.format(True).hex())
            pk.close()


    else:
        with open(lock, 'wb+') as pk:
            private_key = generate_key()
            pk.write(private_key.secret)
            print('public key :', private_key.public_key.format(True).hex())
            pk.close()