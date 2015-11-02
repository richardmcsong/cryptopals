from Crypto.Cipher import AES
import binascii

cipher = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)
task = binascii.a2b_base64("".join(open('10.txt').read().split('\n')))

testcipher = AES.new("YELLOW SUBMARINE", AES.MODE_CBC, '\x00' * 16)

def cbc_encrypt(task, iv):
    blocks = [task[i:i+16] for i in range(0, len(task), 16)]
    result = ""
    last_block = iv
    for block in blocks:
        current = "".join([chr(ord(block[i]) ^ ord(last_block[i])) for i in range(len(block))])
        encryptedBlock = cipher.encrypt(block)
        result += encryptedBlock
        last_block = current
    return result

def cbc_decrypt(task, iv):
    blocks = [task[i:i+16] for i in range(0, len(task), 16)]
    result = ""
    last_block = iv
    for block in blocks:
        current = cipher.decrypt(block)
        result += "".join([chr(ord(current[i]) ^ ord(last_block[i])) for i in range(len(current))])
        last_block = block
    return result

assert cbc_decrypt(cbc_encrypt('YELLOW SUBMARINE', '\x00' * 16), '\x00' * 16) == 'YELLOW SUBMARINE'
assert cbc_decrypt(task, '\x00' * 16) == testcipher.decrypt(task)