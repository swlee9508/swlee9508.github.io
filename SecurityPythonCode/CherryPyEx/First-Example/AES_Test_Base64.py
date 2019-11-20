from Crypto import Random
from Crypto.Cipher import AES
import os
import base64
from Crypto.Util.Padding import pad, unpad
# 패딩/언패딩 관련 라이브러리 추가

BLOCK_SIZE = 16
KEY_SIZE = 32

BLOCK_SIZE = AES.block_size
KEY_SIZE = AES.key_size[2]

key = os.urandom(KEY_SIZE)
IV = Random.new().read(BLOCK_SIZE)

message = b"Information Security & Programming. Test Message........"
print("key: ", key)
print("key length: ", len(key))

def AESencrypt(message, passphrase):
    cipher = AES.new(passphrase, AES.MODE_CBC, IV)
    print(cipher)
    #return cipher.encrypt(message)  # CFB 모드인 경우에는 ...
    #return cipher.encrypt(pad(message, AES.block_size))  # CBC/OFB/CTR 모드인 경우 패딩 수행
    return base64.b32encode(cipher.encrypt(pad(message, AES.block_size))).decode()
    # CBC/OFB/CTR 모드인 경우 패딩 수행 + base64 encoding

def AESdecrypt(encrypted, passphrase):
    cipher = AES.new(passphrase, AES.MODE_CBC, IV)
    #return cipher.decrypt(encrypted)
    #return unpad(cipher.decrypt(encrypted), AES.block_size)   # CBC/OFB/CTR 모드인 경우 언패딩 수행
    return unpad(cipher.decrypt(base64.b32decode(encrypted)), AES.block_size)
    # base64 decoding + CBC/OFB/CTR 모드인 경우 언패딩 수행

encrypted = AESencrypt(message, key)
print("Encrypted: ", encrypted)
#print("Encrypted (base64): ", base64.b32encode(encrypted))
#print("Encrypted (base64 & decode): ", base64.b32encode(encrypted).decode())

decrypted = AESdecrypt(encrypted, key)
print("Decrypted: ", decrypted.decode('utf-8'))
