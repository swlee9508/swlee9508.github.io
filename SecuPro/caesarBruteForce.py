import random
import string

from cryptomath import gcd, findModInverse
from detectEnglish import isEnglish

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

#input : LETTER, ciphertext, ????(key 는 모른다.)
#output : decrypted plaintext
def caesarHack(LETTERS, ciphertext):
    for key in range(len(LETTERS)):
        plaintext = caesarDec(LETTERS, ciphertext, key)
        print("key :",key , "Decplaintext: ",plaintext)


#아핀 암호 기능 구현
# input : LETTERS
# output : RRS
def findReducedResidueSet(LETTERS): #기약 잉여류 찾는 함수
    RRS = []
    for c in range(1,len(LETTERS)):
        if (gcd(c, len(LETTERS)) == 1):
            RRS.append(c)
    return RRS

#input : LETTERS, plaintext, key1, key2
#output : ciphertext
def affineEnc(LETTERS, plaintext, key1, key2):
    ciphertext =''
    for c in plaintext:
        if c in LETTERS:
            ciphertext += LETTERS[((LETTERS.find(c)*key1)+key2)%len(LETTERS)]
        else:
            ciphertext += c
    return ciphertext

#List로 구현(암호화)
#input : LETTERS, plaintext, key1, key2
#output : ciphertext
def affineEnc2(LETTERS, plaintext, key1, key2):
    ciphertext = []
    for c in plaintext:
        if c in LETTERS:
            ciphertext += LETTERS[((LETTERS.find(c)*key1)+key2)%len(LETTERS)]
        else:
            ciphertext += c
    return ''.join(ciphertext)

#input : LETTERS, ciphertext, key1, key2
#output : plaintext
def affineDec(LETTERS, ciphertext, key1, key2):
    plaintext =''
    for c in ciphertext:
        if c in LETTERS:
            plaintext += LETTERS[((LETTERS.find(c) - key2) * findModInverse(key1, len(LETTERS))) % len(LETTERS)]
        else:
            plaintext += c
    return plaintext

#input : LETTER, ciphertext, ????, ????(key 는 모른다.)
#output : decrypted plaintext

def affineHack(LETTERS, ciphertext):
    guessed_RRS = findReducedResidueSet(LETTERS)
    for key1 in guessed_RRS:
        for key2 in range(len(LETTERS)):
            guessed_plaintext = affineDec(LETTERS,ciphertext,key1,key2)
            print("key 1 :", key1, "key 2 :", key2, "예상된 평문 :", guessed_plaintext)

#input : ????(LETTERS 도 모른다고 가정하면??), ciphertext, ????, ????(key 는 모른다.)
#output : decrypted plaintext
def affineHackAutoDetect(LETTERS, ciphertext): # 자동 공격(필요한 문만 출력)
    guessed_RRS = findReducedResidueSet(LETTERS)
    for key1 in guessed_RRS:
        for key2 in range(len(LETTERS)):
            guessed_plaintext = affineDec(LETTERS, ciphertext, key1, key2)
            if isEnglish(guessed_plaintext, 58):
                print("key 1 :", key1, "key 2 :", key2, "예상된 평문 :", guessed_plaintext)
                return 1
    return 0

#input : Length(문자 집합의 개수??)
#output : LETTERS
def GenLETTERS(Length):
    LETTERS = ''
    specialCarSet = "!@#$%^&*()_+=[{]};:<>?/"
    LETTERSET = string.digits + specialCarSet
    RandLength = Length #random.randint(0, Length)
    for i in range(RandLength):
        LETTERS += random.choice(LETTERSET)
    #LETTERS = ''.join(random.choice(LETTERSET) for x in range(RandLength)) #LETTERS 의 리스트를 만드는 기능
    return string.ascii_letters + LETTERS

if __name__ == "__main__":

    LETTERS = string.ascii_letters + "$%"

    print(LETTERS," ",len(LETTERS))
    plaintext = "This is an information security class. 2019$%"

    key = random.randrange(0,len(LETTERS))
    print("Selected key: ", key)

    ciphertext = caesarEnc(LETTERS, plaintext,key)
    print(ciphertext)

    plaintext2 = caesarDec(LETTERS, ciphertext,key)
    print(plaintext2)

    #LETTERS를 알고 있다는 가정 하에서...

    #LETTERS2 = string.ascii_letters
    #LETTERS2 = string.ascii_uppercase
    #ciphertext2 = "R UXEN VH TRCCH"
    #caesarHack(LETTERS2, ciphertext2)

    RRS = findReducedResidueSet(LETTERS)

    key1 = RRS[random.randrange(0,len(RRS))]
    print("아핀 키 1 :", key1)
    key2 = random.randrange(0,len(LETTERS))
    print("아핀 키 2 :", key2)

    affineCipher = affineEnc(LETTERS, plaintext, key1, key2)
    print("아핀 암호 텍스트 : ", affineCipher)

    affinePlain = affineDec(LETTERS, affineCipher, key1, key2)
    print("아핀 평문 텍스트 : ", affinePlain)

    while(True):
        LETTERS = GenLETTERS(2);
        print("Generated LETTRS :", LETTERS)
        status = affineHackAutoDetect(LETTERS, affineCipher)
        if status == 1:
            break

    #affineHack(LETTERS, affineCipher)
