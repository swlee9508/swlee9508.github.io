from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

## Alice(Client) : 서명 생성자, 생성된 Signature를 Bob에게 전송 (또는 CherryPy로 업로드)
print("Alice(Client) : 서명 생성자, 생성된 Signature를 Bob에게 전송 (또는 CherryPy로 업로드)")
message = 'To be signed.......'
print("Sent Message:", message)
key = RSA.import_key(open('private_Alice.pem').read())
h = SHA256.new(message.encode())
print("Message Hash:", h.digest())
signature = pkcs1_15.new(key).sign(h)  # 해쉬값에 대한 서명을 생성함 (디지털서명 생성을 위해 pkcs1_15 사용
print("Signature:", signature)
print("Signature len: %d bytes" % len(signature))
file_out = open("signature_with_message.bin", "wb")  # Signature + message 순서로 저장
file_out.write(signature + message.encode())
file_out.close()

## Bob(Server) : 서명 확인/검증자, 업로드된 Signature를 확인/검증함 (또는 CherryPy로 업로드)
## Alice의 공개키와 file(Signature+Message)을 함께 업로드함..
print("\nBob(Server) : 서명 확인/검증자, 업로드된 Signature를 확인/검증함 (또는 CherryPy로 업로드)")
key = RSA.import_key(open('public_Alice.pem').read())
file_in = open("signature_with_message.bin","rb")
uploaded_data = file_in.read()
received_signature = uploaded_data[:SHA256.digest_size]   # SHA256.digest_size == 256
print("Received Signature:", received_signature)
received_messsge = uploaded_data[SHA256.digest_size:]
file_in.close()
h = SHA256.new(received_messsge)
print("Received Message Hash:", h.digest())
try:
    pkcs1_15.new(key).verify(h, received_signature)
    print("The signature is valid.")
    print("Received Message:", received_messsge.decode())
except (ValueError, TypeError):
    print("The signature is not valid.")
