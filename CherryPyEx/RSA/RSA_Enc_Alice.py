from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP # 키에 대한 정보로 사이퍼 를 만들 수 있다.
# ===============================================
# 생성된 RSA Public_key_Bob.bin 파일을 읽어들이는 과정(Alice..)
# 웹상의 밥에 공개키를 불러들인다고 가정

file_in = open("public_key_Bob.bin",'rb')
temp = file_in.read()
file_in.close()


#========= Alice 의 사이퍼 키 생성 =========

pubkey_Bob = RSA.import_key(temp)
### cipher_RSA = RSA.generate(2048)
cipher_RSA = PKCS1_OAEP.new(pubkey_Bob)  # 불러드린 공개키를 이용해서 암호키를 만든다.

message = b"test message"
enc_msg = cipher_RSA.encrypt(message)
print(enc_msg)

file_out = open("encrypted_data_from_Alice_to_Bob.bin","wb")
file_out.write(enc_msg)
file_out.close()

