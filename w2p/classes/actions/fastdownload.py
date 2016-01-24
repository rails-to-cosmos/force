''' AFastDownload --- download webpage from url without using virtual browser '''

from w2p.classes.actions.action import Action
from w2p.classes.staticwp import StaticWP


class AFastDownload(Action):
    ''' Download page without using virtual browser '''

    def __init__(self, _data=None, _name=None, _target=None, _settings=None):
        super(AFastDownload, self).__init__(_data, _name, _target, _settings)

    def do(self):
        urls = self.data.get('url')
        urls = super(AFastDownload, self).ensure_list(urls)

        for url in urls:
            webpage = StaticWP()
            webpage.download(url)
            super(AFastDownload, self)._add_to_result_(webpage)
