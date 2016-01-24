''' Basic abstract class for actions '''

import time
import traceback
from w2p.classes.webpage import WebPage

from abc import abstractmethod


class Action(object):
    ''' Contains action constants and main methods to override and use '''
    # Config attributes
    DATA = 'data'
    NAME = 'name'
    SETTINGS = 'settings'
    TARGET = 'target'
    TYPE = 'type'
    ACTIONS = 'actions'
    RESULT = 'result'


    ### Action types. Type name must be equal to class name
    # Click on object with specified selector and store webpage content
    AT_CLICK = 'AClick'
    # Gets all pages
    AT_PAGES = 'APages'
    # Download page from url
    AT_DOWNLOAD = 'ADownload'
    # Parse text by jquery selector
    AT_PARSE_BY_SELECTOR = 'AParseBySelector'
    # Store specified parameter
    AT_STORE_PARAM = 'AStoreParam'
    # Re.match wrapper
    AT_RE_MATCH = 'AReMatch'
    # Compare action.target and action.data
    AT_ASSERT_EQUALS = 'AAssertEquals'
    # WITHOUT VIRTUAL BROWSER: Download only text content from url
    AT_FAST_DOWNLOAD = 'AFastDownload'

    # Action settings
    ## temp local storage for downloaded files
    AS_LOCAL_STORAGE = 'local_storage'

    AS_INPUT_FORMAT = 'input_format'  # specify input format
    AS_OUTPUT_FORMAT = 'output_format'  # specify output format

    ## If True, user may get action result by processor's get_data:
    AS_VISIBLE = 'visible'

    ## If specified, repeat action n times:
    AS_REPEAT = 'repeat'
    ### Repeat action until exception is raised
    AR_UNTIL_EXCEPTION = 'until_exception'

    ## Customize wait behaviour of phantom processes:
    AS_WAIT = 'wait'
    AWT_AJAX = 'ajax'
    AWT_DOCUMENT_READY = 'ready'
    AWT_SELECTOR = 'selector'


    # Possible action data
    AD_LOCAL = '__local__'  # local action data
    AD_SELECTOR = 'selector'  # selector for jq parsing
    AD_URL = 'url'  # url for url processing
    AD_CURRENT_PAGE = 'current_page'  # paginator setting, start page index
    AD_PATTERN = 'pattern'  # pattern for re operations
    AD_NAMES = 'names'  # output names


    # Formats
    AF_PLAIN_TEXT = 'plainText'
    AF_WEBPAGE_OBJECT = 'webpageObject'
    AF_LXML_OBJECT = 'lxmlObject'


    # Warnings
    AW_UNABLE_TO_LOCATE_TARGET = 'Target not found'
    AW_ELEMENT_TOO_OLD = 'Element too old'
    AW_NO_JQUERY_ON_SITE = 'No jQuery on this site'


    # Exceptions
    AE_UNABLE_TO_LOCATE_ENTRY = 'Unable to locate entry by selector "%s"'
    AE_MAX_EX_TIME_EXCEEDED = 'Maximum execution time exceeded'
    AE_SPECIFY_PAGE_PARAM = '''You must specify :page: increment
    parameter in selector'''
    AE_ASSERTION_ERROR = 'Result (%d) not equals counter (%d)'
    AE_ASSERTION_SUCCESS = 'Result (%d) equals counter (%d)'


    # Messages
    MSG_ITERATION_STOPPED = 'Iteration stopped by %s action'
    MSG_PAGES_COUNT = '%d pages found'

    def __init__(self, _data=None, _name=None, _target=None, _settings=None):
        self.data, self.name, self.target = _data, _name, _target
        # default values
        self.data = _data if _data else dict()
        self.settings = _settings if _settings else dict()
        self.result = list()
        self.start_time = None
        self.errors = list()
        self.warnings = list()
        self.info = list()

    def prepare(self):
        ''' Prepare action to do '''
        self.start_time = time.time()

    def finish(self):
        ''' Finish action '''
        pass
        # print('--- Action %s.%s executed in %05.2f seconds' %
        #       (self.__class__, self.name, time.time() - self.start_time))

    def free(self):
        ''' Remove unnecessary data from memory '''
        for res_item in self.result:
            if isinstance(res_item, WebPage):
                res_item.free()
                res_item = None

        self.result = []

    @abstractmethod
    def do(self):
        ''' Main method for each action child to work with self.data,
        self.name, self.taget, self.settings '''
        pass

    def set_setting(self, setting_name, setting_value):
        ''' Set action setting to specified value '''
        if not isinstance(self.settings, dict):
            self.settings = dict()

        self.settings[setting_name] = setting_value

    def register_error(self, errmsg):
        ''' Register error in self.errors '''
        self.errors.append({
            'message': errmsg,
            'action': self.name,
            'traceback': traceback.format_exc()
        })

    def register_warning(self, wrnmsg):
        ''' Register warnin in self.warnings '''
        self.warnings.append({
            'message': wrnmsg,
            'action': self.name,
            'traceback': traceback.format_exc()
        })

    def register_info(self, infomsg):
        ''' Register info in self.info '''
        self.info.append({
            'message': infomsg,
            'action': self.name,
        })

    def is_visible(self):
        ''' Return TRUE if action result visible for user '''
        return self.settings.get(self.AS_VISIBLE, False)

    def _add_to_result_(self, elements):
        ''' Add elements to action result '''

        if isinstance(elements, list):
            for element in elements:
                self.result.append(element)
        else:
            self.result.append(elements)

    @staticmethod
    def ensure_list(element):
        if isinstance(element, list):
            return element
        else:
            return [element]


class ActionException(Exception):
    ''' Basic exception class '''
    def __init__(self, action, message):
        super(ActionException, self).__init__()
        self.message = repr('Error in action "%s": "%s".' %
                            (action.name, message))

    def __str__(self):
        return self.message


class ActionTimeoutException(ActionException):
    ''' Raises when action requires a lot of time to process '''
    def __init__(self, action, message):
        super(ActionTimeoutException, self).__init__(action, message)
        action.register_error(self.message)


class FindObjectException(ActionException):
    ''' Raises when action cannot find object '''
    pass


class ConfigParserException(ActionException):
    ''' Raises on wrong config setup '''
    def __init__(self, action, message):
        super(ConfigParserException, self).__init__(action, message)
        action.register_error(self.message)
