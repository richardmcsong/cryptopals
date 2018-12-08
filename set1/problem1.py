import binascii

task = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

def hex_to_base64(task):
    return binascii.b2a_base64(binascii.a2b_hex(task))

def verify(result):
    assert result == b"SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t\n"

print(hex_to_base64(task))
verify(hex_to_base64(task))