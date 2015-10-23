import binascii
from Crypto.Util.number import *

xor_term_1 = 0x1c0111001f010100061a024b53535009181c
xor_term_2 = 0x686974207468652062756c6c277320657965
result = "746865206b696420646f6e277420706c6179"

def fixed_xor(term1, term2):
  return binascii.b2a_hex(long_to_bytes(term1^term2))

actual = fixed_xor(xor_term_1, xor_term_2)
print actual
assert actual == result