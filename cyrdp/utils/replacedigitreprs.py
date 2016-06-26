# -*- coding: utf-8 -*-


def replace_digit_reprs(content, idate):
        content = content.lower()

        dreprs = {
            u'ноль': 0,
            u'один': 1,
            u'два': 2,
            u'три': 3,
            u'четыре': 4,
            u'пять': 5,
            u'шесть': 6,
            u'семь': 7,
            u'восемь': 8,
            u'девять': 9,
            u'десять': 10,
            u'одиннадцать': 11,
            u'двенадцать': 12,
            u'тринадцать': 13,
            u'четырнадцать': 14,
            u'пятнадцать': 15,
            u'шестнадцать': 16,
            u'семнадцать': 17,
            u'восемнадцать': 18,
            u'девятнадцать': 19,
            u'двадцать': 20
        }

        for dr, di in dreprs.iteritems():
            content = content.replace(dr, unicode(di))

        return (content, idate)
