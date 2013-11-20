#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
import operator

alphabet = u' абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
encryptedText = [u'осугдтюспвщО'.lower(),
                 u'м липаернвна',
                 u'емвиер т озв',
                 u'т ипиачмктел',
                 u'китс аофмкри',
                 u'миаач кк зот',
                 u'оминнс оетвр',
                 u'памыняеид те',
                 u'лляа бсооънв',
                 u'ютоя тсосния',
                 u'елоты смьптн',
                 u'янмовмеос ст',
                 u'ныытпошрхмл ',
                 u'ннре ыовыбсх',
                 u'в  ок   т  ч']

colSize = len(encryptedText)
rowSize = len(encryptedText[0])
text = ''
for col in range(0, rowSize):
    for row in range(0, colSize):
# for col in range(rowSize - 1, 0, -1):
#     for row in range(colSize - 1, 0, -1):
        text += encryptedText[row][col]
encryptedText = text

alphabetSize = len(alphabet)
for shift in range(1, alphabetSize):
    decryptedText = ''
    for char in encryptedText:
        decryptedText += alphabet[(alphabet.index(char) + shift) % alphabetSize]
    print 'shift = ' + str(shift) + ': ' + decryptedText


symbolsStats = {}
for symbol in encryptedText:
    if symbol not in symbolsStats:
        symbolsStats[symbol] = 1
    else:
        symbolsStats[symbol] += 1

symbolsStats = collections.OrderedDict(sorted(symbolsStats.items(), key=operator.itemgetter(1)))
# выведем результаты на экран
print '[' + ', '.join(symbolsStats.keys()) + ']'
print symbolsStats.values()
# for item in symbolsStats.items():
#     print '%s: %f' % (item[0], float(item[1]) / len(encryptedText))
print 'размер зашифрованного алфавита = %d' % len(symbolsStats)

# результат будет таким:
# "возможно мы недооцениваем всеобщность закономерности согласно которой человеческая ответственность проявляется только
#  в конкретной жизненной задаче"