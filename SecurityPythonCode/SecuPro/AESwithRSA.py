
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random

plaintext = b'abcdef0123456789'
print("PlainText: ", plaintext)

## generate Session Key using Random function
sessionKey = Random.new().read(16)
print("Generated Session Key: %s" % sessionKey)
## AES encrypt using sessionKey & iv
iv = Random.new().read(AES.block_size)
print("IV, plaintext : %s, %s" %(iv, plaintext))
aesAlice = AES.new(sessionKey, AES.MODE_CFB, iv)
encMSG = iv + aesAlice.encrypt(plaintext)

## generate RSA public Key and private Key (for Bob : Receiver)
rsa  = RSA.generate(2048)
priKey = rsa.exportKey('PEM')  # priKey : private key
print("private key: %s" % priKey)
pubKey = rsa.publickey()  # pubKey : public key
print("public key: %s" % pubKey)
print(pubKey.exportKey('PEM'))

rsaAlice = PKCS1_OAEP.new(pubKey)
encSSK = rsaAlice.encrypt(sessionKey)
print("encrypted session key: %s" % encSSK)
print(len(encSSK))  # length 256 bytes
outputAlice = encSSK + encMSG  # concatenate encrypted SSK + encrypted MSG
print("output: %s" % outputAlice)

###### sending output to Bob...

## decrypt session key
SESSION_KEY_SIZE = len(encSSK)
priKey = RSA.importKey(priKey)
rsaBob = PKCS1_OAEP.new(priKey)
sessionKey = rsaBob.decrypt(outputAlice[:SESSION_KEY_SIZE])
print("Decrypted Session Key: %s" % sessionKey)

## decrypt message using session key
ciphertext = outputAlice[SESSION_KEY_SIZE:]
iv2 = ciphertext[:AES.block_size]  # AES.block_size == 16
aesBob = AES.new(sessionKey, AES.MODE_CFB, iv2) # decrypt using session key
plaintext = aesBob.decrypt(ciphertext[AES.block_size:])
print("Plaintext: %s" % plaintext)