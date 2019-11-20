from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

file_in = open("Password.bin", "rb")
Password = file_in.read()
file_in.close()

file_in = open("private_key_Bob.bin", "rb")
temp = file_in.read()
file_in.close()

file_in = open("enc_msg_to_Bob.bin", "rb")
enc_msg_to_Bob = file_in.read()
file_in.close()

prikey_bob = RSA.import_key(temp)
cipher = PKCS1_OAEP.new(prikey_bob)
enc_msg = cipher.decrypt(enc_msg_to_Bob)

Pw_part = enc_msg[:8]
msg_part = enc_msg[8:]

if Pw_part == Password:
    print("Correct")
    print("MSG : ", msg_part.decode())
else:
    print("Incorrect")
