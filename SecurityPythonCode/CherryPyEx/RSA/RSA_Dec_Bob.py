#======201558060 이상욱 복호화 과제==========
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

file_in = open("private_key_Bob.bin",'rb')
temp = file_in.read()
file_in.close()

#======================================
prikey_Bob = RSA.import_key(temp)
cipher_RSA_Bob = PKCS1_OAEP.new(prikey_Bob)

file_in = open("encrypted_data_from_Alice_to_Bob.bin",'rb')
enc_msg_from_Alice = file_in.read()
file_in.close()

dec_msg = cipher_RSA_Bob.decrypt(enc_msg_from_Alice)
print(dec_msg.decode())


## compect....(예외 처리)
try:
    cipher_RSA_Bob = PKCS1_OAEP.new(RSA.import_key(open("private_key_Bob.bin", 'rb').read()))
except:
    print("Error... Private key of Bob!")

try:
    print(cipher_RSA_Bob.decrypt(open("encrypted_data_from_Alice_to_Bob.bin",'rb').read()).decode())
except:
    print("Without Enc_Data!!")

