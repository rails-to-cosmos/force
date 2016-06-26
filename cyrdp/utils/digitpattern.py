# -*- coding: utf-8 -*-
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta


patterns = [
            r"""
            (?P<year>\b\d{4}\b)
            [^:\w]+
            (?P<month>\b\d{1,2}\b)
            [^:\w]+
            (?P<day>\b\d{1,2})
            \D+
            (?P<hour>\d{1,2}\b)
            [\:]
            (?P<minute>\b\d{2}\b)
            (?:
            [\:]
            (?P<second>\b\d{2}\b)
            )?
            """,

            r"""
            (?P<day>\b\d{1,2}\b)
            [^:\w]+
            (?P<month>\b\d{1,2}\b)
            [^:\w]+
            (?P<year>\b(?:\d{4}|\d{2}))
            \D+
            (?P<hour>\d{1,2}\b)
            [\:]
            (?P<minute>\b\d{2}\b)
            (?:
            [\:]
            (?P<second>\b\d{2}\b)
            )?
            """,

            r"""
            (?P<hour>\b\d{1,2}\b)
            [\:]
            (?P<minute>\b\d{2})
            (?:
            [\:]
            (?P<second>\b\d{2})
            )?
            \D+
            (?P<day>\d{1,2}\b)
            [^:\w]+
            (?P<month>\b\d{1,2}\b)
            [^:\w]+
            (?P<year>\b(?:\d{4}|\d{2})\b)
            """,

            r"""
            (?P<hour>\b\d{1,2}\b)
            [\:]
            (?P<minute>\b\d{2})
            (?:
            [\:]
            (?P<second>\b\d{2})
            )?
            \D+
            (?P<year>\d{4}\b)
            [^:\w]+
            (?P<month>\b\d{1,2}\b)
            [^:\w]+
            (?P<day>\b\d{1,2}\b)
            """,

            r"""
            (?P<day>\b\d{1,2}\b)
            [^:\w]+
            (?P<month>\b\d{1,2})
            \D+
            (?P<hour>\d{1,2}\b)
            [\:]
            (?P<minute>\b\d{2}\b)
            (?:
            [\:]
            (?P<second>\b\d{2}\b)
            )?
            """,

            r"""
            (?P<day>\b\d{1,2}\b)
            [^:\w]+
            (?P<month>\b\d{1,2}\b)
            [^:\w]+
            (?P<year>\b(?:\d{4}|\d{2})\b)
            """,

            r"""
            (?P<year>\b\d{4}\b)
            [^:\w]+
            (?P<month>\b\d{1,2}\b)
            [^:\w]+
            (?P<day>\b\d{1,2}\b)
            """,

            r"""
            (?P<hour>\b\d{1,2}\b)
            [\:]
            (?P<minute>\b\d{2}\b)
            (?:
            [\:]
            (?P<second>\b\d{2})
            )?
            \D+
            (?P<day>\d{1,2}\b)
            [^:\w]+
            (?P<month>\b\d{1,2}\b)
            """,

            r"""
            (?P<hour>\d{1,2}\b)
            [\:]
            (?P<minute>\b\d{2}\b)
            (?:
            [\:]
            (?P<second>\b\d{2})\b
            )?
            """,

            r"""
            (?P<day>\b\d{1,2}\b)
            [^:\w]+
            (?P<month>\b\d{1,2}\b)
            """,

            r"""
            (?P<month>\b\d{1,2}\b)
            [^:\w]+
            (?P<year>\b\d{4}\b)
            """,

            r'(?P<timestamp>\b\d{9,10}\b)',  # understands timestamp with 9 or 10 digits
            ]


def digit_pattern(content, idate):
    for pattern in patterns:
        try:
            date = re.search(pattern, content, flags=re.UNICODE|re.VERBOSE).groupdict()
        except AttributeError as e:
            continue

        # print pattern
        # print content
        # print date

        timestamp = date.get('timestamp')
        day = date.get('day')
        month = date.get('month')
        year = date.get('year')
        if timestamp:
            idate = datetime.fromtimestamp(int(timestamp))
        else:
            if not day and month and year :  # TODO: описать эту логику
                now = datetime.now()
                parsed_date = datetime(
                    year=int(date.get('year') or idate.year),
                    month=int(date.get('month') or idate.year),
                    day=1
                )
                current_date = datetime(
                    year=now.year,
                    month=now.month,
                    day=1
                )
                if parsed_date == current_date:
                    day = now.day
                elif parsed_date < current_date:
                    day = (parsed_date + relativedelta(months=1, days=-1)).day
                else:
                    day = 1

            date = {
                    'day': day or idate.day,
                    'month': date.get('month') or idate.month,
                    'year': date.get('year') or idate.year,
                    'hour': date.get('hour') or 0,
                    'minute': date.get('minute') or 0,
                    'second': date.get('second') or 0,
                }

            for rn, rv in date.iteritems():
                date[rn] = int(rv)

            if date.get('year') < 100:
                date['year'] += 2000

            idate = datetime(**date)

        # content = re.sub(pattern, '', content)
        content = u''  # content made empty to skip other operations

        break

    return content, idate
