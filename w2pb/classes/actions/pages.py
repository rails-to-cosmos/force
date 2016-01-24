''' APaginateClick --- click next page on paginator and wait for result '''

from w2p.classes.webpage import WebPage
from w2p.classes.actions.action import Action, ConfigParserException
from w2p.classes.actions.click import AClick


class APages(AClick):
    ''' Paginate click action class '''

    def do(self):
        webpages = self.target
        selector = self.data.get('selector')

        curr_page = self.data.get(Action.AD_CURRENT_PAGE, 1)
        page = curr_page

        for webpage in webpages:
            page_source = webpage.get_page_source() if isinstance(webpage, WebPage) else webpage
            super(APages, self)._add_to_result_(page_source)

        while True:
            page += 1
            self.data[Action.AD_SELECTOR] = self.__get_page_selector__(selector, page)
            res_len = len(self.result)
            super(APages, self).do()

            if len(self.result) == res_len:
                super(APages, self).register_info(
                    Action.MSG_PAGES_COUNT % page)
                break

    def __get_page_selector__(self, selector, page):
        page_alias = ':page:'
        page_pos = selector.find(page_alias)
        if page_pos == -1:
            raise ConfigParserException(self, Action.AE_SPECIFY_PAGE_PARAM)
        str_before = selector[:page_pos]
        str_after = selector[page_pos + len(page_alias):]
        return '%s%d%s' % (str_before, page, str_after)
