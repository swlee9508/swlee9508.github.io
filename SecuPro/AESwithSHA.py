from Crypto.Cipher import AES
from Crypto.Hash import SHA
from Crypto import Random

# Encrypt

key = b'sixteen byte key'
iv = Random.new().read(AES.block_size)
plaintext = b'attack at dawn'
print("Key, iv, plaintext : %s, %s, %s" %(key, iv, plaintext))

h = SHA.new()
h.update(plaintext)
hashOfMSG = h.digest()

plaintextWithHash = hashOfMSG + plaintext
print("plaintextWithHash : %s" %(plaintextWithHash))

cipher = AES.new(key, AES.MODE_CFB, iv)
msg = iv + cipher.encrypt(plaintextWithHash)
print("Ciphertext : %s" %(msg))

# Decrypt

print()
key = b'sixteen byte key'
iv2 = msg[:16]
print("Key, iv : %s, %s" %(key, iv2))

cipher2 = AES.new(key, AES.MODE_CFB, iv2)

plaintextWithHash2 = cipher2.decrypt(msg[16:])
print("plaintextWithHash2 : %s" %(plaintextWithHash2))
hashOfMSG2 = plaintextWithHash2[:20]
print("hashOfMSG2 : %s" %(hashOfMSG2))

h2 = SHA.new()
h2.update(plaintextWithHash2[20:])
hashOfMSG3 = h2.digest()
print("hashOfPlaintext : %s" %(hashOfMSG3))

if hashOfMSG3 == hashOfMSG2:
    print("Integrity Check OK!")
    print("Decrypted Message: %s" %(plaintextWithHash2[20:]))
else:
    print("Incorrect Hash!!")