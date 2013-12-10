#!/usr/bin/env python
# -*- coding: utf-8 -*-

# вводим исходное зашифрованное сообщение в текстовую переменную. Корректное отображение символов получится только если
# просматривать данный файл в UTF-8 кодировке с шрифтом wingding.ttf (или если скопировать этот текст в текстовый
# редактор с теми же намтройками). Лично я скопировал этот текст из LibreOffice4. Там символы шрифта wingding занимают
# диапазон от #f000 до #f0ff, причем позиция всех символов внутри этого диапазона, кроме символа Ом, совпадает
# с позицией кириллических букв в кодировке windows-1251.
encryptedText = u'' \
                u'' \
                u''
# уменьшаем код символов до диапазона значений 0-255
text = ''.join([chr(ord(char) - 0xf000) for char in encryptedText])
# и заменяем символ '\' на знак пробела
text = text.replace('\\', ' ')
# выводим результат в кодировке windows-1251 (она же cp1251)
print text.decode('cp1251')

# результат будет таким:
# "возможно мы недооцениваем всеобщность закономерности согласно которой человеческая ответственность проявляется только
#  в конкретной жизненной задаче"