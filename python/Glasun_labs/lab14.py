#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This application demonstrates the encryption and decryption of texts via using RSA algorithm. """
import math, numpy, random
from binascii import unhexlify


class RSA:
    """ Implements RSA encoding algorithm. """
    def __init__(self, P=None, Q=None, Ka=None):
        checkCipher(P, Q, Ka)
        self.N = P * Q
        self.phi = (P - 1) * (Q - 1)
        self.Ka = Ka
        # calculate Kb as modular multiplicative inverse from Ka by module phi
        # (see http://en.wikipedia.org/wiki/Modular_multiplicative_inverse for details)
        # however, I have not handled the solution of extended Euclidean algorithm, so I used a simpler solution.
        i = 1
        while True:
            if (self.phi * i + 1) % Ka == 0:
                Kb = (self.phi * i + 1) / Ka
                if isCoPrime(Kb, self.N):
                    break
            i += 1
        self.Kb = Kb
        # calculate which amount of bytes I could handle at once for encoding/decoding data
        self.chunkSize = self.N.bit_length() / 8

    def encode(self, bytesArray):
        result = ''
        # Because encryptedData could be greater than chunkSize lets increase encryptedBytes size on 1
        fmt = '%%0%dx' % ((self.chunkSize + 1) * 2)

        for chunkFirstByteIndex in range(0, len(bytesArray), self.chunkSize):
            chunkBytes = bytesArray[chunkFirstByteIndex: chunkFirstByteIndex + self.chunkSize]
            if chunkFirstByteIndex + self.chunkSize > len(bytesArray):
                # need to add extra empty bytes
                for i in range(0, chunkFirstByteIndex + self.chunkSize - len(bytesArray)):
                    chunkBytes += '\x00'
            # convert bytes array into integer
            chunkData = int(chunkBytes.encode('hex'), 16)
            # encode chunk of data
            encryptedData = pow(chunkData, self.Ka, self.N)
            # convert integer back to bytes array
            encryptedBytes = unhexlify(fmt % encryptedData)
            # and append it to result bytes array
            result += encryptedBytes
        return result

    def decode(self, bytesArray):
        result = ''
        fmt = '%%0%dx' % (self.chunkSize * 2)
        # Because encryptedData could be greater than chunkSize lets increase chunkBytes size on 1
        for chunkFirstByteIndex in range(0, len(bytesArray), self.chunkSize + 1):
            chunkBytes = bytesArray[chunkFirstByteIndex: chunkFirstByteIndex + self.chunkSize + 1]
            chunkData = int(chunkBytes.encode('hex'), 16)
            decryptedData = pow(chunkData, self.Kb, self.N)
            # convert integer back to bytes array
            decryptedBytes = unhexlify(fmt % decryptedData)
            # and append it to result bytes array
            result += decryptedBytes
        # remove empty bytes which could appear after decoding
        return result.rstrip('\x00')


def checkCipher(P, Q, Ka):
    """ Checks that P, Q and Ka parameters is ok """
    if not P or not Q or not Ka:
        raise Exception('The P, Q and Ka values shouldn\'t be specified and greater than 0.')
    #check that P and Q values are greater than 2 and they are prime numbers. Also they shouldn't be equal
    if P <= 2 or Q <= 2 or P == Q or not isPrime(P) or not isPrime(Q):
        raise Exception('The P and Q values should be a prime numbers greater than 2. Also they shouldn\'t be equal.')
    #check that 1 < Ka < φ(N)
    phi = (P - 1) * (Q - 1)
    if Ka >= phi:
        raise Exception('The Ka value should fit to range (1, φ(N)).')
    # check that N > 256. If it isn't so then we need to divide our data to a pieces smaller than one byte.
    N = P * Q
    if N < 256:
        raise Exception('The N value too small to even handle a single byte while encode/decode action.')


def isPrime(number):
    #looking for any divisor greater than 1
    for divisor in range(2, int(math.sqrt(number) + 1)):
        if number % divisor == 0:
            return False
    return True


def isCoPrime(number1, number2):
    #looking for common divisor except 1
    for divisor in range(2, int(math.sqrt(number1) + 1)):
        if number1 % divisor == 0 and number2 % divisor == 0:
            return False
    #check if some number is a multiplier of another
    if  number1 % number2 == 0 or number2 % number1 == 0:
        return False
    #otherwise this numbers is co-prime
    return True


def generateRandomParams():
    # parse text file for numbers separated by whitespaces and placed below 4th line header.
    # first data row is also skipped because this numbers is to small for normal RSA algorithm work
    numpyNumbers = numpy.genfromtxt('./1000_prime_numbers.txt', skip_header=5, skip_footer=1)
    #convert to plain list
    primeNumbers = []
    for subArray in numpyNumbers:
        for num in subArray:
            primeNumbers.append(int(num))

    P = Q = Ka = None
    #skip first 10 prime numbers as too small.
    P = primeNumbers[random.randint(0, len(primeNumbers))]
    while Q is None or Q == P:
        Q = primeNumbers[random.randint(0, len(primeNumbers))]
    phi = (P - 1) * (Q - 1)
    while Ka is None or not isCoPrime(Ka, phi):
        Ka = random.randint(2, 100)
    return P, Q, Ka


# main part of this script
P, Q, Ka = generateRandomParams()
print '--- initial parameters ---'
print 'P = %d, Q = %d, Ka = %d' % (P, Q, Ka)
cipher = RSA(P, Q, Ka)
print '--- calculated parameters ---'
print 'N = %d, φ(N) = %d, Kb = %d, chunkSize = %d bytes' % (cipher.N, cipher.phi, cipher.Kb, cipher.chunkSize)
encodedText = cipher.encode(b'Long-long string with a Latin alphabet letters, а также с русскими буквами.')
print '--- encrypted data ---'
print encodedText
print '--- restored data ---'
print cipher.decode(encodedText)
print '--- done ---'