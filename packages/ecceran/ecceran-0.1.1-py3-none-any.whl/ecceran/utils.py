import codecs

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA256
from coincurve import PrivateKey, PublicKey
from coincurve.utils import get_valid_secret

AES_KEY_BYTES_LEN = 32
AES_CIPHER_MODE = AES.MODE_GCM

def aes_encrypt(key: bytes, plain_text: bytes):
    aes_cipher = AES.new(key, AES_CIPHER_MODE)

    encrypted, tag = aes_cipher.encrypt_and_digest(plain_text)
    cipher_text = bytearray()
    cipher_text.extend(aes_cipher.nonce)
    cipher_text.extend(tag)
    cipher_text.extend(encrypted)
    return bytes(cipher_text)

def aes_decrypt(key: bytes, cipher_text: bytes) -> bytes:
    iv = cipher_text[:16]
    tag = cipher_text[16:32]
    ciphered_data = cipher_text[32:]

    aes_cipher = AES.new(key, AES_CIPHER_MODE, nonce=iv)
    return aes_cipher.decrypt_and_verify(ciphered_data, tag)


def encapsulate(private_key: PrivateKey, peer_public_key: PublicKey) -> bytes:
    shared_point = peer_public_key.multiply(private_key.secret)
    master = private_key.public_key.format(compressed=False) + shared_point.format(
        compressed=False
    )
    derived = HKDF(master, AES_KEY_BYTES_LEN, b"", SHA256)
    return derived


def decapsulate(public_key: PublicKey, peer_private_key: PrivateKey) -> bytes:
    shared_point = public_key.multiply(peer_private_key.secret)
    master = public_key.format(compressed=False) + shared_point.format(compressed=False)
    derived = HKDF(master, AES_KEY_BYTES_LEN, b"", SHA256)
    return derived


def generate_key() -> PrivateKey:
    return PrivateKey(get_valid_secret())


def hex2pub(pub_hex: str) -> PublicKey:

    if pub_hex.startswith("0x") or pub_hex.startswith("0X"):
        return pub_hex[2:]

    uncompressed = codecs.decode(pub_hex, "hex")
    if len(uncompressed) == 64:
        uncompressed = b"\x04" + uncompressed

    return PublicKey(uncompressed)


def hex2prv(prv_hex: str) -> PrivateKey:

    if prv_hex.startswith("0x") or prv_hex.startswith("0X"):
        return prv_hex[2:]
    prv_hex = codecs.decode(prv_hex, 'hex')

    return PrivateKey(prv_hex)