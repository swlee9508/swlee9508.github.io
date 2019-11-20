from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random

public_Password = Random.new().read(8)

file_out = open("Password.bin", "wb")
file_out.write(public_Password)
file_out.close()

msg = b"hello world"

file_in = open("public_key_Bob.bin", "rb")
temp = file_in.read()
file_out.close()

pubkey_bob = RSA.import_key(temp)
cipher = PKCS1_OAEP.new(pubkey_bob)
enc_msg = cipher.encrypt(public_Password + msg)

file_out = open("enc_msg_to_Bob.bin", "wb")
file_out.write(enc_msg)
file_out.close()