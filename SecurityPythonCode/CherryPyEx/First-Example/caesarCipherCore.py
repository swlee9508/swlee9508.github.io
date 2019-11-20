def encrypt(message,key,LETTERS):
    encrypt_message=''
    for symbol in message:
        if symbol in LETTERS:
            num = ( LETTERS.find(symbol) + key ) % (len(LETTERS))
            encrypt = LETTERS[num]
        else:
            encrypt = symbol
        encrypt_message = encrypt_message + encrypt
    return encrypt_message

def decrypt(encrypt_message,key,LETTERS):
    decrypt_message=''
    for symbol in encrypt_message:
        if symbol in LETTERS:
            num = ( LETTERS.find(symbol) - key ) % (len(LETTERS))
            decrypt = LETTERS[num]
        else:
            decrypt = symbol
        decrypt_message = decrypt_message + decrypt
    return decrypt_message
