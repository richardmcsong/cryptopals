from Crypto.Util.number import *
import binascii
from operator import itemgetter

engFreq = [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'l', 'd', 'c', 'u', 'm', 'f', 'g', 'p', 'y', 'w', '\n', 'b', ',', '.', 'v', 'k', '-', '"', '_', '\'', 'x', ')', '(', ';', '0', 'j', '1', 'q', '=', '2', ':', 'z', '/', '*', '!', '?', '$', '3', '5', '>', '{', '}', '4', '9', '[', ']', '8', '6', '7', '\\', '+', '|', '&', '<', '%', '@', '#', '^', '`', '~',]

def decrypt_single_xor(task):
  answers = []
  error = None
  for i in range(255):
    plaintext = ''.join([chr(ord(char) ^ i) for char in task])
    try:
      error = sum([engFreq.index(char.lower()) if char.lower() in engFreq else 99 for char in plaintext])
    except:
      pass
    if error:
      answers.append({"pt":plaintext, "err":error, "key":chr(i)})
    error = None
  if answers:
    return min(answers, key=itemgetter('err'))
  else:
    return None

def hDistance(task1, task2):
  assert len(task1) == len(task2)
  count = 0
  for i in range(len(task1)):
    count += bin(ord(task1[i]) ^ ord(task2[i])).count('1')
  return count  
def hDistanceTest():
  task1 = "this is a test"
  task2 = "wokka wokka!!!"
  assert hDistance(task1, task2) == 37

def find_key_length(task):
  edit_distances = {}
  for i in range(1 , 40):
    edit_distances[float(hDistance(task[0:i], task[i:2*i])) / i] = i
  keys = edit_distances.keys()
  keys.sort()
  return [edit_distances[i] for i in keys]

def break_repeat_key(task):
  results = []
  for klength in find_key_length(task):
    error = 0
    key = ""
    blocks = ["" for i in range(klength)]
    for i in range(len(task)):
      blocks[i%klength] += task[i]
    for block in blocks:
      potential = decrypt_single_xor(block)
      error += potential['err']
      key += potential['key']
    results.append({"key":key, "error":error})
  return min(results, key=itemgetter('error'))
def decode(task, key):
  return "".join([chr(ord(task[i]) ^ ord(key[i % len(key)])) for i in range(len(task))])

task = ""
for line in open('6.txt').read().split("\n"):
  task += line
task = binascii.a2b_base64(task)
# print find_key_length(task)
print decode(task, break_repeat_key(task)["key"])
  