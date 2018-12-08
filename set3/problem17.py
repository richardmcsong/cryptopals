from Crypto.Util import number
from Crypto.Random import random
from Crypto.Cipher import AES
import binascii
from pwn import *

key = number.long_to_bytes(random.getrandbits(16 * 8))
iv = number.long_to_bytes(random.getrandbits(16 * 8))
class InvalidPKCS7Error(Exception):
    pass

tasks = """MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=
MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=
MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==
MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==
MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl
MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==
MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==
MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=
MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=
MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93""".split("\n")

def cbc_encrypt(ipt):
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pkcs7(ipt, 16))
def pkcs7(task, block_length):
    length_to_end = block_length - (len(task) % block_length)
    if length_to_end == 16:
        length_to_end = 0
    result = task + length_to_end * bytes([length_to_end])
    return result
def strip_pkcs7(input):
    padding_length = u8(bytes([input[-1]]))
    if input[0 - padding_length:] != p8(padding_length)*padding_length:
        raise InvalidPKCS7Error()
    else:
        return input[0: 0-padding_length]
def check_padding(ct, iv):
	try: 
		strip_pkcs7(AES.new(key, AES.MODE_CBC, iv).decrypt(ct))
		return True
	except InvalidPKCS7Error as e:
		return False
def attack(ct, iv):
    blocks = [iv] + [ct[i:i+16] for i in range(0, len(ct), 16)]
    return strip_pkcs7(b"".join([break_block(blocks[i], blocks[i+1]) for i in range(len(blocks)-1)]))


def break_block(pb, tb):
    pt = b""
    working = [0]*16
    for pos in range(-1, 0 - len(tb)-1, -1):
        for i in range(256):
            if check_padding(tb, bytes(working)):
                pbyte = i^pb[pos]^abs(pos)
                pt = bytes([pbyte]) + pt
                for j in range(-1, 0 - len(pt) -1, -1):
                    working[j] = len(pt)+1^pt[j]^pb[j]
                break
            else:
                working[pos] += 1
    return pt



task = tasks[random.randint(0, len(tasks)-1)]
pt = binascii.a2b_base64(task)
ct = cbc_encrypt(pt)
print(ct)
print(iv)
print(attack(ct, iv))
print(pt)
assert attack(ct, iv) == pt
