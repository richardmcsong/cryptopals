from pwn import *
class InvalidPKCS7Error(Exception):
    pass


def strip_pkcs7(input):
    padding_length = u8(input[-1])
    if padding_length > 15:
        return input
    else:
        if input[0 - padding_length:] != p8(padding_length)*padding_length:
            raise InvalidPKCS7Error()
        else:
            return input[0: 0-padding_length]

print strip_pkcs7("ICE ICE BABY\x04\x04\x04\x04") == "ICE ICE BABY" 
try:
    strip_pkcs7("ICE ICE BABY\x05\x05\x05\x05")
    print "should have raised an error"
except InvalidPKCS7Error:
    print "caught an expected error"

try:
    strip_pkcs7("ICE ICE BABY\x01\x02\x03\x04")
    print "should have raised an error"
except InvalidPKCS7Error:
    print "caught an expected error"