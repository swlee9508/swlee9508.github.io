from Crypto import Random
from Crypto.Cipher import AES
import os
import base64
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
# 패딩/언패딩 관련 라이브러리 추가

BLOCK_SIZE = 16
KEY_SIZE = 32

BLOCK_SIZE = AES.block_size
KEY_SIZE = AES.key_size[2]


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

### main ###
seed_number = input("Seed Number from WebServer:")

key_AES = SHA256.new(seed_number.encode()).digest()[:16]  ## generated AES Key
IV = Random.new().read(BLOCK_SIZE)

message = b"Web SeverBased Aes Enc/Dec and File Upload Test........"
print("key: ", key_AES)
print("key length: ", len(key_AES))

cipher_AES = AES.new(key_AES, AES.MODE_CBC, IV)
encrypted_msg = base64.b32encode(cipher_AES.encrypt(pad(message, AES.block_size))).decode()

file_out = open("./AES_encrypted_data_for_Upload.bin", "wb")
output = IV + encrypted_msg.encode()
file_out.write(output)  # IV + encrypted_msg 순서로 파일에 저장
file_out.close()
print("File Created!! Let's Upload to Server!!")