import binascii
from Crypto.Cipher import AES
from operator import itemgetter

tasks = [binascii.unhexlify(text) for text in open('8.txt').read().split('\n')]

tasks = filter(None, tasks)
def detect_ecb(tasks):
  result = []
  for task in tasks:
    count = 0
    blocks = [task[i:i+16]for i in range(0, len(task), 16)]
    for block in blocks:
      if blocks.count(block) > 0:
        count += 1
    result.append({"task": task, "count": count})
  return max(result, key=itemgetter("count"))



# cipher = AES.new('YELLOW SUBMARINE', AES.MODE_ECB)


# def encrypt():
#   task = raw_input('enter task:')
#   print cipher.encrypt(task)

print detect_ecb(tasks)