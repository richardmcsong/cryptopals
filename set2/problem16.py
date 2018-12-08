from Crypto.Util import number
from Crypto.Random import random
from Crypto.Cipher import AES
from pwn import *

key = number.long_to_bytes(random.getrandbits(16 * 8))
iv = number.long_to_bytes(random.getrandbits(16 * 8))
ecb = AES.new(key, AES.MODE_ECB)

def cbc_encrypt(ipt):
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pkcs7(ipt, 16))

def cbc_decrypt(ct):
    return strip_pkcs7(AES.new(key, AES.MODE_CBC, iv).decrypt(ct))

def strip_pkcs7(input):
    padding_length = u8(bytes([input[-1]]))
    if padding_length > 15:
        return input
    else:
        if input[0 - padding_length:] != p8(padding_length)*padding_length:
            raise InvalidPKCS7Error()
        else:
            return input[0: 0-padding_length]

def pkcs7(task, block_length):
    length_to_end = block_length - (len(task) % block_length)
    if length_to_end == 16:
        length_to_end = 0
    result = task + length_to_end * bytes([length_to_end])
    return result

def sanitize_inputs(i):
    # dict = {";" : "%3B", "=": "%3D"}
    i = i.decode()
    d = {";" : "\;", "=": "\="}
    return "".join([d[char] if char in d.keys() else char for char in i]).encode()

def create_request(ipt): # this is function 1 in the problem set
    input = sanitize_inputs(ipt)
    return cbc_encrypt(b"comment1=cooking%20MCs;userdata=" + ipt + b";comment2=%20like%20a%20pound%20of%20bacon")

def is_admin(input): # this is function 2
    return ["admin", "true"] in [item.split('=') for item in str(cbc_decrypt(input)).split(';')]

def add_admin(ct, insert_string): # the attack, note that len(insert_string) < 16, as it'll start overwriting itself
    request = list(ct)
    for i in range(len(insert_string)):
        request[32+i] = request[32+i] ^ insert_string[i]
    return bytes(request)


nopsled = b"\x00\x00\x00\x00\x00\x00\x00\x00" * 8
request = create_request(nopsled)
print("raw request: " + cbc_decrypt(request).decode())
request = add_admin(request, b";admin=true;a=")
print("attacked request: " + str(cbc_decrypt(request)))
print("is admin result: " + str(is_admin(request)))