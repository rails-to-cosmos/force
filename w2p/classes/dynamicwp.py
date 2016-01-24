import time
import psutil
from psutil import NoSuchProcess

from w2p import settings

from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import InvalidSelectorException

from w2p.classes.webpage import WebPage
from w2p.classes.myxpathtranslator import MyXPathTranslator


class DynamicWP(WebPage):
    RS_INTERACTIVE = 'interactive'
    RS_COMPLETE = 'complete'

    DWPS_WAIT = 'wait'
    AWT_AJAX = 'ajax'
    AWT_DOCUMENT_READY = 'ready'
    AWT_SELECTOR = 'selector'

    def __init__(self, webdriver=None):
        super(DynamicWP, self).__init__()

        self.webdriver = webdriver
        self.remote_webdriver = True if webdriver else False

        self.__sleeptime__ = 0.5
        self.__settings__ = dict()

    def download(self, url):
        webd = self.webdriver or self.__create_phantom_instance__()
        webd.set_window_size(1120, 560)
        webd.set_page_load_timeout(180)
        webd.get(url)
        self.webdriver = webd
        self.wait()
        super(DynamicWP, self).set_page_source(self.webdriver.page_source)

    def click(self, selector):
        xptr = MyXPathTranslator()
        xpsel, index = xptr.jq_to_xpath(selector)
        elements = self.webdriver.find_elements_by_xpath(xpsel)
        if abs(index) == index:
            try:
                elements = [elements[index]]
            except IndexError:
                # element not found
                raise InvalidSelectorException

        if len(elements) == 0:
            raise InvalidSelectorException

        for element in elements:
            if not element.is_displayed():
                raise InvalidSelectorException

            try:
                element.click()
            except WebDriverException:
                self.webdriver.execute_script(
                    "document.querySelector('%s').click();" % selector)

        self.wait()
        super(DynamicWP, self).set_page_source(self.webdriver.page_source)

    def wait(self):
        ''' Wait until the document is loaded '''
        if self.webdriver:
            for wset in self.__settings__.get(self.DWPS_WAIT):
                if wset == self.AWT_AJAX:
                    print('Wait ajax...')
                    self.__wait_for_ajaxes__()
                elif wset == self.AWT_DOCUMENT_READY:
                    print('Wait ready...')
                    self.__wait_for_ready_state__()
                elif wset == self.AWT_SELECTOR:
                    print('Wait selector...')
                elif isinstance(wset, int):
                    # print('Wait %d seconds...' % wset)
                    time.sleep(wset)

    def free(self):
        if (self.webdriver is not None) and (self.remote_webdriver is False):
            try:
                phjs = psutil.Process(self.webdriver.service.process.pid)
                children = phjs.children(recursive=True)
                for child in children:
                    child.kill()
                self.webdriver.service.process.kill()
            except OSError:
                pass
            except NoSuchProcess:
                pass
            finally:
                # twice here
                self.webdriver.quit()
                self.webdriver = None

    def set_waiting_behaviour(self, wbeh):
        self.__settings__[self.DWPS_WAIT] = wbeh

    @staticmethod
    def __create_phantom_instance__():
        from selenium import webdriver
        return webdriver.PhantomJS(**settings.PHANTOM_DATA)

    def __wait_for_ready_state__(self):
        ready_state = self.RS_INTERACTIVE
        limit = settings.AJAX_TIMEOUT
        cur_iter = 0
        while ready_state != self.RS_COMPLETE:
            ready_state = self.webdriver.execute_script('return document.readyState')
            time.sleep(self.__sleeptime__)
            cur_iter += 1
            if cur_iter > limit:
                break

    def __wait_for_ajaxes__(self):
        active_ajaxes = 1
        limit = settings.AJAX_TIMEOUT
        cur_iter = 0
        try:
            while active_ajaxes > 0:
                active_ajaxes = self.webdriver.execute_script('return jQuery.active')
                time.sleep(self.__sleeptime__)
                cur_iter += 1
                if cur_iter > limit:
                    break
            return
        except WebDriverException:
            pass  # no jQuery on this site
