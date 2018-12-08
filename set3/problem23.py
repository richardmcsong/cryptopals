import problem21
(w, n, m, r) = (32, 624, 397, 31)
a = 0x9908B0DF
(u, d) = (11, 0xFFFFFFFF)
(s, b) = (7, 0x9D2C5680)
(t, c) = (15, 0xEFC60000)
l = 18
f = 1812433253
lower_mask = (1 << r) - 1
upper_mask = ((1 << w) - 1) ^ lower_mask

def left_pad(bin_array):
  while len(bin_array) != 32:
    bin_array = [0] + bin_array
  return bin_array

def undo_left_shift(mtout, shift, mask=0xFFFFFFFF):
  #build from the right
  mtstr = left_pad([int(c) for c in bin(mtout)[2:]])
  maskstr = left_pad([int(c) for c in bin(mask)[2:]])
  known_bits = [0]*32
  for i in range(31, -1, -1):
    if i+shift >= 32:
      # print("no")
      known_bits[i] = mtstr[i]
    else:
      known_bits[i] = mtstr[i] ^ (known_bits[i+shift] & maskstr[i])
  # print("".join([str(c) for c in known_bits]))
  return int("".join([str(c) for c in known_bits]), 2)

def undo_right_shift(mtout, shift, mask=0xFFFFFFFF):
  mtstr = left_pad([int(c) for c in bin(mtout)[2:]])
  maskstr = left_pad([int(c) for c in bin(mask)[2:]])
  known_bits = [0]*32
  for i in range(32):
    if i-shift < 0:
      # print("no")
      known_bits[i] = mtstr[i]
    else:
      known_bits[i] = mtstr[i] ^ (known_bits[i-shift] & maskstr[i])
  # print("".join([str(c) for c in known_bits]))
  return int("".join([str(c) for c in known_bits]), 2)

def untemper(mtout):
    mtout = undo_right_shift(mtout, l)
    mtout = undo_left_shift(mtout, t, c)
    mtout = undo_left_shift(mtout, s, b)
    mtout = undo_right_shift(mtout, u)
    return mtout


if __name__ == "__main__":
  mt1 = problem21.Mt19937()
  mt1.seed_mt(5489)
  mt1.twist()
  # print(a.mt[0])
  mt2 = problem21.Mt19937()
  mt2.index = 0
  for i in range(624):
    # print(a.extract_number())
    mt2.mt[i] = untemper(mt1.extract_number())
  mt1.seed_mt(5489)
  for i in range(900):
    print(mt1.extract_number())
    print(mt2.extract_number())
  # print(untemper(a.extract_number()))
