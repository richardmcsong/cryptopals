from Crypto.Util.number import *

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

hDistanceTest()