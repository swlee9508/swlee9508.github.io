from Crypto.PublicKey import RSA

# ================================================
# RSA Public_Key & Private_Key 생성 과정 (secret_code 설정)
print("******RSA Public_Key & Private_Key 생성 과정 (secret_code 설정)")
secret_code = "Unguessable"
key = RSA.generate(2048)
encrypt_key = key.export_key(passphrase=secret_code, pkcs=8, protection="scryptAndAES128-CBC")
file_out = open("rsa_key.bin", "wb")
file_out.write(encrypt_key)
print(key.publickey().export_key())  # 생성된 Public_key
print(key.publickey())  # 생성된 Public_key Object
print(key.export_key())  # 생성된 Private_key
file_out.close()

# ================================================
# 생성된 RSA Public_Key 읽어들이는 과정 (secret_code 설정)
print("\n\n******생성된 RSA Public_Key 읽어들이는 과정 (secret_code 설정)")
secret_code = "Unguessable"
encoded_key = open("rsa_key.bin", "rb").read()
key = RSA.import_key(encoded_key, passphrase=secret_code)
print(key.publickey().export_key())  # 생성된 Public_key
print(key.publickey())  # 생성된 Public_key Object
print(key.export_key())  # 생성된 Private_key

# ================================================
# RSA Public_Key & Private_Key 생성 과정 (secret_code 설정하지 않고 진행하는 방법)
# Alice 부분
from Crypto.PublicKey import RSA

key = RSA.generate(2048)
private_key = key.export_key()    # Alice의 Private_Key
file_out = open("private_Alice.pem", "wb")
file_out.write(private_key)
file_out.close()

public_key = key.publickey().export_key()
file_out = open("public_Alice.pem", "wb")   # Alice의 Public_Key
file_out.write(public_key)
file_out.close()


# ==================================
# Encrypt data with RSA (Only RSA)
# Bob이 Alice에게 메시지를 전송하고자 하는 과정
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

print("\n\n******Encrypt data with RSA (Only RSA)")
print("#Step1: Bob은 Alice의 Public_Key를 이용하여 메시지를 암호화하여 전송")

# Bob이 Alice에게 전송하고자 하는 메시지..
data = "RSA Encryption and Decryption Test.....".encode("utf-8") # 전송하고자 하는 메시지
print("Bob이 전송하고자 하는 메시지:",data)
# Bob은 Alice의 공개키를 받음 (웹 페이지를 통해 받을 수 있음)
recipient_public_key = RSA.import_key(open("public_Alice.pem").read()) # Alice의 Public_Key를 읽어들임
print("Alice Public_Key:", recipient_public_key.export_key())  # Alice의 Public_key가 제대로 읽혀졌는지 확인
cipher_rsa = PKCS1_OAEP.new(recipient_public_key) # recipient_public_key를 이용하여 암호화할 수 있는 cipher 생성
encrypted_message = cipher_rsa.encrypt(data) # recipient_public_key를 이용하여 암호화 과정 수행
print("Bob이 암호문을 웹/네트워크로 파일 전송:", encrypted_message)
# encrypted_message 아래 이름의 파일로 생성하여 네트워크를 통해 전송하였다고 가정..
file_out = open("encrypted_data_from_Bob.bin", "wb")  # 암호문을 파일로 저장/전송함
file_out.write(encrypted_message)
file_out.close()

print("\n#Step2: Alice는 자신의 Private_Key를 이용하여 메시지 복호화")

encrypted_message = open("encrypted_data_from_Bob.bin", "rb").read()  # 수신/저장된 암호문 파일을 읽어들임
recipient_private_key = RSA.import_key(open("private_Alice.pem", "rb").read()) # Alice의 Private_Key를 읽어들임
print("Alice Private_Key:", recipient_private_key.export_key())  # Alice의 Private_Key가 제대로 읽혀졌는지 확인
cipher_rsa = PKCS1_OAEP.new(recipient_private_key)  # recipient_private_key를 이용하여 복호화할 수 있는 cipher 생성
decrypted_message = cipher_rsa.decrypt(encrypted_message) # recipient_private_key를 이용하여 복호화 과정 수행
print("Alice가 수신한 메시지:",decrypted_message) # 복호화된 메시지를 출력함


# ===========================
# Encrypt data with RSA + AES
# Bob이 Alice에게 메시지를 전송하고자 하는 과정
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

print("\n\n******Encrypt data with RSA + AES")
print("#Step1: Bob은 Alice의 Public_Key를 이용하여 세션키를 암호화, AES 이용하여 메시지를 암호화하여 전송")

# Bob이 Alice에게 전송하고자 하는 메시지..
data = "This is message from Bob to Alice Using RSA + AES.".encode("utf-8") # 전송하고자 하는 메시지
print("Bob이 전송하고자 하는 메시지:",data)
# Bob은 Alice의 공개키를 받음 (웹 페이지를 통해 받을 수 있음)
recipient_public_key = RSA.import_key(open("public_Alice.pem").read())
session_key = get_random_bytes(16)
print("난수로 선택된 session_key:", session_key)
# Encrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(recipient_public_key) # 수신자의 공개키를 이용하여 암호화하는 RSA cipher
enc_session_key = cipher_rsa.encrypt(session_key)

# Encrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX) # 생성된 세션키를 이용하여 암호화하는 AES cipher
ciphertext, tag = cipher_aes.encrypt_and_digest(data) # 전송하고자 하는 데이터를 입력하여 암호화 및 해쉬값 생성

