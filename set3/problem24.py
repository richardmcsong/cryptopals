import problem21
import Crypto.Util.number
import random
import asyncio
import multiprocessing

class Mt19937StreamCipher:

  def __init__(self):
    self.mtprng = problem21.Mt19937()
    # self.mtprng.seed_mt(seed)

  def stream_cipher(self, data, key):
    self.mtprng.seed_mt(key)
    keystream = b''
    while len(keystream) < len(data):
      keystream += Crypto.Util.number.long_to_bytes(self.mtprng.extract_number())
    return "".join([chr(ord(data[i]) ^ keystream[i]) for i in range(len(data))])

def search(ct, padding, known_length, start, end, key):
  pkey = start
  while pkey < end and key.value < 0:
    if Mt19937StreamCipher().stream_cipher("p"*padding + "A"*known_length, pkey)[padding:] == ct[padding:]:
      key.value = pkey
      print("found")
      return
    pkey += 1



def find_key(ct, known_length):
  padding = len(ct) - known_length
  key = 0
  tasks = []
  key = multiprocessing.Value("i", -1)
  # pool = multiprocessing.Pool(processes=6)
  tasks = [multiprocessing.Process(target=search, args=(ct, padding, known_length, i, i+(10000 if i != 60000 else 5535), key)) for i in range(0, 0xffff, 10000)]
  # for i in range(0, 0xffff, 10000):
  #   tasks.append(search(ct, padding, known_length, i, i+(10000 if i != 60000 else 5535)))
  [task.start() for task in tasks]
  [task.join() for task in tasks]
  return key.value
  # print([task.get() for task in tasks])
  # raise Exception()

if __name__ == "__main__":
  key = random.getrandbits(16)
  # key = 5489
  pt = ''.join([chr(random.getrandbits(8)) for i in range(random.randint(20, 100))]) + "A"*60
  ct = Mt19937StreamCipher().stream_cipher(pt, key)
  assert find_key(ct, 60) == key
  # asyncio.run(find_key(ct, 60))
  # assert find_key(ct, 60) == key
  # print(ct)
  # print(Mt19937StreamCipher().stream_cipher(ct, key))
