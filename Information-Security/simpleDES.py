#!/usr/bin/python3

from sys import exit
from time import time

import binascii
import time
import timeit

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

IV = '!'
counter = '?'

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

#added
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

def simpleDES(key, message, mode, blkmode):
    translated =''

    if blkmode == "ECB" :
        for sym in message:
            if mode =='encrypt':
                encMsg = encrypt(key, ord(sym))
                print("Plaintext: %s byte: %s encMSG: %s Ciphertext: %s" % (sym, text_to_bits(sym), bin(encMsg), chr(encMsg)))
                translated = translated + chr(encMsg)

            if mode == 'decrypt':
                decMsg = decrypt(key, ord(sym))
                print("Ciphertext: %s decMSG %s Plaintext: %s" % (sym, bin(decMsg), text_from_bits(bin(decMsg))))
                translated = translated + chr(decMsg)

    elif blkmode == "CBC" :
        pre = ord(IV)
        for sym in message:
            if mode =='encrypt':
                encMsg = encrypt(key, ord(sym) ^ pre)
                print("Plaintext: %s byte: %s encMSG: %s Ciphertext: %s" % (sym, text_to_bits(sym), bin(encMsg), chr(encMsg)))
                translated = translated + chr(encMsg)
                pre = encMsg

            if mode == 'decrypt':
                temp = pre
                pre = ord(sym)
                decMsg = decrypt(key, ord(sym)) ^ temp
                print("Ciphertext: %s decMSG %s Plaintext: %s" % (sym, bin(decMsg), text_from_bits(bin(decMsg))))
                translated = translated + chr(decMsg)

    elif blkmode == "CFB":
        pre = ord(IV)
        for sym in message:
            if mode =='encrypt':
                encMsg = encrypt(key, pre) ^ ord(sym)
                pre = encMsg
                print("Plaintext: %s byte: %s encMSG: %s Ciphertext: %s" % (sym, text_to_bits(sym), bin(encMsg), chr(encMsg)))
                translated = translated + chr(encMsg)

            if mode == 'decrypt':
                decMsg = encrypt(key, pre) ^ ord(sym)
                pre = ord(sym)
                print("Ciphertext: %s decMSG %s Plaintext: %s" % (sym, bin(decMsg), text_from_bits(bin(decMsg))))
                translated = translated + chr(decMsg)

    elif blkmode == "OFB":
        pre = ord(IV)
        for sym in message:
            if mode == 'encrypt':
                encMsg = encrypt(key, pre)
                pre = encMsg
                encMsg = encMsg ^ ord(sym)
                print("Plaintext: %s byte: %s encMSG: %s Ciphertext: %s" % (
                sym, text_to_bits(sym), bin(encMsg), chr(encMsg)))
                translated = translated + chr(encMsg)

            if mode == 'decrypt':
                decMsg = encrypt(key, pre)
                pre = decMsg
                decMsg = decMsg ^ ord(sym)
                print("Ciphertext: %s decMSG %s Plaintext: %s" % (sym, bin(decMsg), text_from_bits(bin(decMsg))))
                translated = translated + chr(decMsg)

    elif blkmode == "CTR":
        ctr = counter
        cnt = 0
        for sym in message:
            if mode =='encrypt':
                encMsg = encrypt(key, ord(ctr) + cnt)
                encMsg = encMsg ^ ord(sym)
                print("Plaintext: %s byte: %s encMSG: %s Ciphertext: %s" % (sym, text_to_bits(sym), bin(encMsg), chr(encMsg)))
                translated = translated + chr(encMsg)

            if mode == 'decrypt':
                decMsg = encrypt(key, ord(ctr) + cnt)
                decMsg = decMsg ^ ord(sym)
                print("Ciphertext: %s decMSG %s Plaintext: %s" % (sym, bin(decMsg), text_from_bits(bin(decMsg))))
                translated = translated + chr(decMsg)

            cnt += 1

    else :
        print("Block Mode Error")

    return translated



if __name__ == '__main__':

    message = "Ji-Yeong Kim"
    key = 0b1110001110

    print("key: %s" % bin(key))
    print("IV : %c binary: %s" % (IV, bin(ord(IV))))
    print("counter : %c binary: %s" % (counter, bin(ord(counter))))
    print("\n")


    start = timeit.default_timer()
    print("ECB mode")

    print("Encrytion")
    encMSG = simpleDES(key, message, 'encrypt', "ECB")
    print("Encrypted Message:",encMSG)

    print("\nDecrytion")
    decMSG = simpleDES(key, encMSG, 'decrypt', "ECB")
    print("Decrypted Message:", decMSG)

    finish = timeit.default_timer()
    print("\nECB Running time : ", end='')
    print(finish - start)
    print("\n")


    start = timeit.default_timer()
    print("CBC mode")

    print("Encrytion")
    encMSG = simpleDES(key, message, 'encrypt', "CBC")
    print("Encrypted Message:", encMSG)

    print("\nDecrytion")
    decMSG = simpleDES(key, encMSG, 'decrypt', "CBC")
    print("Decrypted Message:", decMSG)

    finish = timeit.default_timer()
    print("\nCBC Running time : ", end='')
    print(finish - start)
    print("\n")


    start = timeit.default_timer()
    print("CFB mode")

    print("Encrytion")
    encMSG = simpleDES(key, message, 'encrypt', "CFB")
    print("Encrypted Message:", encMSG)

    print("\nDecrytion")
    decMSG = simpleDES(key, encMSG, 'decrypt', "CFB")
    print("Decrypted Message:", decMSG)

    finish = timeit.default_timer()
    print("\nCFB Running time : ", end='')
    print(finish - start)
    print("\n")


    start = timeit.default_timer()
    print("OFB mode")

    print("Encrytion")
    encMSG = simpleDES(key, message, 'encrypt', "OFB")
    print("Encrypted Message:", encMSG)

    print("\nDecrytion")
    decMSG = simpleDES(key, encMSG, 'decrypt', "OFB")
    print("Decrypted Message:", decMSG)

    finish = timeit.default_timer()
    print("\nOFB Running time : ", end='')
    print(finish - start)
    print("\n")


    start = timeit.default_timer()
    print("CTR mode")

    print("Encrytion")
    encMSG = simpleDES(key, message, 'encrypt', "CTR")
    print("Encrypted Message:", encMSG)

    print("\nDecrytion")
    decMSG = simpleDES(key, encMSG, 'decrypt', "CTR")
    print("Decrypted Message:", decMSG)

    finish = timeit.default_timer()
    print("\nCTR Running time : ", end='')
    print(finish - start)

