import sys
import copy
import re

from w2p.classes.webpage import WebPage
from w2p.classes.actions.action import Action, ActionException
from w2p.classes.actions.assertequals import AAssertEquals
from w2p.classes.actions.click import AClick
from w2p.classes.actions.download import ADownload
from w2p.classes.actions.fastdownload import AFastDownload
from w2p.classes.actions.pages import APages
from w2p.classes.actions.parsebyselector import AParseBySelector
from w2p.classes.actions.rematch import AReMatch
from w2p.classes.actions.storeparam import AStoreParam


class WebPageProcessor(object):
    ''' Main web page processor class '''

    def __init__(self):
        self.actions = list()

    def run(self):
        ''' Run specified actions '''
        actions = self.actions

        for action in actions:
            self.process_action_aliases(action)
            action.prepare()
            try:
                action.do()
            except ActionException:  # action exception breaks process
                break
            finally:
                action.finish()

    def add_action(self, _type, _data=None, _name=None, _target=None, _settings=None, _subject=None, _visible=None):
        ''' Add action in the end of queue '''
        _data = _data or dict()
        _settings = _settings or dict()

        aliases_alist = {
            Action.AT_DOWNLOAD: ['download'],
            Action.AT_FAST_DOWNLOAD: ['fdownload'],
            Action.AT_PARSE_BY_SELECTOR: ['parse'],
            Action.AT_CLICK: ['click'],
            Action.AT_RE_MATCH: ['match'],
            Action.AT_STORE_PARAM: ['store']
        }

        for alik, aliv in aliases_alist.iteritems():
            if _type in aliv:
                _type = alik

        if _subject:
            if _type in (Action.AT_DOWNLOAD, Action.AT_FAST_DOWNLOAD):
                _data[Action.AD_URL] = _subject
            elif _type == Action.AT_PARSE_BY_SELECTOR:
                _data[Action.AD_SELECTOR] = _subject
            elif _type == Action.AT_RE_MATCH:
                _data[Action.AD_PATTERN] = _subject
            elif _type == Action.AT_STORE_PARAM:
                _data = _subject

        if _visible is not None:
            _settings[Action.AS_VISIBLE] = _visible

        if _target:
            if re.match(r':[a-zA-Z_]:', _target) is None:
                _target = ':{target}.result:'.format(target=_target)

        new_action = self.create_action_from_config(_type, _data, _name,
                                                    _target, _settings)
        self.actions.append(new_action)

    def get_result(self):
        ''' Return all visible action values '''
        vis_res = self.__get_visible_results__()
        results = copy.deepcopy(self.__group_results__(vis_res))
        for item in results:
            for ikey, ival in item.iteritems():
                if isinstance(ival, WebPage):
                    item[ikey] = ival.get_page_source()
        return results

    def get_errors(self):
        ''' Return errors in processing '''
        errors = list()

        for action in self.actions:
            for error in action.errors:
                errors.append(error)

        return errors

    def get_warnings(self):
        ''' Return warnings '''
        warnings = list()

        for action in self.actions:
            for warning in action.warnings:
                warnings.append(warning)

        return warnings

    def get_info(self):
        ''' Return action info '''
        info = list()

        for action in self.actions:
            for data in action.info:
                info.append(data)

        return info

    def free(self):
        ''' Free memory, kill all phantomjs instances '''
        for action in self.actions:
            action.free()

    @staticmethod
    def create_action_from_config(_type, _data,
                                  _name=None,
                                  _target=None,
                                  _settings=None):
        action = getattr(sys.modules[__name__], _type)
        return action(_data, _name, _target, _settings)

    def process_action_aliases(self, action):
        a_dict = action.__dict__ if isinstance(action, Action) else action  # recursive
        for akey, aval in a_dict.iteritems():
            if isinstance(aval, basestring):
                obj_val = self.get_val_by_alias(aval)
                if isinstance(action, Action):
                    action.__setattr__(akey, obj_val)
                else:
                    action[akey] = obj_val
            elif isinstance(aval, dict):
                self.process_action_aliases(aval)
            else:
                continue

    def get_val_by_alias(self, composite_alias):
        result = composite_alias
        aliases = self.split_composite_alias(composite_alias)
        if len(aliases) == 0:
            return result

        for c_alias in aliases:
            full_alias, alias, func, args = c_alias

            # get object value by path
            path = alias.split('.')
            obj_val = self.get_val_by_path(path)

            try:
                assert obj_val
            except AssertionError:
                continue

            if func:
                obj_val = self.__affect_func_on_obj__(func, args, obj_val)

            if isinstance(obj_val, list) and len(obj_val) == 1:
                obj_val = obj_val[0]

            if isinstance(obj_val, basestring):
                replacement = obj_val if isinstance(obj_val, unicode) else str(obj_val)
                result = result.replace(full_alias, replacement)
            else:
                result = obj_val
                break

        return result

    @staticmethod
    def __affect_func_on_obj__(func, args, obj):
        result = None
        if func == 'get':
            index = args if isinstance(args, int) else int(args)
            try:
                return obj[index]
            except IndexError:
                return None
        elif func == 'id':
            result = range(1, len(obj) + 1)
        elif func == 'alen':
            result = len(obj)
        elif func == 'len':
            result = sum(1 if item else 0 for item in obj)
        elif func == 'dec':
            result = [int(ii)-1 for ii in obj]
        elif func == 'inc':
            result = [int(ii)-1 for ii in obj]
        return result

    def get_val_by_path(self, path):
        obj_val = None
        if len(path) == 1: # take from result by default
            path.append(Action.RESULT)
        for step in path:
            if obj_val is None:
                target_pos = self.__get_action_pos_by_name__(step)
                if target_pos < 0:
                    continue
                obj_val = self.actions[target_pos].__dict__
            elif isinstance(obj_val, dict):
                obj_val = obj_val.get(step)
            elif isinstance(obj_val, list) and obj_val.__len__() > 0:
                # hack to access first result from config TODO for all
                if isinstance(obj_val[0], dict):
                    obj_val = obj_val[0].get(step)

        return obj_val

    @staticmethod
    def split_composite_alias(composite_alias):
        ''' split composite alias
            alias_pattern -- splits aliases, function and function args
            (aliases), (function), (args) '''
        alias_pattern = r'(:([A-Za-z._]+)(?:\.([A-Za-z]+)\(([0-9a-zA-Z\-]*)\))?:)'
        aliases = re.findall(alias_pattern, composite_alias)
        if len(aliases) == 0:
            # new style
            alias_pattern = r'({{([A-Za-z._]+)(?:\.([A-Za-z]+)\(([0-9a-zA-Z\-]*)\))?}})'
            aliases = re.findall(alias_pattern, composite_alias)

        return aliases

    def __get_action_pos_by_name__(self, name):
        for action_pos, action in enumerate(self.actions):
            if action.name == name:
                return action_pos
        return -1

    @staticmethod
    def __msg_stop_iter__(action):
        return '''Iteration stopped on action %s.%s because of an exception.
                To prevent this message specify Action.AS_DEFAULT_VALUE
                in this action setting''' % (action.__class__, action.name)

    def __get_visible_results__(self):
        visible_results = []
        for action in self.actions:
            if action.is_visible():
                visible_results.append((action.name, action.result))
        return visible_results

    @staticmethod
    def __group_results__(results):
        groupped = list()
        for param in results:
            param_name = param[0]
            param_vals = param[1]
            for param_id, param_val in enumerate(param_vals):
                if groupped.__len__() > param_id:
                    groupped[param_id][param_name] = param_val
                else:
                    groupped.append({param_name: param_val})
        return groupped
