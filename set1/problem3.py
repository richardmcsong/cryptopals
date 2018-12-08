from Crypto.Util.number import *
from operator import itemgetter

engFreq = [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'l', 'd', 'c', 'u', 'm', 'f', 'g', 'p', 'y', 'w', '\n', 'b', ',', '.', 'v', 'k', '-', '"', '_', '\'', 'x', ')', '(', ';', '0', 'j', '1', 'q', '=', '2', ':', 'z', '/', '*', '!', '?', '$', '3', '5', '>', '{', '}', '4', '9', '[', ']', '8', '6', '7', '\\', '+', '|', '&', '<', '%', '@', '#', '^', '`', '~',]

task = 0x1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

def decrypt_single_xor(task):
  answers = []
  error = None
  for i in range(255):
    plaintext = ''.join([chr(char ^ i) for char in long_to_bytes(task)])
    try:
      error = sum([engFreq.index(char.lower()) for char in plaintext])
    except:
      pass
    if error:
      answers.append({"pt":plaintext, "err":error})
    error = None

  return min(answers, key=itemgetter('err'))


print(decrypt_single_xor(task))