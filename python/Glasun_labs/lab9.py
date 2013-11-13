#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This application demonstrates the encryption and decryption of texts via using Vigenere cipher. """


class Cipher:
    """ Uses Vigenere cipher with specified alphabet to convert text data into encrypted string and vice versa. """
    def __init__(self, alphabet, key):
        """ Constructs the Cipher instance with specified alphabet.
            Note that any character in this alphabet should be unique and appears only once."""
        checkCipher(alphabet, key)
        self.alphabet = alphabet
        self.key = key

    def encode(self, text):
        checkText(self.alphabet, text)
        alphabet, key = self.alphabet, self.key
        result = ''
        for i in range(len(text)):
            sourceChar = text[i]
            keyChar = key[i % len(key)]
            encodedChar = alphabet[(alphabet.find(sourceChar) + alphabet.find(keyChar)) % len(alphabet)]
            result += encodedChar
        return result

    def decode(self, text):
        checkText(self.alphabet, text)
        alphabet, key = self.alphabet, self.key
        result = ''
        for i in range(len(text)):
            sourceChar = text[i]
            keyChar = key[i % len(key)]
            # Sequence types in Python handles negative indices properly,
            # so here no need to add len(alphabet) to the left part of expression.
            decodedChar = alphabet[(alphabet.find(sourceChar) - alphabet.find(keyChar)) % len(alphabet)]
            result += decodedChar
        return result


def checkCipher(alphabet, key):
    #check if alphabet is None or empty
    if not alphabet or not key:
        raise Exception('The alphabet or key values shouldn\'t be empty.')
    #check if alphabet is incorrect (contains multiple occurrences of the same character)
    for i in range(len(alphabet)):
        char = alphabet[i]
        if alphabet.find(char) < i:
            raise Exception('The character \'' + char + '\' (ord = ' + str(ord(char)) + ') appears '
                            'multiple times in current alphabet (' + alphabet + ').')
    #check if key contains any characters which are not from a current alphabet
    for char in key:
        if char not in alphabet:
            raise Exception('A forbidden character \'' + char + '\' (ord = ' + str(ord(char)) + ') was found '
                            'in key. Only characters from current alphabet (' + alphabet + ') are allowed.')


def checkText(alphabet, text):
    #check if text or key params are None or empty
    if not text:
        raise Exception('The text value shouldn\'t be empty.')
    #check if text contains any characters which are not from a current alphabet
    for char in text:
        if char not in alphabet:
            raise Exception('A forbidden character \'' + char + '\' (ord = ' + str(ord(char)) + ') was found '
                            'in text. Only characters from current alphabet (' + alphabet + ') are allowed.')


# main part of this script
print '--- decoding ---'
cipher = Cipher(alphabet=' ABCDEFGHIJKLMNOPQRSTUVWXYZ', key='EMPIRE')
print cipher.decode('MRPPIFGOUMRYMAHNRYMDUNRWZOANJEF TIZNIMIQWREQUNGEIALWRNSMXRJEUASTWYENCMRYMRCIZJEEICXKJQPQ XEBDLBJYM'
                    'LRKMETGJJXEEDIKMFFPBZJEZDWWCEIDCCIE DBRKFYAIFZY')

print '--- encoding ---'
cipher = Cipher(alphabet=' ABCDEFGHIJKLMNOPQRSTUVWXYZ.', key='DRAGON')
encodedText = cipher.encode('ONE DAY PETER THE NUMBSKULL HAD THREE RUBLES. HE SHOVED THEM INTO HIS POCKET AND WENT OFF '
                            'FOR A WALK')
print 'encoded: ' + encodedText
print 'decoded: ' + cipher.decode(encodedText)
print '--- done ---'