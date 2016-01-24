import re
from lxml.cssselect import CSSSelector


class MyXPathTranslator(object):
    def jq_to_xpath(self, jqsel):
        index = -1

        selector_logics = {
            'RELATIVE': (jqsel[0] == '>'),
            'EQ': ('eq' in jqsel),
            'RECURSIVE': False,
        }

        if selector_logics.get('RELATIVE') is True:
            jqsel = jqsel[1:]

        if selector_logics.get('EQ') is True:
            indexes = re.findall(r':eq\((\d+)\)', jqsel)
            splitted = re.split(r':eq\(\d+\)\W*', jqsel)
            splitted = [x for x in splitted if x]
            index = int(indexes.pop(0))
            selector = splitted.pop(0)
            # TODO remove eq from selector
            xpsel = CSSSelector(selector).path
            if len(splitted) > 0:
                jqsel = jqsel.replace('{item}:eq({index})'.format(
                    item=selector,
                    index=index), '')
                selector_logics['RECURSIVE'] = True
        else:
            xpsel = CSSSelector(jqsel).path

        if selector_logics.get('RELATIVE') is True:
            xpsel = re.sub(r'^descendant-or-self::', '', xpsel)

        result = [(xpsel, int(index))]

        if selector_logics.get('RECURSIVE'):
            result.extend(self.jq_to_xpath(jqsel))

        return result
