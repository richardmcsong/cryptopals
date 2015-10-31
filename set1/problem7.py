import binascii
from Crypto.Cipher import AES

task = binascii.a2b_base64("".join(open('7.txt').read().split('\n')))
key = "YELLOW SUBMARINE"
cipher = AES.new(key, AES.MODE_ECB)
print cipher.decrypt(task)