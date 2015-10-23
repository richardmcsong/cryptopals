from Crypto.Util.number import *
from operator import itemgetter

engFreq = [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'l', 'd', 'c', 'u', 'm', 'f', 'g', 'p', 'y', 'w', '\n', 'b', ',', '.', 'v', 'k', '-', '"', '_', '\'', 'x', ')', '(', ';', '0', 'j', '1', 'q', '=', '2', ':', 'z', '/', '*', '!', '?', '$', '3', '5', '>', '{', '}', '4', '9', '[', ']', '8', '6', '7', '\\', '+', '|', '&', '<', '%', '@', '#', '^', '`', '~',]

task = []

def decrypt_single_xor(task):
  answers = []
  error = None
  for i in range(255):
    plaintext = ''.join([chr(ord(char) ^ i) for char in long_to_bytes(task)])
    try:
      error = sum([engFreq.index(char.lower()) for char in plaintext])
    except:
      pass
    if error:
      answers.append({"pt":plaintext, "err":error})
    error = None
  try:
    result = min(answers, key=itemgetter('err'))
  except:
    result = None

  return result

file = open("4.txt")
task = [int(line, 16) for line in file.read().split("\n")]
answers = []
for line in task:
  result = decrypt_single_xor(line)
  if result:
    answers.append(result)
print min(answers, key=itemgetter('err'))["pt"]