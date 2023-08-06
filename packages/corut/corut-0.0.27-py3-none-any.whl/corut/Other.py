#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
...
"""

__author__ = 'ibrahim CÖRÜT'
__email__ = 'ibrhmcorut@gmail.com'

import string
from . import print_error
from binascii import hexlify, unhexlify


def convert_character(data, non_converting_character=''):
    result = ''
    try:
        for character in data:
            if character in non_converting_character:
                result = result + character
            elif character in string.ascii_letters or character in string.digits or character in ('-', '+'):
                result = result + character
            elif character in ('ı', 'İ', 'ö', 'Ö', 'ü', 'Ü', 'ç', 'Ç', 'ğ', 'Ğ', 'ş', 'Ş'):
                for c, c1 in ([['ı', 'i'], ['İ', 'i'], ['ö', 'o'], ['Ö', 'O'], ['ü', 'u'], ['Ü', 'U'],
                               ['ç', 'c'], ['Ç', 'C'], ['ğ', 'g'], ['Ğ', 'G'], ['ş', 's'], ['Ş', 'S']]):
                    if character == c:
                        result = result + c1
                        break
            elif character in string.punctuation.replace('-', ''):
                result = result + '_'
    except Exception as error:
        print_error(error, locals())
    return result


def encrypt_text(data):
    try:
        if data is None:
            print('encrypt_text ---> Data is None'.rjust(70, '?'))
        else:
            data = hexlify(data.encode()).decode()
    except Exception as error:
        print_error(error, locals())
    return data


def decrypt_text(data):
    try:
        if data is None:
            print('decrypt_text ---> Data is None'.rjust(70, '?'))
        else:
            data = unhexlify(data.encode()).decode()
    except Exception as error:
        print_error(error, locals())
    return data


def remove_items(items, remove_item):
    try:
        for item in remove_item:
            if item in items:
                if type(items) == list:
                    items.remove(item)
                elif type(items) == dict:
                    items.pop(item)
    except Exception as error:
        print_error(error, locals())
    return items.copy()


class Other:
    convert_character = staticmethod(convert_character)
    encrypt_text = staticmethod(encrypt_text)
    decrypt_text = staticmethod(decrypt_text)
    remove_items = staticmethod(remove_items)
