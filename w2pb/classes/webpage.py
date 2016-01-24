import copy
from abc import abstractmethod
from w2p.classes import JSONSerializable


class WebPage(JSONSerializable):
    def __init__(self):
        self.__source__ = ''

    def set_page_source(self, src):
        self.__source__ = copy.copy(src)

    def get_page_source(self):
        return self.__source__

    def save(self, filename):
        fff = open(filename, 'w')
        fff.write(self.get_page_source().encode('utf-8'))
        fff.close()

    @abstractmethod
    def download(self, url):
        ''' Download page '''
        pass

    def free(self):
        pass
