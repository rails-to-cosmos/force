import requests
from w2p.classes.webpage import WebPage


class StaticWP(WebPage):
    def __init__(self):
        super(StaticWP, self).__init__()

    def download(self, url):
        session = requests.Session()
        # session.headers.update({
        #     'Accept-Language': 'en-US;q=0.6,en;q=0.4'
        # })
        response = session.get(url)
        self.set_page_source(response.text)
