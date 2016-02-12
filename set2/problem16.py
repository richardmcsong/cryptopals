from Crypto.Util import number
from Crypto.Random import random
from Crypto.Cipher import AES
from pwn import *

key = number.long_to_bytes(random.getrandbits(16 * 8))
iv = number.long_to_bytes(random.getrandbits(16 * 8))
ecb = AES.new(key, AES.MODE_ECB)

def cbc_encrypt(input):
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pkcs7(input, 16))

def cbc_decrypt(ct):
    return strip_pkcs7(AES.new(key, AES.MODE_CBC, iv).decrypt(ct))

def strip_pkcs7(input):
    padding_length = u8(input[-1])
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
    result = task + length_to_end * chr(length_to_end)
    return result

def sanitize_inputs(input):
    # dict = {";" : "%3B", "=": "%3D"}
    dict = {";" : "\;", "=": "\="}
    return "".join([dict[char] if char in dict.keys() else char for char in input])

def create_request(input): # this is function 1 in the problem set
    input = sanitize_inputs(input)
    return cbc_encrypt("comment1=cooking%20MCs;userdata=" + input + ";comment2=%20like%20a%20pound%20of%20bacon")

def is_admin(input): # this is function 2
    return ["admin", "true"] in [item.split('=') for item in cbc_decrypt(input).split(';')]

def add_admin(ct, insert_string): # the attack, note that len(insert_string) < 16, as it'll start overwriting itself
    request = list(ct)
    for i in range(len(insert_string)):
        request[32+i] = chr(ord(request[32+i]) ^ ord(insert_string[i]))
    return "".join(request)


nopsled = "\x00\x00\x00\x00\x00\x00\x00\x00" * 8
request = create_request(nopsled)
print "raw request: " + cbc_decrypt(request)
print "encrypted request: " + request
request = add_admin(request, ";admin=true;a=")
print "attacked request: " + cbc_decrypt(request)
print "is admin result: " + str(is_admin(request))