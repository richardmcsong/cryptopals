from Crypto.Util import number
from Crypto.Random import random
from Crypto.Cipher import AES
import binascii

key = number.long_to_bytes(random.getrandbits(16 * 8))
iv = number.long_to_bytes(random.getrandbits(16 * 8))
ecb = AES.new(key, AES.MODE_ECB);
cbc = AES.new(key, AES.MODE_CBC, iv);

def pkcs7(task, block_length):
	length_to_end = block_length - (len(task) % block_length)
	result = task + length_to_end * chr(length_to_end)
	return result

def encryption_oracle(input):
	plaintext = pkcs7(number.long_to_bytes(random.getrandbits(8 * random.randint(0, 100))) + input, 16)
	return ecb.encrypt(plaintext)

def discover_block_size(function):
	ct_lengths = [len(function('\x00'*i)) for i in range(40)]
	ct_lengths = list(set(ct_lengths))
	ct_lengths.sort()
	return ct_lengths[1] - ct_lengths[0]

def generate_keydict(knownbytes):
	keychar_dict = {}
	for i in range(256):
		keychar_dict[ecb.encrypt(pkcs7(chr(i) + knownbytes[:15]))] = chr(i)
	return keychar_dict


def crack_ecb_hard(task):
	pt = "\x00" * 64 + task
	keydict = generate_keydict(knownbytes)


task = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
task = binascii.a2b_base64(task)
# print crack_ecb(task, encryption_oracle)
# assert task == crack_ecb(task, encryption_oracle)

