# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: .\sdk\sdk_manager.py
# Compiled at: 2020-08-19 12:20:28
# Size of source mod 2**32: 791 bytes
import os, plaintext_sdk

class SDKManager(object):

    def __init__(self, event_client, socket_obj, uart_obj):
        self.plaintext_sdk = plaintext_sdk.PlaintextSDK(event_client, socket_obj, uart_obj)
        self.plaintext_sdk_config = {}
        self.load_cfg()

    def load_cfg(self):
        cur_dir = os.path.dirname(__file__)
        f = open(cur_dir + '/version.txt')
        version_ori = f.readlines()
        f.close()
        version = ''
        for i in version_ori:
            version = version + '%.2d.' % int(i.split(' ')[-1][0:-1])
        else:
            version = version[0:-1]
            self.plaintext_sdk_config['version'] = version

    def enable_plaintext_sdk(self):
        self.plaintext_sdk.init(self.plaintext_sdk_config)