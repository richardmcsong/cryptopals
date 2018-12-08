from Crypto.Util import number
from Crypto.Random import random
from Crypto.Cipher import AES
import binascii

key = number.long_to_bytes(random.getrandbits(16 * 8))
iv = number.long_to_bytes(random.getrandbits(16 * 8))
ecb = AES.new(key, AES.MODE_ECB);
cbc = AES.new(key, AES.MODE_CBC, iv);

def pkcs7_padding(task, block_length):
	# print(type(task))
	length_to_end = block_length - (len(task) % block_length)
	result = task + length_to_end * chr(length_to_end).encode()
	return result

def encryption_oracle(input):
	# plaintext = number.long_to_bytes(random.getrandbits(8 * random.randint(5, 10))) + input + number.long_to_bytes(random.getrandbits(8 * random.randint(5, 10)))
	plaintext = pkcs7_padding(input, 16)
	return ecb.encrypt(plaintext)

def discover_block_size(function):
	ct_lengths = [len(function(b'\x00'*i)) for i in range(40)]
	ct_lengths = list(set(ct_lengths))
	ct_lengths.sort()
	return ct_lengths[1] - ct_lengths[0]

def get_keychar_dict_ecb(block_length, enc_func):
	keychar_dict = {}
	for i in range(256):
		keychar_dict[enc_func(b'\x00' * (block_length - 1) + chr(i).encode())] = chr(i).encode()
	return keychar_dict

def crack_ecb(task, enc_func):
	block_length = discover_block_size(enc_func)
	keychar_dict = get_keychar_dict_ecb(block_length, enc_func)
	result = b""
	for char in task:
		result += keychar_dict[enc_func(b'\x00'*(block_length-1) + bytes([char]))]
	return result

task = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
task = binascii.a2b_base64(task)
print(crack_ecb(task, encryption_oracle))
assert task == crack_ecb(task, encryption_oracle)

