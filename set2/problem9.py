def pkcs7_padding(task, block_length):
  length_to_end = block_length % len(task)
  result = task + length_to_end * chr(length_to_end)
  return result
assert pkcs7_padding("YELLOW SUBMARINE", 20) == "YELLOW SUBMARINE\x04\x04\x04\x04"
