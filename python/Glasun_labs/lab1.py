#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import collections
# import operator
#
# alphabet = u' АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
# # alphabet = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
#
# # вводим исходное зашифрованное сообщение в текстовую переменную. (прочитано по строкам)
# encryptedText = u'пщигплкМядйкяжъЩЖзължзёюЖлььлсзЯЗзевжяёГКйяяъжмКЛмжщщвщЛХчзличцЬЩщщйзщлВЖжюъщдзЧъъяжзщё'
# # (прочитано по столбцам)
# encryptedText = u'пяЖЖЗКЛХЩЖъщдзлзймчщжъийъьеяжзщюягкльвящлйъжпяжлжъщизщзлжзсяжвчщдщкъёзёмщцлзёМЩюЯГКЛЬВЧ'
#               # u'Ценность на КОТОРУЮ НаПРавЛеНО деЙСТвИе ТРаНЦеНТНа ПО ОТНОШеНИЮ К СаМОМУ ЭТОМу дЕйстВию'
# # составляем перечень используюемых в зашифрованном сообщении символов и подсчитаем количество их вхождений в текст.
# symbolsStats = {}
# for symbol in encryptedText:
#     if symbol not in symbolsStats:
#         symbolsStats[symbol] = 1
#     else:
#         symbolsStats[symbol] += 1
#
# symbolsStats = collections.OrderedDict(sorted(symbolsStats.items(), key=operator.itemgetter(1)))
# # выведем результаты на экран
# print '[' + ', '.join(symbolsStats.keys()) + ']'
# print symbolsStats.values()
# # for item in symbolsStats.items():
# #     print '%s: %f' % (item[0], float(item[1]) / len(encryptedText))
# print 'размер зашифрованного алфавита = %d' % len(symbolsStats)
#
# # составим сперва перечень символов, которые, как мы ожидаем, могут присутствовать в исходном сообщении.
# charsList = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя .,'
# # теперь сделаем предположения по отдельным символам на основе ранее собранных сведений.
# #             [В, Г, Ж, З, К, Л, М, Х, Ч, Щ, Ь, Я, в, г, д, е, ж, з, и, й, к, л, м, п, с, ц, ч, щ, ъ, ь, ю, я, ё]
# #             [1, 1, 3, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 7, 8, 2, 3, 2, 6, 2, 2, 1, 1, 2, 9, 6, 2, 2, 6, 3]
# mapping = {}
# mapping[u'з'] = u' '

# проверяем метод перестановки
# for i in range(2, len(encryptedText) / 2):
#     for j in range(0, len(encryptedText), i):
#         print encryptedText[j: j + i]
#     print '---'
# print 'end'

# for alphabetSize in range(66, 67):
#     print '--- alphabet size = %d ---' % alphabetSize
#     for shift in range(1, alphabetSize):
#         decryptedText = ''
#         for char in encryptedText:
#             decryptedText += alphabet[(alphabet.index(char) + shift) % alphabetSize]
#         print 'shift = ' + str(shift) + ': ' + decryptedText

alphabet = u' абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
encryptedText = u'пяЖЖЗКЛХЩЖъщдзлзймчщжъийъьеяжзщюягкльвящлйъжпяжлжъщизщзлжзсяжвчщдщкъёзёмщцлзёМЩюЯГКЛЬВЧ'.lower()
alphabetSize = len(alphabet)
for shift in range(1, alphabetSize):
    decryptedText = ''
    for char in encryptedText:
        decryptedText += alphabet[(alphabet.index(char) + shift) % alphabetSize]
    print 'shift = ' + str(shift) + ': ' + decryptedText