file_out = open("encrypted_data_RSA_AND_AES.bin", "wb")  # 전송한 것을 파일로 저장해 놓음
file_out.write(enc_session_key + cipher_aes.nonce + tag + ciphertext)
file_out.close()

print("len enc_session_key:", len(enc_session_key))
print("len cipher_aes.nonce:", len(cipher_aes.nonce))
print("len tag:", len(tag))
print("len ciphertext:", len(ciphertext))

# Receiver : Alice
print("\n#Step2: Alice는 자신의 Private_Key를 이용하여 메시지 복호화")

encrypted_message = open("encrypted_data_RSA_AND_AES.bin", "rb").read()
enc_session_key = encrypted_message[:256] # 암호문의 0~256 부분
cipher_aes.nonce = encrypted_message[256:256+len(cipher_aes.nonce)]
tag = encrypted_message[256+len(cipher_aes.nonce):256+len(cipher_aes.nonce)+16]
ciphertext = encrypted_message[256+len(cipher_aes.nonce)+16:]
print("session_key:", session_key)
print("cipher_aes.nonce:", cipher_aes.nonce)
print("tag:", tag)
print("ciphertext:", ciphertext)

recipient_private_key = RSA.import_key(open("private_Alice.pem").read())
cipher_rsa = PKCS1_OAEP.new(recipient_private_key) # 수신자의 개인키를 이용하여 복호화하는 RSA cipher
session_key = cipher_rsa.decrypt(enc_session_key) # 수신자의 개인키를 이용하여 암호화된 세션키를 복호화함
print("Decrypted Session Key:", session_key)
cipher_aes = AES.new(session_key, AES.MODE_EAX, cipher_aes.nonce) # 복호화된 세션키, nonce값을 이용하여, 복호화 과정을 수행하는 AES cipher
decrypted_message = cipher_aes.decrypt_and_verify(ciphertext, tag)  # 암호화된 ciphertext, 해쉬값 tag 를 입력하여 복호화 및 검증 과정 수행
print("수신된 메시지:",decrypted_message)

# ================================================
## Pycryptodome Utility Function Test

from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from Crypto.Util.number import GCD, getPrime, inverse, isPrime
print("\n\n******Pycryptodome Utility Function Test")
data = b'Unaligned'   # 9 bytes
key = get_random_bytes(AES.key_size[2])  # AES.key_size == (16, 24, 32); AES.key_size[2] == 32
iv = get_random_bytes(AES.block_size)   # AES.block_size == 16
cipher1 = AES.new(key, AES.MODE_CBC, iv)
ct = cipher1.encrypt(pad(data, AES.block_size))

cipher2 = AES.new(key, AES.MODE_CBC, iv)
pt = unpad(cipher2.decrypt(ct), AES.block_size)
assert(data == pt), 'Not equal...'    # 일치할 경우 표시 없음.. 만일 다를 경우 'Not equal...' 출력

data_padded = pad(data, AES.block_size)
assert(data == unpad(data_padded, AES.block_size)), 'Not equal...'

def ISPrime(n):
    return "True" if isPrime(n) else "False"

print("is 7 prime? ", ISPrime(7))

print("multiplicative Inverse 7 in mod 13: ", inverse(7, 13))
print("GCD (7,13): ", GCD(7,13))
print("Get Prime Number: ", getPrime(16))

## CherryPy + Pycryptodome 구현해볼만한 내용

## File Upload + Encryption/Decryption (Symmetric : AES) + on Web
# 대칭키 기반, Alice가 자신이 전송하고자 하는 파일을 CherryPy 웹으로 업로드: 대칭키 기반 파일 업로더 웹 시스템
# Alice : Client,  Bob : Server
# Alice는 Bob 서버에 Secret 값을 저장해 놓음
# Alice : Bob이 홈페이지를 통해 생성한 난수 값을 확인함
# Alice : 난수값과 서버에 이미 저장해 놓은 Secret 값을 이용하여 일회용 세션키(대칭키)를 생성
# Alice : 제출하고자 하는 파일을 대칭키로 암호화함, 그리고 이를 웹으로 업로드함
# Bob : 난수 값과 Alice가 등록해 놓은 Secret을 이용하여 일회용 세션키(대칭키)를 생성함
# Bob : Alice가 업로드된 파일을 복호화 함...

## File Upload + Encryption/Decryption (Asymmetric : RSA) + on Web
# 공개키 기반, Alice가 자신이 전송하고자 하는 파일을 CherryPy 웹으로 업로드: 공개키 기반 파일 업로더 웹 시스템
# Alice : Client,  Bob : Server
# Alice : Bob(Server)의 공개키를 다운로드 받음
# Alice : 제출하고자 하는 파일을 Bob의 공개키로 암호화함, 그리고 이를 웹으로 업로드함
# Bob : 업로드된 파일에 대해 Bob 자신의 개인키를 이용하여 복호화 함...
# 업로드하고자 하는 파일의 종류 : BMP 이미지, PNG 이미지 파일, PDF 파일 등...
# Bob : 업로드된 파일을 웹 페이지에 출력 (이미지 파일인 경우)
# 추후 .. 블록체인 시스템 (간단한 시스템)으로도 발전시킬 수 있음??

## Secret 게시판 + Encryption/Decryption (Asymmetric : RSA) + on Web
# 공개키 기반, Alice가 CherryPy 웹 페이지 내에 글을 작성하고 안전하게 저장: 공개키 기반 Secret 게시판 웹 시스템


## Encrypted File Decryption (Brute Force) on Web

## Hash DB ?? on Web
