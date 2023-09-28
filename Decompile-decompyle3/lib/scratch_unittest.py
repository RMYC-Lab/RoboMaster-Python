# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: .\lib\scratch_unittest.py
# Compiled at: 2020-08-19 12:20:28
# Size of source mod 2**32: 558 bytes


class TestResult:

    def __init__(self):
        self.test_finished = False
        self.test_result = False
        self.test_exit = False

    def set_test_finished(self):
        self.test_finished = True

    def get_test_finished(self):
        return self.test_finished

    def set_test_result(self, result):
        self.test_result = result

    def get_test_result(self):
        return self.test_result

    def set_test_exit(self):
        self.test_exit = True

    def get_test_exit(self):
        return self.test_exit