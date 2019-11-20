from Crypto import Random
from Crypto.Cipher import AES,PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
import base64

BLOCK_SIZE = 16
KEY_SIZE = 32

# Alice and Bob 공유하는 키/iv..
key = Random.new().read(KEY_SIZE)
IV = Random.new().read(BLOCK_SIZE)

# Bob 의 공개키를 이용해서 key 와 IV 값을 안전하게 전달한다...
pubkey_bob = RSA.import_key(open("public_key_Bob.bin", "rb").read())
cipher_RSA_Alice = PKCS1_OAEP.new(pubkey_bob)
enc_key = cipher_RSA_Alice.encrypt(key)

file_out = open("enc_key.bin", "wb")
file_out.write(IV + enc_key)
file_out.close()

# Alice
msg = "hello world!! Brother...."

hashResult = SHA256.new(msg.encode())

msg_with_hash = hashResult.digest()+msg.encode()
print(msg_with_hash)

cipher = AES.new(key, AES.MODE_CBC, IV)
enc_msg = base64.b32encode(cipher.encrypt(pad(msg_with_hash, AES.block_size))).decode()
# CBC/OFB/CTR 모드인 경우 패딩 수행 + base64 encoding

print("해쉬 + 평문에 대한 암호문 : " + enc_msg)
file_out = open("enc_msg.bin","wb")
file_out.write(enc_msg.encode())
file_out.close()