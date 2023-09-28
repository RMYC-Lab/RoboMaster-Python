# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: .\src\test\custom_ui\widget_module.py
# Compiled at: 2021-08-19 19:18:58
# Size of source mod 2**32: 2268 bytes
import rm_define, duml_cmdset
from duss_event_msg import EventMsg
from tools import hostid2senderid
from widget_define import *

def widget_type_to_enum(t):
    if t == 'bool':
        return widget_date_type.bool
    if t == 'int32':
        return widget_date_type.int32
    if t == 'float':
        return widget_date_type.float
    if t == 'string':
        return widget_date_type.string


def widget_value_to_length(t, v):
    if t == 'bool':
        return 1
    if t == 'int32' or t == 'float':
        return 4
    if t == 'string':
        return len(v)


class Widget(object):

    def __init__(self, event_client):
        self.event_client = event_client
        self.msg_buff = EventMsg(hostid2senderid(event_client.my_host_id))
        self.msg_buff.set_default_receiver(rm_define.mobile_id)
        self.msg_buff.set_default_cmdset(duml_cmdset.DUSS_MB_CMDSET_RM)

    def attribute_set(self, type, index, function_enum, params=()):
        self.msg_buff.init()
        self.msg_buff.cmd_id = duml_cmdset.DUSS_MB_CMD_RM_CUSTOM_UI_ATTRIBUTE_SET
        self.msg_buff.append('type', 'uint8', type)
        self.msg_buff.append('index', 'uint8', index)
        self.msg_buff.append('function_enum', 'uint8', function_enum)
        self.msg_buff.append('params_num', 'uint8', len(params))
        id = 0
        for t, v in params:
            self.msg_buff.append('param_type_%d' % id, 'uint8', widget_type_to_enum(t))
            self.msg_buff.append('param_length_%d' % id, 'uint8', widget_value_to_length(t, v))
            self.msg_buff.append('param_value_%d' % id, t, v)
            id += 1
        else:
            duss_result = self.event_client.send_msg(self.msg_buff)

    def action_trigger_callback_register(self, callback):
        cmd_set_id = duml_cmdset.DUSS_MB_CMDSET_RM << 8 | duml_cmdset.DUSS_MB_CMD_RM_CUSTOM_UI_ACTION_TRIGGER
        self.event_client.async_req_register(cmd_set_id, callback)

    def action_trigger_callback_unregister(self):
        cmd_set_id = duml_cmdset.DUSS_MB_CMDSET_RM << 8 | duml_cmdset.DUSS_MB_CMD_RM_CUSTOM_UI_ACTION_TRIGGER
        self.event_client.async_req_unregister(cmd_set_id)