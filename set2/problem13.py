from Crypto.Util import number
from Crypto.Random import random
from Crypto.Cipher import AES
import binascii

key = number.long_to_bytes(random.getrandbits(8*16))
ecb = AES.new(key, AES.MODE_ECB)

def kv_test():
	task = "foo=bar&baz=qux&zap=zazzle"
	expected = {
		"foo": 'bar',
		"baz": 'qux',
		"zap": 'zazzle'
	}
	assert kv(task) == expected

def kv(task):
	output = {}
	tokens = task.split("&")
	for token in tokens:
		pair = token.split("=")
		output[pair[0]] = try_convert_num(pair[1])
	return output

def try_convert_num(s):
    try:
        return int(s)
    except ValueError:
        return s

def pkcs7(task, block_length):
	length_to_end = block_length - (len(task) % block_length)
	result = task + length_to_end * chr(length_to_end)
	return result

def remove_pkcs7(task):
	if (ord(task[-1]) < 16 and task[0 - ord(task[-1]):] == task[-1] * ord(task[-1])):
		return task[:0 - ord(task[-1])]
	else:
		return task


def profile_for_test():
	task = "foo@bar.com"
	expected = "email=foo@bar.com&uid=10&role=user"
	assert profile_for(task) == expected

def profile_for(email):
	for invalid in ["&", "="]:
		assert invalid not in email
	return "email=" + email + "&uid=10&role=user"

def encrypted_profile_for(email):
	return ecb.encrypt(pkcs7(profile_for(email), 16))

def decrypt_parse_profile(tokens):
	return kv(remove_pkcs7(ecb.decrypt(tokens)))

def attack(encrypted_token):
	return encrypted_token[:-16] + ecb.encrypt("role=admin" + "\x06"*6)

if __name__ == "__main__":
	kv_test()
	profile_for_test()
	actual = decrypt_parse_profile(attack(encrypted_profile_for("test@testtest.test")))
	expected = {
	  "email": "test@testtest.test",
	  "uid": 10,
	  "role": 'admin'
	}
	assert actual == expected