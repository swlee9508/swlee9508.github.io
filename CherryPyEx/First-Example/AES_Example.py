from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes # 키 만들때 필요한 랜덤 바이트 값 생성 라이브러리 호출 방법
from Crypto import Random
import base64
from Crypto.Util.Padding import pad, unpad # 패딩/언패딩 관련 라이브러리 추가

BLOCK_SIZE = AES.block_size
KEY_SIZE = AES.key_size[2] # AES.key_size 는 (16, 24, 32) 세가지의 튜플 값이 있기 때문에 그 위치를 설정 해준다.
IV = Random.new().read(BLOCK_SIZE) # 블록 사이즈 만큼 IV 값 랜덤 생성

key = get_random_bytes(KEY_SIZE) # KEY_SIZE 만큼 랜덤 바이트 키 생성 방법
print()
print("key : ", key)
print("key size : ", len(key))

plaintext = "Information Security with Python....."

def AES_Enc(key,message): # AES 메서드 생성
    cipher = AES.new(key, AES.MODE_CFB, IV) # 주의할 점 오브젝트 한번 사용후 재사용 불가
    return base64.b32encode(cipher.encrypt(pad(message.encode(),16))).decode() # pad(16바이트로 패딩으로 시켜준다.)

def AES_Dec(key,message):
    cipher = AES.new(key, AES.MODE_CFB, IV)
    return unpad(cipher.decrypt(base64.b32decode(message.encode())),16).decode() # unpad(패딩 받은것을 다시 돌려준다.)

output_enc = AES_Enc(key, plaintext)
output_dec = AES_Dec(key, output_enc)

print(output_enc)
print(output_dec)


#base64.b32encode 를 실행하면 암호화 된 값이 아스킷 코드 문자로 변경되고
#그 후 .decode() 를 해주면 스트링 값으로 변경된다.





