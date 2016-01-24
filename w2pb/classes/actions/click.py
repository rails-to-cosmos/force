''' AClick --- click element on webpage and take page '''

from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidSelectorException

from w2p.classes.actions.action import Action


class AClick(Action):
    ''' Click action class '''
    def __init__(self, _data=None, _name=None, _target=None, _settings=None):
        Action.__init__(self, _data, _name, _target, _settings)

    def do(self):
        selector = self.data.get(Action.AD_SELECTOR)

        webpages = self.target
        webpages = super(AClick, self).ensure_list(webpages)

        repeat_count = self.settings.get(Action.AS_REPEAT, 1)

        for webpage in webpages:
            click_count = 0

            while True:
                try:
                    webpage.click(selector)
                except StaleElementReferenceException:
                    super(AClick, self).register_warning(
                        Action.AW_ELEMENT_TOO_OLD)
                    break
                except InvalidSelectorException:
                    break
                except WebDriverException:
                    break
                except AttributeError:
                    break

                click_count += 1

                if click_count == repeat_count:
                    break

            if click_count > 0:
                super(AClick, self)._add_to_result_(webpage)
