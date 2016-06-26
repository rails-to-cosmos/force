#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re


def replace_month_reprs(content, idate):
        content = content.lower()

        cyrillic_mreprs = {
            u'янв': 1, u'фев': 2, u'мар': 3, u'апр': 4,
            u'мая': 5, u'май': 5, u'июн': 6, u'июл': 7,
            u'авг': 8, u'сен': 9, u'окт': 10, u'ноя': 11,
            u'дек': 12
        }

        latin_mreprs = {
            u'jan': 1, u'feb': 2, u'mar': 3, u'apr': 4,
            u'may': 5, u'jun': 6, u'jul': 7, u'aug': 8,
            u'sep': 9, u'oct': 10, u'nov': 11, u'dec': 12
        }

        mreprs = dict(cyrillic_mreprs.items() + latin_mreprs.items())

        for mkey, mval in mreprs.iteritems():
            if mkey in content:
                content = re.sub(ur'\b{0}\w*'.format(mkey), unicode(mval), content, flags=re.UNICODE)

        return (content, idate)
