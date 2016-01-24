''' AParseBySelector --- action for incapsulated webpage parsing '''
import re
import lxml
import HTMLParser
import lxml.html as lhtml

from w2p.classes.myxpathtranslator import MyXPathTranslator
from w2p.classes.actions.action import Action
from w2p.classes.webpage import WebPage


class AParseBySelector(Action):
    ''' Parse entire webpages and receive elements in what format you want '''

    def do(self):
        '''Iteratively parses TARGET by DATA.SELECTOR and
        returns result in SETTINGS.OUTPUT_FORMAT '''

        selectors = self.data.get('selector')
        selectors = self.ensure_list(selectors)

        web_elements = self.ensure_list(self.target)

        try:
            for web_element in web_elements:
                for selector in selectors:
                    elem_found = False

                    if isinstance(web_element, WebPage):
                        page_source = web_element.get_page_source()
                    else:
                        page_source = web_element

                    elements = self.__find_elements__(page_source, selector)
                    if elements:
                        self._add_to_result_(elements)
                        elem_found = True
                        break

                if not elem_found:
                    super(AParseBySelector, self)._add_to_result_(
                        '')  # default value
        except TypeError:
            super(AParseBySelector, self).register_warning(Action.AW_UNABLE_TO_LOCATE_TARGET)

        return True

    def __find_elements__(self, target, selector=None,
                          input_format=Action.AF_PLAIN_TEXT,
                          output_format=Action.AF_PLAIN_TEXT):

        result = []

        # complex selectors
        cpxsels = self.__split_selector_attr__(selector)

        for isel, cpxsel in enumerate(cpxsels):
            sel, attr = cpxsel

            if len(cpxsels) > 1:
                if isel == 0:  # first elem
                    lifmt = input_format
                    lofmt = Action.AF_LXML_OBJECT
                elif isel == len(cpxsels) - 1:  # last elem
                    lifmt = Action.AF_LXML_OBJECT
                    lofmt = output_format
                else:  # middle elems
                    lifmt = Action.AF_LXML_OBJECT
                    lofmt = Action.AF_LXML_OBJECT
            else:
                lifmt = input_format
                lofmt = output_format

            result = self.__parse_by_format__(tgt=target,
                                              sel=sel,
                                              attr=attr,
                                              inpf=lifmt,
                                              oupf=lofmt)
            target = result  # recursive attribute parsing

        return result

    def __parse_by_format__(self, tgt, sel, inpf, oupf, attr=''):
        if inpf == Action.AF_WEBPAGE_OBJECT:
            return self.__selenium_parsing__(tgt, sel, attr, oupf)
        elif inpf == Action.AF_PLAIN_TEXT:
            return self.__plain_text_parsing__(tgt, sel, attr, oupf)
        elif inpf == Action.AF_LXML_OBJECT:
            return self.__lxml_parsing__(tgt, sel, attr, oupf)
        else:
            return None

    def __selenium_parsing__(self, target, selector, attr, output_format):
        result = list()

        if selector:
            item_count = self.__item_count_by_selector__(selector)
            selector = self.__remove_eq_from_selector__(selector)

            elements = target.find_elements_by_css_selector(selector)

            if item_count > 0 and len(elements) >= item_count:
                elements = [elements[item_count - 1]]
        else:
            elements = [target]

        for elem in elements:
            if output_format == Action.AF_PLAIN_TEXT:
                if attr:
                    result.append(elem.get_attribute(attr))
                else:
                    result.append(elem.text)
            elif output_format == Action.AF_WEBPAGE_OBJECT:
                result.append(elem)

        return result

    def __plain_text_parsing__(self, target, selector, attr, ofmt):
        result = list()
        unescape = HTMLParser.HTMLParser().unescape
        elems = self.__get_lxml_elems_by_sel_from_str__(selector, target)

        for elem in elems:
            if not attr:
                eres = elem
            elif attr == 'outerHTML':
                eres = elem
            elif attr == 'prev':
                eres = elem.getprevious()
            else:
                eres = elem.get(attr)

            if ofmt == Action.AF_PLAIN_TEXT:
                if not attr:
                    eres = elem.text_content()
                if isinstance(eres, lhtml.HtmlElement):
                    eres = lhtml.tostring(eres)
                    eres = unescape(eres)

            result.append(eres)

        return result

    def __get_lxml_elems_by_sel_from_str__(self, selector, target):
        ''' Get elements by selector from target type of string.
        LXML implementation '''
        elements = []

        try:
            tree = lhtml.fromstring(target)
        except lxml.etree.XMLSyntaxError:
            super(AParseBySelector, self).register_warning(Action.AW_UNABLE_TO_LOCATE_TARGET)
            return elements

        if selector:
            if True:  # XPath relative algo: hack
                xpt = MyXPathTranslator()
                xpath_objects = xpt.jq_to_xpath(selector)
                for xpsel, epos in xpath_objects:
                    elements = tree.xpath(xpsel)
                    if epos > -1:
                        elements = elements[epos]
                    break
                # if selector[0:1] == '>':
                #     selector = selector[1:]
                #     sel = CSSSelector(selector).path
                #     xpath_self = re.sub(r'^descendant-or-self::', '', sel)

                #     if 'nth-child' in selector:
                #         elements = tree.xpath(sel)
                #     else:
                #         elements = tree.xpath(xpath_self)

                #     if item_count > 0:
                #         elements = [elements[item_count - 1]]
                # else:
                #     elements = CSSSelector(selector)(tree)
        else:
            elements = [tree]

        return elements

    def __lxml_parsing__(self, target, selector, attr, output_format):
        # TODO on complex selector improve this method
        # now it suports something like this: div[id="comment"][prev][id]
        result = list()
        elems = target
        for elem in elems:
            result.append(elem.get(attr))
        return result

    @staticmethod
    def __split_selector_attr__(selector):
        ''' Split complex selector and return simple
        selectors and args tuple list '''
        reg = re.findall(r'(.*?)\[([a-zA-Z\-]+)\]', selector)
        result = list()
        if len(reg) > 0:
            for reg_index, reg_tuple in enumerate(reg):
                result.append(reg_tuple)
        else:
            result.append((selector, ''))

        return result
