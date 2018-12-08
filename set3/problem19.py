from Crypto.Util import number
from Crypto.Random import random
from Crypto.Cipher import AES
from operator import itemgetter
import binascii
from pwn import *

tasks = b"""SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==
Q29taW5nIHdpdGggdml2aWQgZmFjZXM=
RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==
RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=
SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk
T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==
T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=
UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==
QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=
T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl
VG8gcGxlYXNlIGEgY29tcGFuaW9u
QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==
QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=
QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==
QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=
QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=
VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==
SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==
SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==
VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==
V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==
V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==
U2hlIHJvZGUgdG8gaGFycmllcnM/
VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=
QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=
VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=
V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=
SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==
U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==
U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=
VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==
QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu
SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=
VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs
WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=
SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0
SW4gdGhlIGNhc3VhbCBjb21lZHk7
SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=
VHJhbnNmb3JtZWQgdXR0ZXJseTo=
QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4="""

key = number.long_to_bytes(random.getrandbits(16 * 8))
engFreq = [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'l', 'd', 'c', 'u', 'm', 'f', 'g', 'p', 'y', 'w', '\n', 'b', ',', '.', 'v', 'k', '-', '"', '_', '\'', 'x', ')', '(', ';', '0', 'j', '1', 'q', '=', '2', ':', 'z', '/', '*', '!', '?', '$', '3', '5', '>', '{', '}', '4', '9', '[', ']', '8', '6', '7', '\\', '+', '|', '&', '<', '%', '@', '#', '^', '`', '~',]
def atk_ctr(list_of_ct):
    blocks = [bytes(filter(None.__ne__, [ct[i] if i < len(ct) else None for ct in list_of_ct])) for i in range(max([len(ct) for ct in list_of_ct]))]
    print(blocks)
    keystream = b""
    error = None
    for block in blocks:
        answers = []
        for i in range(255):
            plaintext = ''.join([chr(char ^ i) for char in block])
            try:
                error = sum([engFreq.index(char.lower()) for char in plaintext])
            except:
                pass
            if error:
                answers.append({"ks":bytes([i]), "err":error})
            error = None
        try:
            keystream += min(answers, key=itemgetter('err'))["ks"]
        except:
            keystream += "\x00"
    print(keystream)
    print([bytes([ct[i] ^ keystream[i] for i in range(len(ct))]) for ct in list_of_ct])

def ctr(text):
    keystream = b""
    i = 0
    while len(keystream) < len(text):
        keystream += AES.new(key, AES.MODE_ECB).encrypt(p64(0) + p64(i))
        i += 1
    return bytes([text[c] ^ keystream[c] for c in range(len(text))])
# print(type(tasks.split(b"\n")[0]))
ct = [ctr(binascii.a2b_base64(bytes(t))) for t in tasks.split(b"\n")]
# print(ct)

print(atk_ctr(ct))