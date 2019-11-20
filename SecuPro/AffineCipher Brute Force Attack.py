import random
import string

from cryptomath import gcd, findModInverse

LETTERS = string.ascii_letters


#아핀 암호 기능 구현
# input : LETTERS
# output : RRS Z*_Letter
def findReducedResidueSet(LETTERS): #기약 잉여류 찾는 함수
    RRS = [] # 기약잉여류 집합....
    for c in range(1, len(LETTERS)):
        if (gcd(c, len(LETTERS)) == 1): #GCD 가 서로소인 원소
            RRS.append(c)
    return RRS

# 평문 암호화 아핀 암호
def AffineEnc(plaintext, key1, key2):
    ciphertext = ''
    for c in plaintext:
        if c in LETTERS:
            cipherIndex = LETTERS.find(c)
            ciphertext += LETTERS[(cipherIndex * key1 + key2) % len(LETTERS)]
        else:
            ciphertext += c
    return ciphertext

# 평문 복호화 아핀 암호
def AffineDec(ciphertext, key1, key2):
    plaintext = ''
    for p in ciphertext:
        if p in LETTERS:
            planIndex = LETTERS.find(p)
            plaintext += LETTERS[(planIndex - key2) * findModInverse(key1, len(LETTERS)) % len(LETTERS)]
        else:
            plaintext += p
    return plaintext

# 암모문의 전사 공격 기능 구현
def AffineCipherBFA(ciphertext, LETTERS):
    plaintext = ''
    RRS = findReducedResidueSet(LETTERS)
    for key1 in RRS:
        for key2 in range(len(LETTERS)):
            plaintext = AffineDec(ciphertext, key1, key2)
            print("key1 :", key1, "key2 :", key2, "예상된 평문 :", plaintext)

if __name__ == "__main__":

    plaintext = "This is an information security class 2019. Hanshin University"

    RRS = findReducedResidueSet(LETTERS)

    key1 = RRS[random.randrange(0, len(RRS))] # RRS 의 원소중 한개 랜덤 선택
    print("key1 : ", key1)

    key2 = random.randrange(0, len(LETTERS))
    print("key2 : ", key2)
#  AffineEnc/Dec
    ciphertext = AffineEnc(plaintext, key1, key2)
    print("암호문 : ", ciphertext)

    plaintext2 = AffineDec(ciphertext, key1, key2)
    print("평문 : ", plaintext2)

    print()

    AffineCipherBFA(ciphertext, LETTERS)
