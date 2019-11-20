from Crypto import Random
from Crypto.Cipher import AES
import os

BLOCK_SIZE = 16
KEY_SIZE=32

key = os.urandom(KEY_SIZE)
IV = Random.new().read(BLOCK_SIZE)

message = b"Information Security & Programming. Test Message!...."
print("key: ", key)
print("key length: ", len(key))

def AESencrypt(message, passphrase):
    cipher = AES.new(passphrase, AES.MODE_CFB, IV)
    print(cipher)
    return cipher.encrypt(message)

def AESdecrypt(encrypted, passphrase):
    cipher = AES.new(passphrase, AES.MODE_CFB, IV)
    return cipher.decrypt(encrypted)

encrypted = AESencrypt(message, key)
print("Encrypted: ", encrypted)

decrypted = AESdecrypt(encrypted, key)
print("Decrypted: ", decrypted.decode('utf-8'))
