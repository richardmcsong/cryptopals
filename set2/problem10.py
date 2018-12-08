from Crypto.Cipher import AES
import binascii

pw = b"YELLOW SUBMARINE"
cipher = AES.new(pw, AES.MODE_ECB)
task = binascii.a2b_base64("".join(open('10.txt').read().split('\n')))

testcipher = AES.new(pw, AES.MODE_CBC, b'\x00' * 16)

def cbc_encrypt(task, iv):
    blocks = [task[i:i+16] for i in range(0, len(task), 16)]
    result = b""
    last_block = iv
    for block in blocks:
        current = "".join([chr(block[i] ^ last_block[i]) for i in range(len(block))]).encode()
        encryptedBlock = cipher.encrypt(block)
        result += encryptedBlock
        last_block = current
    return result

def cbc_decrypt(task, iv):
    blocks = [task[i:i+16] for i in range(0, len(task), 16)]
    result = b""
    last_block = iv
    for block in blocks:
        current = cipher.decrypt(block)
        result += "".join([chr(current[i] ^ last_block[i]) for i in range(len(current))]).encode()
        last_block = block
    return result

assert cbc_decrypt(cbc_encrypt(pw, b'\x00' * 16), b'\x00' * 16) == pw
assert cbc_decrypt(task, b'\x00' * 16) == testcipher.decrypt(task)