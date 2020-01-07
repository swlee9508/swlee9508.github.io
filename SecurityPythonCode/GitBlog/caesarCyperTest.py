import random
import string

LETTERS = string.ascii_letters

# 암호화 기능 구현
# input : LETTERS, plaintext, key
# output : ciphertext
def caesarEnc(LETTERS, plaintext, key):
    ciphertext = ''
    for c in plaintext:
        if c in LETTERS:
            ciphertext += LETTERS[(LETTERS.find(c) + key) % len(LETTERS)]
        else:
            ciphertext += c
    return ciphertext

# 복호화 기능 구현
# input : LETTERS, ciphertext, key
# output : plaintext
def caesarDec(LETTERS, ciphertext, key):
    plaintext = ''
    for c in ciphertext:
        if c in LETTERS:
            plaintext += LETTERS[(LETTERS.find(c) - key) % len(LETTERS)]
        else:
            plaintext += c
    return plaintext

if __name__ == "__main__":

    plaintext = "Hello my name is FLant haha hoho!!!"

    key = random.randrange(0, len(LETTERS))
    print("Selected key(생성된 랜덤 키): ", key)

    ciphertext = caesarEnc(LETTERS, plaintext, key)
    print("생성된 암호문 : ", ciphertext)

    replaintext = caesarDec(LETTERS, ciphertext, key)
    print("다시 복호화 된 평문 : ", replaintext)