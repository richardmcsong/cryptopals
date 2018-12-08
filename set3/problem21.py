(w, n, m, r) = (32, 624, 397, 31)
a = 0x9908B0DF
(u, d) = (11, 0xFFFFFFFF)
(s, b) = (7, 0x9D2C5680)
(t, c) = (15, 0xEFC60000)
l = 18
f = 1812433253
lower_mask = (1 << r) - 1
upper_mask = ((1 << w) - 1) ^ lower_mask

class Mt19937:
  def __init__(self):
    self.mt = list(range(n))
    self.index = n+1

  def seed_mt(self, seed):
    # nonlocal index
    # nonlocal mt
    self.index = n
    self.mt[0] = seed
    for i in range(1, len(self.mt)):
      self.mt[i] = d & (f * (self.mt[i-1] ^ (self.mt[i-1] >> (w-2))) + i)

  def extract_number(self):
    # nonlocal index
    # nonlocal mt
    if self.index >= n:
        if self.index > n:
          self.seed_mt(5489)
          # Alternatively, seed with constant value; 5489 is used in reference C code[46]
        self.twist()

    y = self.mt[self.index]
    # print("stage 1: " + str(y))
    y = y ^ ((y >> u) & d)
    # print("stage 2: " + str(y))
    # print(bin(y))
    # print(bin((y<<s) & 0xffffffff))
    # print(bin(b))
    # print(bin(((y << s) & b)))
    y = y ^ ((y << s) & b)
    # print(bin(((y << s) & b)))
    # print("0b000"+bin(y)[2:])
    # print("stage 3: " + str(y))
    y = y ^ ((y << t) & c)
    # print("stage 4: " + str(y))
    y = y ^ (y >> l)
    # print("stage 5: " + str(y))

    self.index += 1
    return d & y

  def genrand_res53(self):
    a = extract_number() >> 5
    b = extract_number() >> 6
    return (a*67108864.0+b)*(1.0/9007199254740992.0)

  def twist(self):
    for i in range(n-1):
      x = (self.mt[i] & upper_mask) + (self.mt[(i+1) % n] & lower_mask)
      xA = x >> 1
      if (x % 2) != 0:
        xA = xA ^ a
      self.mt[i] = self.mt[(i + m) % n] ^ xA
    self.index = 0
if __name__ == "__main__":
  mt = Mt19937()
  mt.seed_mt(5489)
  print([mt.extract_number() for i in range(10)])
  mt2 = Mt19937()
  mt2.seed_mt(5489)
# print([mt.extract_number() for i in range(10)])
# print([mt2.extract_number() for i in range(10)])
# print([extract_number() for i in range(10)])
# seed_mt(5489)
# twist()
# twist()
# print([extract_number() for i in range(10)])
# seed_mt(5489)
# # twist()
# print(genrand_res53())
# print(genrand_res53())
# import random
# random.seed(5489)
# print(random.random())
# print(random.random())
