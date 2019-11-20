from sys import exit
from time import time

import binascii, detectEnglish

KeyLength = 10
SubKeyLength = 8
DataLength = 8
FLength = 4

# Tables for initial and final permutations (b1, b2, b3, ... b8)
IPtable = (2, 6, 3, 1, 4, 8, 5, 7)
FPtable = (4, 1, 3, 5, 7, 2, 8, 6)

# Tables for subkey generation (k1, k2, k3, ... k10)
P10table = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
P8table = (6, 3, 7, 4, 8, 5, 10, 9)

# Tables for the fk function
EPtable = (4, 1, 2, 3, 2, 3, 4, 1)
S0table = (1, 0, 3, 2, 3, 2, 1, 0, 0, 2, 1, 3, 3, 1, 3, 2)
S1table = (0, 1, 2, 3, 2, 0, 1, 3, 3, 0, 1, 0, 2, 1, 0, 3)
P4table = (2, 4, 3, 1)

def perm(inputByte, permTable):
    """Permute input byte according to permutation table"""
    outputByte = 0
    for index, elem in enumerate(permTable):
        if index >= elem:
            outputByte |= (inputByte & (128 >> (elem - 1))) >> (index - (elem - 1))
        else:
            outputByte |= (inputByte & (128 >> (elem - 1))) << ((elem - 1) - index)
    return outputByte

def ip(inputByte):
    """Perform the initial permutation on data"""
    return perm(inputByte, IPtable)

def fp(inputByte):
    """Perform the final permutation on data"""
    return perm(inputByte, FPtable)

def swapNibbles(inputByte):
    """Swap the two nibbles of data"""
    return (inputByte << 4 | inputByte >> 4) & 0xff

def keyGen(key):
    """Generate the two required subkeys"""
    def leftShift(keyBitList):
        """Perform a circular left shift on the first and second five bits"""
        shiftedKey = [None] * KeyLength
        shiftedKey[0:9] = keyBitList[1:10]
        shiftedKey[4] = keyBitList[0]
        shiftedKey[9] = keyBitList[5]
        return shiftedKey

    # Converts input key (integer) into a list of binary digits
    keyList = [(key & 1 << i) >> i for i in reversed(range(KeyLength))]
    permKeyList = [None] * KeyLength
    for index, elem in enumerate(P10table):
        permKeyList[index] = keyList[elem - 1]
    shiftedOnceKey = leftShift(permKeyList)
    shiftedTwiceKey = leftShift(leftShift(shiftedOnceKey))
    subKey1 = subKey2 = 0
    for index, elem in enumerate(P8table):
        subKey1 += (128 >> index) * shiftedOnceKey[elem - 1]
        subKey2 += (128 >> index) * shiftedTwiceKey[elem - 1]
    return (subKey1, subKey2)

def fk(subKey, inputData):
    """Apply Feistel function on data with given subkey"""
    def F(sKey, rightNibble):
        aux = sKey ^ perm(swapNibbles(rightNibble), EPtable)
        index1 = ((aux & 0x80) >> 4) + ((aux & 0x40) >> 5) + \
                 ((aux & 0x20) >> 5) + ((aux & 0x10) >> 2)
        index2 = ((aux & 0x08) >> 0) + ((aux & 0x04) >> 1) + \
                 ((aux & 0x02) >> 1) + ((aux & 0x01) << 2)
        sboxOutputs = swapNibbles((S0table[index1] << 2) + S1table[index2])
        return perm(sboxOutputs, P4table)

    leftNibble, rightNibble = inputData & 0xf0, inputData & 0x0f
    return (leftNibble ^ F(subKey, rightNibble)) | rightNibble

def encrypt(key, plaintext):
    """Encrypt plaintext with given key"""
    data = fk(keyGen(key)[0], ip(plaintext))
    return fp(fk(keyGen(key)[1], swapNibbles(data)))

def decrypt(key, ciphertext):
    """Decrypt ciphertext with given key"""
    data = fk(keyGen(key)[1], ip(ciphertext))
    return fp(fk(keyGen(key)[0], swapNibbles(data)))

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def simpleDES(key, message, mode):
    translated =''
    for sym in message:
        if mode =='encrypt':
            encMsg = encrypt(key, ord(sym))
            translated = translated + chr(encMsg)
        if mode == 'decrypt':
            decMsg = decrypt(key, ord(sym))
            translated = translated + chr(decMsg)
    return translated

if __name__ == '__main__':

    message = "This is an information security class."

    plaintext = 0b10101010
    key = 0b1110001110
    translated = ''

    encMsg = encrypt(key, plaintext)
    print("key: %s  Plaintext: %s encMSG %s" % (bin(key), bin(plaintext), bin(encMsg)))
    decMSG = decrypt(key, encMsg)

    print("key: %s  encMSG: %s decMSG %s" % (bin(key), bin(encMsg), bin(decMSG)))
    if (plaintext == decMSG):
        print("Correctly Decrypted by using Simple DES!")

    print(translated)
    print("key: %s" % bin(key))

    encMSG = simpleDES(key, message, 'encrypt')
    print("Encrypted Message:",encMSG)

    print("key: %s" % bin(key))
    decMSG = simpleDES(key, encMSG, 'decrypt')
    print("Decrypted Message:", decMSG)

    yes = {'yes', 'y', 'ye', ''}
    no = {'no', 'n'}

    choice = input("Are you want to Hack on S-AES ? ").lower()
    if choice in yes:
        for key in range(0b0000000000,0b10000000000):
            print("key: %s" % bin(key))
            decMSG = simpleDES(key, encMSG, 'decrypt')
            print(decMSG)
            if (detectEnglish.isEnglish(decMSG)):
                print("Found Key!!!")
                print("Key:", bin(key), "Decrypted Message:", decMSG)
                break
    elif choice in no:
        print("See you")
    else:
        sys.stdout.write("Please respond with 'yes' or 'no'")
