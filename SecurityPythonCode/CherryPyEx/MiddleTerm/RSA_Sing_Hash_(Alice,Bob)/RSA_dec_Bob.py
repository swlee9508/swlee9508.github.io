from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

#=== 밥의 복호화 ===#
file_out = open("private_key_Bob.bin", "rb")
temp_bob = file_out.read()
file_out.close()

priBob = RSA.import_key(temp_bob)

file_out = open("enc_msg_to_Bob.bin", "rb")
enc_msg_bob = file_out.read()
file_out.close()

cipher_Bob = PKCS1_OAEP.new(priBob)
dec_msg = cipher_Bob.decrypt(enc_msg_bob)

hashResult = SHA256.new(dec_msg) # 복호화 된 메세지 해쉬값 생성

#=== 서명 검증 ===#
file_out = open("Sign_hash_from_Alice.bin", "rb")
Sign_hash_from_Alice = file_out.read()
file_out.close()

Sign_part = Sign_hash_from_Alice[:256]
hash_part = Sign_hash_from_Alice[256:]

file_out = open("public_key_Alice.bin", "rb")
pubkey_Alice = file_out.read()
file_out.close()

pubkey = RSA.import_key(pubkey_Alice)
Signature = pkcs1_15.new(pubkey)

try:
    Signature.verify(hashResult,Sign_part)
    print("Correct")
    print("MSG : ", dec_msg.decode())
except:
    print("INCorrect")