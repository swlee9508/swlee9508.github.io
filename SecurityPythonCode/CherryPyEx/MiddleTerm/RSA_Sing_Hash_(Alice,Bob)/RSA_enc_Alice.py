from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP

#===bob의 public_key로 암호문 생성===#

file_out = open("public_key_bob.bin","rb")
temp = file_out.read()
file_out.close()

msg = "hello world"

pubKey_bob = RSA.import_key(temp)
cipher_bob = PKCS1_OAEP.new(pubKey_bob)

enc_msg = cipher_bob.encrypt(msg.encode())

file_in = open("enc_msg_to_Bob.bin", "wb")
file_in.write(enc_msg)
file_in.close()

#===Alice 의 private_key로 서명값 생성 후 해쉬의 서명===#

file_out = open("private_key_Alice.bin", "rb")
temp_Alice = file_out.read()
file_out.close()

hashResult = SHA256.new(msg.encode())
prikey_Alice = RSA.import_key(temp_Alice)

Signature_Alice = pkcs1_15.new(prikey_Alice)
Sign_Alice = Signature_Alice.sign(hashResult)

file_in = open("Sign_hash_from_Alice.bin", "wb")
file_in.write(Sign_Alice + hashResult.digest())
file_in.close()