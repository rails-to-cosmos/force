import os
import urllib

from w2p.classes.processor import WebPageProcessor
from w2p.classes.actions.action import Action

from django.utils import timezone


def download_menu_files():
    menu_files = list()
    site_url = "http://hleb-sol.biz"

    wpp = WebPageProcessor()
    wpp.add_action(
        _type=Action.AT_FAST_DOWNLOAD,
        _name="webpage",
        _subject=site_url
    )
    wpp.add_action(
        _type=Action.AT_PARSE_BY_SELECTOR,
        _name="link",
        _target="webpage",
        _subject=".menuItemBig td a[href]",
        _visible=True
    )
    wpp.run()
    links = wpp.get_result()

    for lind, link in enumerate(links):
        rel_url = link.get('link')
        abs_url = site_url + rel_url
        upload_dir = 'static/uploads/'  # TODO move to settings
        os.path.exists(upload_dir) or os.makedirs(upload_dir)
        filename = u'{dt}-{di}.xls'.format(dt=unicode(timezone.now()),
                                           di=lind)
        urllib.urlretrieve(abs_url, upload_dir+filename)
        menu_files.append(upload_dir+filename)

    return menu_files
