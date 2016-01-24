import os
import unittest
import json
import time

from copy import deepcopy

from w2p.classes.processor import WebPageProcessor
from .configs import echoconf
from .configs import testconf


class ConfigsTestCase(unittest.TestCase):
    ''' Test new implemented configs '''
    @classmethod
    def setUpClass(self):
        self.maxDiff = None
        self.config = None

    def make_dirs(self, filename):
        try:
            os.stat(os.path.dirname(filename))
        except OSError:
            os.makedirs(os.path.dirname(filename))

    def save_json(self, name1, name2, jsondata):
        jsonpath = '/tmp/mcs/comments/%s/%s.json' % (name1, name2)
        self.make_dirs(jsonpath)
        fff = open(jsonpath, 'w')
        fff.write(json.dumps(jsondata, indent=4, ensure_ascii=False).encode('utf-8'))
        fff.close()

    def save_config(self, name, config):
        self.save_json(name, 'config', config)

    def save_result(self, name, result):
        self.save_json(name, 'result',  result)

    def save_errors(self, name, errors):
        self.save_json(name, 'errors', errors)

    def save_warnings(self, name, warnings):
        self.save_json(name, 'warnings', warnings)

    def save_info(self, name, info):
        self.save_json(name, 'info', info)

    @staticmethod
    def get_counter(result):
        try:
            counter = int(result[0].get('counter'))
        except ValueError:
            pass
        return counter

    @staticmethod
    def get_comment_count(result):
        res_len = sum(1 if comment['body'].strip()
                      else 0 for comment in result)
        return res_len

    def tearDown(self):
        print('\n%s starts here' % self._testMethodName)
        start_time = time.time()

        w2p = WebPageProcessor()

        config = self.config.get('comments')
        for action in deepcopy(config):
            w2p.add_action(_type=action.get('type'),
                           _data=action.get('data'),
                           _name=action.get('name'),
                           _target=action.get('target'),
                           _settings=action.get('settings'))
        try:
            w2p.run()
        finally:
            result = w2p.get_result()
            errors = w2p.get_errors()
            warnings = w2p.get_warnings()
            info = w2p.get_info()
            w2p.free()

        print('%s executed in %05.2f seconds' % (self._testMethodName, (time.time() - start_time)))
        self.save_result(self._testMethodName, result)
        self.save_config(self._testMethodName, self.config)
        self.save_errors(self._testMethodName, errors)
        self.save_warnings(self._testMethodName, warnings)
        self.save_info(self._testMethodName, info)
        self.assertEqual(len(errors), 0)

    # +
    def test_testconf(self):
        self.config = testconf.config
