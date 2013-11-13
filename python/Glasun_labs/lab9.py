#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
This application demonstrates the encryption and decryption of texts via using Vigenere cipher.
"""
DEFAULT_ALPHABET = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class Encoder:
    """ Converts text data into encrypted string using Vigenere cipher with specified alphabet. """
    def __init__(self, alphabet=DEFAULT_ALPHABET):
        """ Constructs the Encoder instance with specified alphabet.
            Note that any character in this alphabet should be unique and appears only once."""
        self.alphabet = alphabet

    def encode(self, text, key):
        checkEncodeDecodeParams(self.alphabet, text, key)
        alphabet = self.alphabet
        result = ''
        for i in range(len(text)):
            sourceChar = text[i]
            keyChar = key[i % len(key)]
            encodedChar = alphabet[(alphabet.find(sourceChar) + alphabet.find(keyChar)) % len(alphabet)]
            result += encodedChar
        return result


class Decoder:
    """ Converts encrypted text data to plain string using Vigenere cipher with specified alphabet. """
    def __init__(self, alphabet=DEFAULT_ALPHABET):
        """ Constructs the Decoder instance with specified alphabet.
            Note that any character in this alphabet should be unique and appears only once."""
        self.alphabet = alphabet

    def decode(self, encryptedText, key):
        checkEncodeDecodeParams(self.alphabet, encryptedText, key)
        alphabet = self.alphabet
        result = ''
        for i in range(len(encryptedText)):
            sourceChar = encryptedText[i]
            keyChar = key[i % len(key)]
            # Sequence types in Python handles negative indices properly,
            # so here no need to add len(alphabet) to the left part of expression.
            decodedChar = alphabet[(alphabet.find(sourceChar) - alphabet.find(keyChar)) % len(alphabet)]
            result += decodedChar
        return result


def checkAlphabet(alphabet):
    #check if alphabet is None or empty
    if not alphabet:
        raise Exception('The alphabet shouldn\'t be empty.')
    #check if alphabet is incorrect (contains multiple occurrences of the same character)
    for i in range(len(alphabet)):
        char = alphabet[i]
        if alphabet.find(char) < i:
            raise Exception('The character \'' + char + '\' (ord = ' + str(ord(char)) + ') appears '
                            'multiple times in current alphabet (' + alphabet + ').')


def checkEncodeDecodeParams(alphabet, text, key):
    #check if text or key params are None or empty
    if not text or not key:
        raise Exception('The text and key parameters shouldn\'t be empty.')
    #check if text or key contains any characters which are not from a current alphabet
    for char in text:
        if char not in alphabet:
            raise Exception('A forbidden character \'' + char + '\' (ord = ' + str(ord(char)) + ') was found '
                            'in text. Only characters from current alphabet (' + alphabet + ') are allowed.')
    for char in key:
        if char not in alphabet:
            raise Exception('A forbidden character \'' + char + '\' (ord = ' + str(ord(char)) + ') was found '
                            'in key. Only characters from current alphabet (' + alphabet + ') are allowed.')


# main part of this script
print '--- decoding ---'
print Decoder().decode('MRPPIFGOUMRYMAHNRYMDUNRWZOANJEF TIZNIMIQWREQUNGEIALWRNSMXRJEUASTWYENCMRYMRCIZJEEICXKJQPQ '
                       'XEBDLBJYMLRKMETGJJXEEDIKMFFPBZJEZDWWCEIDCCIE DBRKFYAIFZY', 'EMPIRE')

print '--- encoding ---'
en = Encoder()
data = [
    (u'THERE LIVED IN A VILLAGE A MAN WHOSE NAME WAS PETER. HIS NICKNAME, HOWEVER, WAS NUMBSKULL', u'COPYBOOK'),
    (u'ONE DAY PETER THE NUMBSKULL HAD THREE RUBLES. HE SHOVED THEM INTO HIS POCKET AND WENT OFF FOR A WALK', u'DRAGON'),
    (u'BUT EVERY TWO STEPS HE WOULD STOP AND CHECK—ARE THOSE THREE RUBLES STILL THERE IN HIS POCKET?', u'EMPIRE'),
    (u'HE WAS SO PLEASED THAT HE HAD THREE RUBLES ALL OF HIS OWN. AND THEN ONCE AGAIN HE PUT HIS HAND IN HIS POCKET—AND IT WAS EMPTY', u'ENCOUNTER'),
    (u'PETER THE NUMBSKULL SAT DOWN ON A LOG AND BURST INTO TEARS', u'ENDING'),
    (u'ALONG THROUGH THE VILLAGE CAME RUNNING A BOY, WHOSE NAME WAS IGNAT.', u'INFANTRY'),
    (u'OFF WENT IGNAT, AND SOON HE FOUND THE THREE RUBLES, LYING UNDER A BURDOCK PLANT.', u'OUTSIDER'),
    (u'HE GRABBED THOSE THREE RUBLES AND HID THEM DEEP DOWN IN HIS POCKET. AND THEN HE STUFFED HIS POCKET WITH GRASS, SO THAT THE MONEY WOULD NOT FALL OUT.', u'JOURNAL'),
    (u'IGNAT RAN TO VISIT EVERY DAY, BUT INSTEAD OF BEING ON THE CART, THE WHEELS LAY IN THE SHED', u'NOTATION'),
    (u'AND PETER THE NUMBSKULL WAS LEFT STANDING ON THE TABLE, WITH CHALK TRICKLING OFF HIS UGLY MUG, AND GRASS FLYING OUT OF HIS POCKET.', u'NOTEBOOK'),
    (u'ОДНИМ ИЗ САМЫХ ПРИМИТИВНЫХ ТАБЛИЧНЫХ ШИФРОВ ПЕРЕСТАНОВКИ ЯВЛЯЕТСЯ ПРОСТАЯ ПЕРЕСТАНОВКА', u'МИСТИФИКАЦИЯ'),
    (u'НЕСКОЛЬКО БОЛЬШЕЙ СТОЙКОСТЬЮ К РАСКРЫТИЮ ОБЛАДАЕТ МЕТОД  ОДИНОЧНОЙ ПЕРЕСТАНОВКОЙ ПО КЛЮЧУ', u'ДЕЛЕНИЕ'),
    (u'В ВЕРХНЕЙ СТРОКЕ ЛЕВОЙ ТАБЛИЦЫ ЗАПИСАН КЛЮЧ', u'РЕАКЦИЯ'),
    (u'ПРИ СЧИТЫВАНИИ СОДЕРЖИМОГО ПРАВОЙ ТАБЛИЦЫ ПО СТРОКАМ И ЗАПИСИ ШИФРТЕКСТА ГРУППАМИ ПО ЧЕТЫРЕ БУКВЫ ПОЛУЧИМ ШИФРОВАННОЕ СООБЩЕНИЕ', u'АССОЦИАТИВНОСТЬ'),
    (u'ДВОЙНАЯ ПЕРЕСТАНОВКА НЕ ОТЛИЧАЕТСЯ ВЫСОКОЙ СТОЙКОСТЬЮ И СРАВНИТЕЛЬНО ПРОСТО ВЗЛАМЫВАЕТСЯ ПРИ ЛЮБОМ РАЗМЕРЕ ТАБЛИЦЫ ШИФРОВАНИЯ', u'РЕГРЕССИЯ'),
    (u'ШИФРУЕМЫЙ ТЕКСТ ВПИСЫВАЕТСЯ В МАГИЧЕСКИЕ КВАДРАТЫ В СООТВЕТСТВИИ С НУМЕРАЦИЕЙ ИХ КЛЕТОК.', u'ПРОГРЕССИЯ'),
    (u'ПРИ ШИФРОВАНИИ ПОДСТАНОВКОЙ СИМВОЛЫ ШИФРУЕМОГО ТЕКСТА ЗАМЕНЯЮТСЯ СИМВОЛАМИ ТОГО ЖЕ С ЗАРАНЕЕ УСТАНОВЛЕННЫМ ПРАВИЛОМ ЗАМЕНЫ', u'ИДЕНТИФИКАЦИЯ'),
    (u'ТАКОЙ ШИФР ЗАМЕНЫ МОЖНО ЗАДАТЬ ТАБЛИЦЕЙ ПОДСТАНОВОК, СОДЕРЖАЩЕЙ СООТВЕТСТВУЮЩИЕ ПАРЫ БУКВ ОТКРЫТОГО ТЕКСТА И ШИФРТЕКСТА.', u'ЗАКОН'),
    (u'УСТАНОВИМ ВЗАИМНО ОДНОЗНАЧНОЕ СООТВЕТСТВИЕ МЕЖДУ АЛФАВИТОМ И МНОЖЕСТВОМ ЦЕЛЫХ ЧИСЕЛ', u'СПРАВОЧНИК'),
    (u'В ОТЛИЧИЕ ОТ ШИФРА ЦЕЗАРЯ СИСТЕМА ШИФРОВАНИЯ ЦЕЗАРЯ ОБРАЗУЕТ ПО СЕМЕЙСТВО ОДНОАЛФАВИТНЫХ ПОДСТАНОВОК ДЛЯ ВЫБИРАЕМЫХ ЗНАЧЕНИЙ КЛЮЧА', u'ДИСКЕТА'),
]
for text, key in data:
    try:
        print Encoder().encode(text, key)
        print '-'
    except Exception as e:
        print e.message

print '--- done ---'