from Crypto.Util import number
from Crypto.Random import random
from Crypto.Cipher import AES
import binascii
from pwn import *

task = b"L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
key = b"YELLOW SUBMARINE"
def ctr(text):
    keystream = b""
    i = 0
    while len(keystream) < len(text):
        keystream += AES.new(key, AES.MODE_ECB).encrypt(p64(0) + p64(i))
        i += 1
    return bytes([text[c] ^ keystream[c] for c in range(len(text))])
ct = binascii.a2b_base64(task)
print(ct)
print(ctr(ct))
