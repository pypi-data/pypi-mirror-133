# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecceran']

package_data = \
{'': ['*']}

install_requires = \
['coincurve==16.0.0', 'pycryptodome==3.12.0']

entry_points = \
{'console_scripts': ['ecceran = ecceran.__main__:main']}

setup_kwargs = {
    'name': 'ecceran',
    'version': '0.1.1',
    'description': 'Simple ECC encrypt decrypt',
    'long_description': "# Ecceran\n\nsimple ECC encrypt & decrypt\n\n### Install\n\n`$ pip install ecceran`\n\n### Generate Private Key\n\nrun `ecceran` in your command line for generate new secret key in `.private_key`\n\n```\n\n$ ecceran\n\npublic key : 02a4610d81d6c522ae67c2570********\n\n```\nthe public key will be used to decrypt. `generate` command will return public key from file `.private_key`, to re-generate need to delete file `private_key`\n\n### Get Private Key\n\n```python\n\nfrom ecceran import private_key\n\n\n\nprivate_key_app = private_key()\n\n# 5xa46gg0d81d6c522ae9ku2570********\n\n  \n\n```\n\n### Encrypt & Decrypt\n\n```python\n\nfrom ecceran import encrypt, decrypt, private_key\n\n\n\npubkey = '02a4610d81d6c522ae67c2570********'\n\nenc_data = encrypt(pubkey, b'test')\n\nprint(enc_data)\n\n# d2zx4d81d6xxx2va67c24470********\n\n  \n\nprikey = private_key()\n\nbyte = bytes.fromhex(enc_data)\n\ndec_data = decrypt(prikey, byte)\n\nprint(dec_data)\n\n# b'test'\n\n```",
    'author': 'hfrada',
    'author_email': 'madefrada@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
