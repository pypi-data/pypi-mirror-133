from coincurve.keys import PublicKey

from .utils import aes_decrypt, aes_encrypt, decapsulate, encapsulate, generate_key, hex2prv, hex2pub

def encrypt(receiver_pk: str, msg: bytes):

    ephemeral_key = generate_key()
    if isinstance(receiver_pk, str):
        receiver_pubkey = hex2pub(receiver_pk)
    else:
        raise TypeError("Invalid public key type")

    aes_key = encapsulate(ephemeral_key, receiver_pubkey)
    cipher_text = aes_encrypt(aes_key, msg)
    result = ephemeral_key.public_key.format(False) + cipher_text
    return result.hex()


def decrypt(receiver_sk: str, msg: bytes) -> bytes:

    if isinstance(receiver_sk, str):
        private_key = hex2prv(receiver_sk)
    else:
        raise TypeError("Invalid secret key type")

    pubkey = msg[0:65]
    encrypted = msg[65:]
    ephemeral_public_key = PublicKey(pubkey)

    aes_key = decapsulate(ephemeral_public_key, private_key)
    return aes_decrypt(aes_key, encrypted)


def private_key(loc = '.private_key') -> bytes:

    with open(loc, 'rb') as sk:
        private_key = sk.read()
        return private_key