from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

# ================================================
# RSA Public_Key & Private_Key 생성 과정 (My.....)
print("******RSA Public_Key & Private_Key 생성 과정 (secret_code 설정)")

cipher_RSA = RSA.generate(2048)# 2048 은 기준 비트수
private_key = cipher_RSA.export_key() # 이 줄을 실행 시킬 때 나오는 정보는 프라이빗 키를 끄집어 내는 것이다.
print(private_key) # 화면에 출력
file_out = open("private_key_My.bin", "wb")# "private_key_My.bin" 이름으로 파일 생성
file_out.write(private_key) # "private_key_My.bin" 이 파일에 작성
file_out.close() # 작성 종료

public_key = cipher_RSA.publickey().export_key() # 이줄을 실행 시키면 위의 값의 대한 퍼블릭 키 생성
print(public_key)
file_out = open("public_key_My.bin","wb")
file_out.write(public_key)
file_out.close()

# ===============================================
#BoB....

cipher_RSA_Bob = RSA.generate(2048)
private_key_Bob = cipher_RSA_Bob.export_key()
print("Bob 의 프라이베이트 키",private_key_Bob)
print()
file_out = open("private_key_Bob.bin", "wb") # write binary mode
file_out.write(private_key_Bob)
file_out.close()

public_key_Bob = cipher_RSA_Bob.publickey().export_key()
print("Bob 의 퍼블릭 키",public_key_Bob)
print()
file_out = open("public_key_Bob.bin", "wb") # write binary mode
file_out.write(public_key_Bob)
file_out.close()



