from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad,pad
import base64

BLOCK_SIZE = AES.block_size
KEY_SIZE = AES.key_size[2]

key = Random.new().read(KEY_SIZE)
IV = Random.new().read(BLOCK_SIZE)

message = "Hello world......."

hashResult = SHA256.new(message.encode())

msg_in_hash = hashResult.digest()+message.encode()

cipher = AES.new(key, AES.MODE_CBC, IV)
enc_msg = base64.b32encode(cipher.encrypt(pad(msg_in_hash, AES.block_size))).decode()

file_out = open("enc_msg.bin","wb")
file_out.write(enc_msg.encode())
file_out.close


file_in = open("enc_msg.bin","rb")
enc_msg_Alice = file_in.read()
file_in.close()

# cipher_bob = AES.new(key, AES.MODE_CBC, IV)
# dec_msg = unpad(cipher_bob.decrypt(base64.b32decode(enc_msg_Alice)), AES.block_size)

cipher_Bob = AES.new(key, AES.MODE_CBC, IV)
dec_msg = unpad(cipher_Bob.decrypt(base64.b32decode(enc_msg_Alice)), AES.block_size)


hash_part = dec_msg[:32]
msg_part = dec_msg[32:]

if hash_part == SHA256.new(msg_part).digest():
    print("correct")
    print("msg : ", msg_part.decode())