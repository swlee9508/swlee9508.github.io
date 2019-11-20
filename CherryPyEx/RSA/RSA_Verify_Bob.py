from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15 # 디지털 서명 생성 라이브러리 호출
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

msg_from_Alice = open("singature_by_Alice.bin", 'rb').read()

sig_part = msg_from_Alice[:256] # 서명 길이가 256 이기 때문에 0~255 까지 자르기
msg_part = msg_from_Alice[256:] # 나머지 뒷부분은 보낸 메세지

pubKey_Alice = RSA.import_key(open("public_key_My.bin", 'rb').read())
singnature_Bob = pkcs1_15.new(pubKey_Alice) # 엘리스의 디지털 서명 검증 펑션 생성

msg_hash = SHA256.new(msg_part) # 메세지의 해쉬값 생성

try:
    singnature_Bob.verify(msg_hash,sig_part) # 앨리스의 사인 값 검증 과정
    print("Correct !! Received MSG: ", msg_part.decode())
except:
    print("Incorrect!!")