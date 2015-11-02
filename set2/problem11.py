from Crypto.Util import number
from Crypto.Random import random
from Crypto.Cipher import AES

key = number.long_to_bytes(random.getrandbits(16 * 8))
iv = number.long_to_bytes(random.getrandbits(16 * 8))
ecb = AES.new(key, AES.MODE_ECB);
cbc = AES.new(key, AES.MODE_CBC, iv);

def pkcs7_padding(task, block_length):
	length_to_end = block_length - (len(task) % block_length)
	result = task + length_to_end * chr(length_to_end)
	return result

def encryption_oracle(input):
	plaintext = number.long_to_bytes(random.getrandbits(8 * random.randint(5, 10))) + input + number.long_to_bytes(random.getrandbits(8 * random.randint(5, 10)))
	plaintext = pkcs7_padding(plaintext, 16)
	if random.getrandbits(1):
		return ecb.encrypt(plaintext)
	else:
		return cbc.encrypt(plaintext)

def detect_ecb_or_cbc(input):
	blocks = [input[i:i+16] for i in range(0, len(input), 16)]
	if blocks[1] == blocks[2]:
		print "ecb"
	else:
		print "cbc"

detect_ecb_or_cbc(encryption_oracle("\x00" * 64))