# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: .\src\test\rm_path.py
# Compiled at: 2021-08-19 19:18:58
# Size of source mod 2**32: 1183 bytes
import os, sys, string
src_root_path = None
data_root_path = None
ftp_server_port = None
scratch_log_enable = 0
for p in sys.path:
    if p.startswith('scratch_src_root&'):
        arr = p.split('&')
        src_root_path = arr[1]
    else:
        if p.startswith('scratch_data_root&'):
            arr = p.split('&')
            data_root_path = arr[1]
        if p.startswith('ftp_server_port&'):
            arr = p.split('&')
            ftp_server_port = int(arr[1])
    if p.startswith('scratch_log_enable&'):
        arr = p.split('&')
        scratch_log_enable = int(arr[1])
else:

    def get_root_path():
        global src_root_path
        return src_root_path


    def get_data_path():
        global data_root_path
        return data_root_path


    def get_ftp_server_port():
        global ftp_server_port
        return ftp_server_port


    def get_scratch_log_enable():
        global scratch_log_enable
        return scratch_log_enable


    def make_src_full_path(file_name):
        return os.path.join(src_root_path, file_name)


    def make_data_full_path(file_name):
        return os.path.join(data_root_path, file_name)