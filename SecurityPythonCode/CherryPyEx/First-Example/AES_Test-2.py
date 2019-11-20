from Crypto import Random
from Crypto.Cipher import AES
import os
import base64

BLOCK_SIZE = 16
KEY_SIZE=32

key = os.urandom(KEY_SIZE) # 또는 key = Random.new().read(KEY_SIZE) 와 동일하다(Crypto 에서 제공하는 랜덤 생성 함수)
IV = Random.new().read(BLOCK_SIZE)

message = b"Information Security & Programming. Test Message!...." #binary string 작성 법(꼭 이 형태의 스트링을 넣어 주어야 된다.) 또는 message.encode() 로 사용한다.
print("key: ", key)
print("key length: ", len(key)) # 32byte == 256bit

def AESencrypt(message, passphrase):
    cipher = AES.new(passphrase, AES.MODE_CFB, IV)
    print(cipher)
    return cipher.encrypt(message)

def AESdecrypt(encrypted, passphrase):
    cipher = AES.new(passphrase, AES.MODE_CFB, IV)
    return cipher.decrypt(encrypted)

encrypted = AESencrypt(message, key)
print("Encrypted: ", encrypted)
print("Encrypted (base64): ", base64.b32encode(encrypted))
print("Encrypted (base64 & decode): ", base64.b32encode(encrypted).decode())

decrypted = AESdecrypt(encrypted, key)
print("Decrypted: ", decrypted.decode('utf-8'))


# base64 -> 한자의 6bit
# 64 =  2^6

