# Ecceran

simple ECC encrypt & decrypt

### Install

`$ pip install ecceran`

### Generate Private Key

run `ecceran` in your command line for generate new secret key in `.private_key`

```

$ ecceran

public key : 02a4610d81d6c522ae67c2570********

```
the public key will be used to decrypt. `generate` command will return public key from file `.private_key`, to re-generate need to delete file `private_key`

### Get Private Key

```python

from ecceran import private_key



private_key_app = private_key()

# 5xa46gg0d81d6c522ae9ku2570********

  

```

### Encrypt & Decrypt

```python

from ecceran import encrypt, decrypt, private_key



pubkey = '02a4610d81d6c522ae67c2570********'

enc_data = encrypt(pubkey, b'test')

print(enc_data)

# d2zx4d81d6xxx2va67c24470********

  

prikey = private_key()

byte = bytes.fromhex(enc_data)

dec_data = decrypt(prikey, byte)

print(dec_data)

# b'test'

```