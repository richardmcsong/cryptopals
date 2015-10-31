from Crypto.Cipher import AES

cipher = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)
task = "".join(open('10.txt').read().split('\n'))

def cbc_decrypt(task, iv):
  blocks = [task[i:i+16] for i in range(0, len(task), 16)]
  print blocks
  result = ""
  last_block = iv
  for block in blocks:
    current = cipher.decrypt(block)
    result += "".join([chr(ord(current[i]) ^ ord(last_block[i])) for i in range(len(current))])
    last_block = block
    
  return result


print cbc_decrypt(task, '\x00' * 16)

assert cipher.decrypt(cipher.encrypt('YELLOW SUBMARINE')) == 'YELLOW SUBMARINE'
print cipher.decrypt('VGY4VgF8y7GedI1h')