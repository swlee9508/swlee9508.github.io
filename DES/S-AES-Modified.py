import sys

# S-Box
sBox = [0x9, 0x4, 0xa, 0xb, 0xd, 0x1, 0x8, 0x5,
        0x6, 0x2, 0x0, 0x3, 0xc, 0xe, 0xf, 0x7]

# Inverse S-Box
sBoxI = [0xa, 0x5, 0x9, 0xb, 0x1, 0x7, 0x8, 0xf,
         0x6, 0x0, 0x2, 0x3, 0xc, 0x4, 0xd, 0xe]

# Round keys
w = [None] * 6


# function which multiplies in GF(2^4)
def mult(p1, p2):
    p = 0
    while p2:
        if p2 & 0b1:
            p ^= p1
        p1 <<= 1
        if p1 & 0b10000:
            p1 ^= 0b11
        p2 >>= 1
    return p & 0b1111


# function used to convert an 8 bit integer into a 4 element vector
def convertVector(n):
    return [n >> 12, (n >> 4) & 0xf, (n >> 8) & 0xf, n & 0xf]


# fuction used to convert a 4 element vector into 8 bit integers
def convertInteger(x):
    return (x[0] << 12) + (x[1] << 4) + (x[2] << 8) + x[3]


# function used to add two keys in GF(2^4) (s-AES)
def addKey(s1, s2):
    return [i ^ j for i, j in zip(s1, s2)]


# simple substitution function
def substitution(sbox, s):
    return [sbox[e] for e in s]


# simple function to shift the current row
def shift(s):
    return [s[0], s[1], s[3], s[2]]


# this function expands the key into subkeys, then creates the other keys
def keyExpansion(key):
    # generates the key rounds
    def sub2Nib(B):# swaps and then subsitutes the key using the above s-box
        return sBox[B >> 4] + (sBox[B & 0x0f] << 4)

    Rcon1, Rcon2 = 0b10000000, 0b00110000
    w[0] = (key & 0xff00) >> 8
    w[1] = key & 0x00ff
    w[2] = w[0] ^ Rcon1 ^ sub2Nib(w[1])
    w[3] = w[2] ^ w[1]
    w[4] = w[2] ^ Rcon2 ^ sub2Nib(w[3])
    w[5] = w[4] ^ w[3]


# The main encryption function, used to encrypt input plaintext
def encrypt(ptext):
    # function used to mix the columns of the two matrixs by [1, 4, 4, 1]
    def mixColumns(s):
        return [s[0] ^ mult(4, s[2]), s[1] ^ mult(4, s[3]),
                s[2] ^ mult(4, s[0]), s[3] ^ mult(4, s[1])]

    state = convertVector(((w[0] << 8) + w[1]) ^ ptext)
    state = mixColumns(shift(substitution(sBox, state)))
    state = addKey(convertVector((w[2] << 8) + w[3]), state)
    state = shift(substitution(sBox, state))
    return convertInteger(addKey(convertVector((w[4] << 8) + w[5]), state))


# The main decryption function, used to decrypt input ciphertext
def decrypt(ctext):
    # function used to mix the columns of the two matrixs by [9, 2, 2, 9]
    def inverseMixColumns(s):
        return [mult(9, s[0]) ^ mult(2, s[2]), mult(9, s[1]) ^ mult(2, s[3]),
                mult(9, s[2]) ^ mult(2, s[0]), mult(9, s[3]) ^ mult(2, s[1])]

    state = convertVector(((w[4] << 8) + w[5]) ^ ctext)
    state = substitution(sBoxI, shift(state))
    state = inverseMixColumns(addKey(convertVector((w[2] << 8) + w[3]), state))
    state = substitution(sBoxI, shift(state))
    return convertInteger(addKey(convertVector((w[0] << 8) + w[1]), state))


def stringTo16Bits(st):
    input = ' '.join(map(bin,bytearray(st))).split(' ')
    if len(input)%2 == 1:
        input.append('0b0000000')  # null string
    finalInput = []
    for x in range(1, len(input), 2):
        if len(input[x-1][2:]) < 8:
            firstByte = input[x-1][:2] + '0'*(8-len(input[x-1][2:])) + input[x-1][2:]
        if len(input[x][2:]) < 8:
            secondByte = input[x][:2] + '0'*(8-len(input[x][2:])) + input[x][2:]
        else:
            firstByte = input[x-1]
            secondByte = input[x]
        finalInput.append(firstByte + secondByte[2:])
    return finalInput

def bits16ToString(st):
    output = []
    for x in st:
        if len(x) > 8:
            output.append(chr(int(x[0:len(x)-8], 2)))
            output.append(chr(int(x[len(x)-8:], 2)))
        else:
            output.append(chr(int(x, 2)))
    return ''.join(output)

# main function
if __name__ == '__main__':
    print('This program encrypts your 16-bit binary plaintext and key using')
    print('s-AES (simplified advanced encryption standard)')

    # used to convert to binary
    getBin = lambda x: x >= 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]

    encryptedList = []
    decryptedList = []

    st = b"Hello World! Information Security Class. $323545%^&#@@!"
    stList = stringTo16Bits(st)
    print("Plaintext :", st)
    print(stList)
    for msg in stList:
        plaintext = msg
        key = 0b0100100001001001
        keyExpansion(key)
        cipher = encrypt(int(plaintext, 2))
        encryptedList.append(getBin(cipher))

    print("Key:" + getBin(key))
    print()
    print("Encrypted :")
    print(encryptedList)
    print()

    for x in range (0,26):
        print(len(encryptedList[x]))


    for cipher in encryptedList:
        ciphertext = cipher
        key = 0b0100100001001001
        keyExpansion(key)
        plaintext = decrypt(int(ciphertext, 2))
        decryptedList.append(getBin(plaintext))

    print("Key:" + getBin(key))
    print()

    print("Decrypted :")
    print(decryptedList)
    print("Decrypted Plaintext :", bits16ToString(decryptedList))
    print()

    # f = open("dictionary.txt", 'r')
    # while True:
    #     line = f.readline()
    #     if not line: break
    #
    #     st = "Hello World! Information Security Class. "+line
    #     st = st.encode()
    #     stList = stringTo16Bits(st)
    #     for msg in stList:
    #         plaintext = msg
    #         key = 0b0100100001001001
    #         keyExpansion(key)
    #         cipher = encrypt(int(plaintext, 2))
    #         encryptedList.append(getBin(cipher))
    #
    #     print("Key:" + getBin(key))
    #     print()
    #     print("Encrypted :")
    #     print(encryptedList)
    #
    #     print()
    #
    #     for cipher in encryptedList:
    #         ciphertext = cipher
    #         key = 0b0100100001001001
    #         keyExpansion(key)
    #         plaintext = decrypt(int(ciphertext, 2))
    #         decryptedList.append(getBin(plaintext))
    #
    #     print("Key:" + getBin(key))
    #     print()
    #
    #     print("Decrypted :")
    #     print(decryptedList)
    #     print("Decrypted Plaintext :", bits16ToString(decryptedList))
    #     print()
    # f.close()














