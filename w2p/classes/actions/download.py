''' ADownload --- download webpage from url '''
from w2p.classes.actions.action import Action
from w2p.classes.dynamicwp import DynamicWP


class ADownload(Action):
    ''' Download action class '''

    def __init__(self, _data=None, _name=None, _target=None, _settings=None):
        super(ADownload, self).__init__(_data, _name, _target, _settings)

    def do(self):
        urls = self.data.get('url')
        urls = super(ADownload, self).ensure_list(urls)

        for url in urls:
            webpage = DynamicWP()
            webpage.set_waiting_behaviour(
                self.settings.get(
                    Action.AS_WAIT,
                    [Action.AWT_AJAX, Action.AWT_DOCUMENT_READY]))
            webpage.download(url)
            super(ADownload, self)._add_to_result_(webpage)
