import random
import binascii
import hashlib

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
bits = '01'

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


###PBE functions###

#generate Salt
def genSalt() :
    salt = "".join(([random.choice(letters) for _ in range(10)]))
    return salt

#generate KEK
def genKEK(salt, password) :
    plain = salt + password
    kek = hashlib.sha1(plain.encode('utf-8')).hexdigest()
    return kek

#generate Key
def genKey() :
    key = int("".join(([random.choice(bits) for _ in range(10)])), 2)
    return key

#encryption of PBE
def encryptPBE(message) :

    #put your Password
    print("Password : ", end='')
    password = input()

    salt = genSalt()
    kek = int(genKEK(salt, password), 16)
    key = genKey()

    print("KEK : %x" % (kek))
    print("Key : %s" % (bin(key)))

    encKey = simpleDES(kek, str(key), 'encrypt')
    encMsg = simpleDES(key, message, 'encrypt')

    return (salt, encKey, encMsg)

#decryption of PBE
def decryptPBE(salt, encKey, encMsg):

    #put your Password
    print("Password : ", end='')
    password = input()

    kek = int(genKEK(salt, password), 16)
    print("KEK : %x" % (kek))

    decKey = simpleDES(kek, encKey, 'decrypt')
    decMsg = simpleDES(int(decKey), encMsg, 'decrypt')

    print("Decrypt Key : %s" % (bin(int(decKey))))

    return decMsg


if __name__ == '__main__':

    #put your message
    print("Message : ", end='')
    message = input()

    #encryption
    print("\n******Encryption PBE******")
    salt, encKey, encMsg = encryptPBE(message)
    print("Salt : %s" % (salt))
    print("Encrypt Key : %s" % (encKey))
    print("Encrypt Message : %s" % (encMsg))

    #decryption
    print("\n******Decryption PBE******")
    decMsg = decryptPBE(salt, encKey, encMsg)
    print("Decrypt Message : %s" % (decMsg))