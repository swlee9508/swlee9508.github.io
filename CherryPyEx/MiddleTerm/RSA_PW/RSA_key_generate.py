from Crypto.PublicKey import RSA

#=== 밥의 public,private_key 생성===#
cipher_Bob = RSA.generate(2048)
private_key_Bob = cipher_Bob.export_key()
file_in = open("private_key_Bob.bin","wb")
file_in.write(private_key_Bob)
file_in.close()

public_key_Bob = cipher_Bob.publickey().export_key()

file_in = open("public_key_Bob.bin","wb")
file_in.write(public_key_Bob)
file_in.close()

#=== 엘리스의 public,private_key 생성===#
cipher_Alice = RSA.generate(2048)
private_key_Alice = cipher_Alice.export_key()

file_in = open("private_key_Alice.bin","wb")
file_in.write(private_key_Alice)
file_in.close()

public_key_Alice = cipher_Alice.publickey().export_key()

file_in = open("public_key_Alice.bin","wb")
file_in.write(public_key_Alice)
file_in.close()