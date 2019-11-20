from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
import base64

BLOCK_SIZE = 16 # AES.block_size
KEY_SIZE = 32 # AES.key_size[2]

# Alice and Bob 공유하는 키/iv..
key = Random.new().read(KEY_SIZE)
IV = Random.new().read(BLOCK_SIZE)

# Alice
msg = "hello world"

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

# Bob
# enc_msg, key, IV 받았다고 가정.....
file_in = open("enc_msg.bin","rb")
enc_msg_bob = file_in.read()
file_in.close()

cipher_Bob = AES.new(key, AES.MODE_CBC, IV)
msg_with_hash_bob = unpad(cipher_Bob.decrypt(base64.b32decode(enc_msg_bob)), AES.block_size)

# base64 decoding + CBC/OFB/CTR 모드인 경우 언패딩 수행
print(msg_with_hash_bob)

hash_part = msg_with_hash_bob[:32] #SHA256.digest_size == 32bytes
msg_part = msg_with_hash_bob[32:]

hash_Bob = SHA256.new(msg_part)
if hash_part == hash_Bob.digest():
    print("Correct")
    print("Received MSG: ", msg_part.decode())

