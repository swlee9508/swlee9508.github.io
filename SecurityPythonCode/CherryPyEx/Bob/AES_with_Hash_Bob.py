from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES,PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
import base64

# Bob
# enc_msg, key, IV 받았다고 가정.....
file_in = open("enc_key.bin", "rb")
IV_with_enc_key = file_in.read()
file_in.close()

IV2 = IV_with_enc_key[:16]
enc_key_part = IV_with_enc_key[16:]

print("Received IV: ", IV2)
print()

prikey_Bob = RSA.import_key(open("private_key_Bob.bin", "rb").read())
cipher_RSA_Bob = PKCS1_OAEP.new(prikey_Bob)
key2 = cipher_RSA_Bob.decrypt(enc_key_part)
print("Received Key: ", key2)
print()


file_in = open("enc_msg.bin","rb")
enc_msg_bob = file_in.read()
file_in.close()

cipher_Bob = AES.new(key2, AES.MODE_CBC, IV2)
msg_with_hash_bob = unpad(cipher_Bob.decrypt(base64.b32decode(enc_msg_bob)), AES.block_size)
# base64 decoding + CBC/OFB/CTR 모드인 경우 언패딩 수행
print("Msg_with_hash_bob: ", msg_with_hash_bob)

hash_part = msg_with_hash_bob[:32] #SHA256.digest_size == 32bytes
msg_part = msg_with_hash_bob[32:]

hash_Bob = SHA256.new(msg_part)
if hash_part == hash_Bob.digest():
    print()
    print("Correct")
    print("Received MSG: ", msg_part.decode())