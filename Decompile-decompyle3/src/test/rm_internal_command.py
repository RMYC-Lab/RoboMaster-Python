# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: .\src\test\rm_internal_command.py
# Compiled at: 2021-08-19 19:18:58
# Size of source mod 2**32: 553 bytes
import os
INTERNAL_CMD_SOF = 254
INTERNAL_CMD_EOF = 239
CMD_PING = 0
CMD_EXIT = 1
CMD_CONNECTED = 2
CMD_DISCONNECTED = 3
CMD_INVALID = 255

def is_internal_command(buff):
    buf_len = len(buff)
    if buf_len >= 4:
        if buff[0] == INTERNAL_CMD_SOF:
            if buff[buf_len - 1] == INTERNAL_CMD_EOF:
                return True
    return False


def get_internal_command(buff):
    if is_internal_command(buff):
        return buff[2]
    return CMD_INVALID