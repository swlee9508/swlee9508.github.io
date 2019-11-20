from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15 # 디지털 서명 생성 라이브러리 호출
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
msg = b"test message"


priKey_Alice = RSA.import_key(open("private_key_My.bin", 'rb').read())
singnature_Alice = pkcs1_15.new(priKey_Alice) # 엘리스의 디지털 서명 펑션 생성

msg_hash = SHA256.new(msg) # 메세지의 해쉬값 생성

signature = singnature_Alice.sign(msg_hash) # 앨리스의 사인 값 생성(해쉬 메세지 필요)

print("singature value: ", signature)
print("length of signature:", len(signature))# 서명의 바이트 길이

public_Key_Bob = RSA.import_key(open("public_key_Bob.bin", 'rb').read())
cipher_RSA_Alice = PKCS1_OAEP.new(public_Key_Bob)
enc_msg = cipher_RSA_Alice.encrypt(msg)


file_out = open("singature_and_enc_by_Alice.bin", 'wb')
file_out.write(signature + enc_msg)
file_out.close()
