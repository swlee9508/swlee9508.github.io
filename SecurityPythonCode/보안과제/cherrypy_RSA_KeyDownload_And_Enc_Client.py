from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

print("\n\n******Encrypt data with RSA (Only RSA)")
print("#Step1: Alice는 Web Server(Bob)로 부터 다운받은 Public_Key를 이용하여 전송하고자 하는 메세지를 암호화")

#Alice가 Bob에게 전송하고자 하는 메시지..
data = "[From Alice] RSA Encryption and Decryption Test...............".encode("utf-8")
print("Alice가 전송하고자 하는 메시지: ", data)
#Bob은 Alice의 공개키를 받음 (웹 페이지를 통해 받을 수 있음)
recipient_public_key = RSA.import_key(open("public_WebServer.bin").read())
print("Web Server's Public_Key: ", recipient_public_key.export_key())
cipher_rsa = PKCS1_OAEP.new(recipient_public_key)
encrypted_message = cipher_rsa.encrypt(data)

#파일 전송시 Base64로 인코딩해서 전송
encrypted_message_base64 = base64.b32encode(encrypted_message)

print("#Step2: Alice는 생성된 암호화 파일을 Web Server(Bob)에 업로드하여 전송")
print("Alice가 전송하고자 하는 암호문 (웹/네트워크로 파일 업로드 전송): ", encrypted_message_base64)
#encrypted_message 아래 이름의 파일로 생성하여 네트워크를 통해 전송하였다고 가정..
file_out = open("encrypted_data_from_Alice.bin", "wb") # 암호문을 파일로 저장/전송함
file_out.write(encrypted_message_base64)
file_out.close()