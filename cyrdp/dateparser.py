# -*- coding: utf-8 -*-

import re
import sys

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from copy import copy
from testcases import testcases
from utils.replacedigitreprs import replace_digit_reprs
from utils.digitpattern import digit_pattern
from utils.relrepr import rel_repr
from utils.reltime import rel_time
from utils.replacemonthrepr import replace_month_reprs


class DateParser(object):
    @classmethod
    def parse(cls, content, pattern=None):
        try:
            result = cls.__main_parse_logic__(content, pattern)
        except Exception as exc:
            print u'Error catched:'
            if content:
                print u'Parse: Content = {content}'.format(content=content)
            if pattern:
                print u'Pattern = {pattern}'.format(pattern=pattern)
            print u'Message = {msg}'.format(msg=exc.message.decode('utf-8'))
            raise

        return result

    @staticmethod
    def __main_parse_logic__(content, pattern=None):
        initial_content = content

        try:
            content = content.lower()
        except AttributeError:
            raise Exception('Content is None, string expected')

        initial_content_lower = content

        now = datetime.now()
        idate = datetime(year=now.year,
                         month=now.month,
                         day=now.day,
                         hour=now.hour,
                         minute=now.minute,
                         second=now.second)  # initial date

        def custom_pattern(pattern):
            if pattern:
                def def_pattern(content, idate):
                    try:
                        groups = re.search(pattern, content).groupdict()
                    except AttributeError:
                        return content, idate

                    idate = datetime(year=int(groups.get('year', idate.year)),
                                     month=int(groups.get('month', idate.month)),
                                     day=int(groups.get('day', idate.day)),
                                     hour=int(groups.get('hour', 0)),
                                     minute=int(groups.get('minute', 0)),
                                     second=int(groups.get('second', 0)))
                    return content, idate
                return def_pattern
            else:
                def null_pattern(content, idate):
                    return content, idate
                return null_pattern

        registered_patterns = [
            replace_month_reprs,  # приводим строковое представление месяца к числу
            custom_pattern(pattern),
            replace_digit_reprs,
            rel_repr,
            digit_pattern,
            rel_time,

        ]

        changed = False
        for rp in registered_patterns:

            try:
                initial_idate = copy(idate)
                content, idate = rp(content, idate)
                if not changed:
                    changed = (initial_idate.replace(microsecond=0) != idate.replace(microsecond=0)) or \
                              (initial_content_lower != content)
            except Exception as exc:
                print u'Method: {method}'.format(method=rp.__name__)
                print u'Exception: Content = {content}'.format(content=initial_content)
                print u'Date: {date}'.format(date=idate)
                exc.message = exc.message + '. Content = {content}'.format(content=initial_content.encode('utf-8'))
                raise type(exc)(exc.message)

            if rp.__name__ == 'def_pattern' and pattern:
                break

        if not changed and initial_content:
            raise Exception(u'Couldn\'t parse date\nNot changed: Content = {}'.format(initial_content_lower))

        return '%04d-%02d-%02dT%02d:%02d:%02d' % (idate.year,
                                                  idate.month,
                                                  idate.day,
                                                  idate.hour,
                                                  idate.minute,
                                                  idate.second)

if __name__ == '__main__':
    dp = DateParser()

    only_test_cases = dict()
    for initial, expected in testcases.iteritems():
        if re.match(r'^\!.*', initial):
            try:
                only_test_cases[initial[1:]] = expected
            except KeyError:
                only_test_cases = dict()
                only_test_cases[initial[1:]] = expected

    if only_test_cases:
        testcases = only_test_cases

    tcnt, tsuc, terr = 0, 0, 0

    method_to_call = DateParser.parse
    for initial, expected in testcases.iteritems():
        try:
            method_result = method_to_call(initial)
            method_result = datetime.strptime(method_result, '%Y-%m-%dT%H:%M:%S')

            tcnt += 1

            if isinstance(expected, tuple):
                assert method_result >= expected[0] and method_result <= expected[1]
            else:
                assert method_result == expected

            tsuc += 1
        except AssertionError:
            terr += 1
            print(u'')
            print(u'*'*3)
            print(u'Test "{initial}" failed'.format(initial=initial))
            print(u'%s != %s' % (method_result, expected))
            print(u'*'*3)
            print(u'')

    print('{tcnt} tests done, {tsuc} succeeded, {terr} failed'.format(
        tcnt=tcnt,
        tsuc=tsuc,
        terr=terr
    ))
