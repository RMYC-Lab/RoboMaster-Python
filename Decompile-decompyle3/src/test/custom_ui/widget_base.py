# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: .\src\test\custom_ui\widget_base.py
# Compiled at: 2021-08-19 19:18:58
# Size of source mod 2**32: 7917 bytes
from rm_log import dji_scratch_logger_get
from tools import byte_to_int32
from tools import byte_to_float
from tools import byte_to_string
from widget_module import Widget
from widget_define import *
logger = dji_scratch_logger_get()

def byte_to_value(type, byte):
    if type == 'bool':
        return byte[0]
    if type == 'int32':
        return byte_to_int32(byte)
    if type == 'float':
        return byte_to_float(byte)
    if type == 'string':
        return byte_to_string(byte)


class Position(object):

    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, x, y):
        self.x = x
        self.y = y

    def get(self):
        return (
         self.x, self.y)


class Size(object):

    def __init__(self):
        self.w = 0
        self.h = 0

    def update(self, w, h):
        self.w = w
        self.h = h

    def get(self):
        return (
         self.w, self.h)


class Color(object):

    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0
        self.a = 0

    def update(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def get(self):
        return (
         self.r, self.g, self.b, self.a)


class Attribute(object):

    def __init__(self):
        self.name = ''
        self.active = None
        self.on_stage = None
        self.position = Position()
        self.pivot = Position()
        self.size = Size()
        self.color = Color()
        self.order = 0
        self.rotation = 0

    def update_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def update_active(self, flag):
        self.active = flag

    def get_active(self, flag):
        return self.active

    def update_position(self, x, y):
        self.position.update(x, y)

    def get_position(self):
        return self.position.get()

    def update_size(self, w, h):
        self.size.update(w, h)

    def get_size(self):
        return self.size.get()

    def update_color(self, r, g, b, a):
        self.color.update(r, g, b, a)

    def get_color(self):
        return self.color.get()

    def update_rotation(self, d):
        self.rotation = d

    def get_rotation(self):
        return self.rotation

    def update_pivot(self, x, y):
        self.pivot.update(x, y)

    def get_pivot(self):
        return self.pivot.get()

    def update_order(self, order):
        self.order = order

    def get_order(self):
        return self.order


class WidgetBase(Attribute):

    def __init__(self, event_client, type, index):
        super(WidgetBase, self).__init__()
        self.type = type
        self.index = index
        self.widget = Widget(event_client)
        self.action_trigger_dict = {}
        self.action_enum_dict = {}
        self.action_value_type_list_dict = {}
        self.action_trigger_process_callback_register(self._WidgetBase__action_trigger_process)

    def create(self):
        return self.set_custom_attribute(widget_public_function.create)

    def destory(self):
        return self.set_custom_attribute(widget_public_function.destory)

    def get_type(self):
        return self.type

    def get_index(self):
        return self.index

    def set_active(self, flag):
        self.update_active(flag)
        params = (
         (
          'bool', flag),)
        return self.set_custom_attribute(widget_public_function.active)

    def set_name(self, name):
        name = name[0:64]
        self.update_name(name)
        params = (
         (
          'string', name),)
        return self.set_custom_attribute(widget_public_function.name, params)

    def set_position(self, x, y):
        self.update_position(x, y)
        params = (
         (
          'float', x),
         (
          'float', y))
        return self.set_custom_attribute(widget_public_function.position, params)

    def set_size(self, w, h):
        self.update_size(w, h)
        params = (
         (
          'int32', w),
         (
          'int32', h))
        return self.set_custom_attribute(widget_public_function.size, params)

    def set_rotation(self, d):
        self.update_rotation(d)
        params = (
         (
          'float', d),)
        return self.set_custom_attribute(widget_public_function.rotation, params)

    def set_pivot(self, x, y):
        self.update_pivot(x, y)
        params = (
         (
          'int32', x),
         (
          'int32', y))
        return self.set_custom_attribute(widget_public_function.pivot, params)

    def set_order(self, order):
        self.update_order(order)
        params = (
         (
          'int32', order),)
        return self.set_custom_attribute(widget_public_function.order, params)

    def test(self, v1, v2, v3, v4):
        params = (
         (
          'bool', v1),
         (
          'int32', v2),
         (
          'float', v3),
         (
          'string', v4))
        return self.set_custom_attribute(widget_public_function.test, params)

    def set_custom_attribute(self, function_enum, params=()):
        return self.widget.attribute_set(self.type, self.index, function_enum, params)

    def action_trigger_process_callback_register(self, cb):
        self.widget.action_trigger_callback_register(cb)

    def action_trigger_process_callback_unregister(self, cb):
        self.widget.action_trigger_callback_unregister(cb)

    def callback_register(self, action, cb):
        if action in self.action_enum_dict.keys():
            if callable(cb):
                self.action_trigger_dict[self.action_enum_dict[action]] = cb

    def update_action_enum_dict(self, action_enum_dict):
        self.action_enum_dict = action_enum_dict

    def update_action_value_type_list_dict(self, action_value_type_list_dict):
        self.action_value_type_list_dict = action_value_type_list_dict

    def __action_trigger_process--- This code section failed: ---

 L. 229         0  SETUP_FINALLY        38  'to 38'

 L. 230         2  LOAD_FAST                'msg'
                4  LOAD_STR                 'data'
                6  BINARY_SUBSCR    
                8  STORE_FAST               'data'

 L. 231        10  LOAD_FAST                'data'
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  STORE_FAST               'type'

 L. 232        18  LOAD_FAST                'data'
               20  LOAD_CONST               1
               22  BINARY_SUBSCR    
               24  STORE_FAST               'index'

 L. 233        26  LOAD_FAST                'data'
               28  LOAD_CONST               2
               30  BINARY_SUBSCR    
               32  STORE_FAST               'action'
               34  POP_BLOCK        
               36  JUMP_FORWARD         86  'to 86'
             38_0  COME_FROM_FINALLY     0  '0'

 L. 235        38  DUP_TOP          
               40  LOAD_GLOBAL              Exception
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    84  'to 84'
               46  POP_TOP          
               48  STORE_FAST               'e'
               50  POP_TOP          
               52  SETUP_FINALLY        72  'to 72'

 L. 236        54  LOAD_GLOBAL              logger
               56  LOAD_METHOD              fatal
               58  LOAD_STR                 'action_trigger_preocess unpack error, error msg: %s'
               60  LOAD_FAST                'e'
               62  BINARY_MODULO    
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          
               68  POP_BLOCK        
               70  BEGIN_FINALLY    
             72_0  COME_FROM_FINALLY    52  '52'
               72  LOAD_CONST               None
               74  STORE_FAST               'e'
               76  DELETE_FAST              'e'
               78  END_FINALLY      
               80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
             84_0  COME_FROM            44  '44'
               84  END_FINALLY      
             86_0  COME_FROM            82  '82'
             86_1  COME_FROM            36  '36'

 L. 238        86  SETUP_FINALLY       326  'to 326'

 L. 239        88  LOAD_FAST                'type'
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                type
               94  COMPARE_OP               ==
            96_98  POP_JUMP_IF_FALSE   322  'to 322'
              100  LOAD_FAST                'index'
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                index
              106  COMPARE_OP               ==
          108_110  POP_JUMP_IF_FALSE   322  'to 322'

 L. 240       112  LOAD_FAST                'action'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                action_trigger_dict
              118  LOAD_METHOD              keys
              120  CALL_METHOD_0         0  ''
              122  COMPARE_OP               in
          124_126  POP_JUMP_IF_FALSE   322  'to 322'

 L. 241       128  LOAD_FAST                'self'
              130  LOAD_ATTR                action_trigger_dict
              132  LOAD_FAST                'action'
              134  BINARY_SUBSCR    
              136  STORE_FAST               'cb'

 L. 242       138  LOAD_FAST                'cb'
          140_142  POP_JUMP_IF_FALSE   312  'to 312'

 L. 243       144  LOAD_FAST                'data'
              146  LOAD_CONST               3
              148  BINARY_SUBSCR    
              150  STORE_FAST               'params_num'

 L. 244       152  LOAD_FAST                'data'
              154  LOAD_CONST               4
              156  LOAD_CONST               None
              158  BUILD_SLICE_2         2 
              160  BINARY_SUBSCR    
              162  STORE_FAST               'data'

 L. 246       164  LOAD_FAST                'self'
              166  LOAD_ATTR                action_value_type_list_dict
              168  LOAD_FAST                'action'
              170  BINARY_SUBSCR    
              172  STORE_FAST               'params_type_list'

 L. 247       174  BUILD_LIST_0          0 
              176  STORE_FAST               'user_data'

 L. 249       178  LOAD_FAST                'params_num'
              180  LOAD_GLOBAL              len
              182  LOAD_FAST                'params_type_list'
              184  CALL_FUNCTION_1       1  ''
              186  COMPARE_OP               !=
              188  POP_JUMP_IF_FALSE   228  'to 228'

 L. 250       190  LOAD_GLOBAL              logger
              192  LOAD_METHOD              fatal
              194  LOAD_FAST                'params_type_list'
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          

 L. 251       200  LOAD_GLOBAL              logger
              202  LOAD_METHOD              fatal
              204  LOAD_STR                 'action_trigger_preocess error , params number parse error. cur num: %d tar num: %d'
              206  LOAD_FAST                'params_num'
              208  LOAD_GLOBAL              len
              210  LOAD_FAST                'params_type_list'
              212  CALL_FUNCTION_1       1  ''
              214  BUILD_TUPLE_2         2 
              216  BINARY_MODULO    
              218  CALL_METHOD_1         1  ''
              220  POP_TOP          

 L. 252       222  POP_BLOCK        
              224  LOAD_CONST               None
              226  RETURN_VALUE     
            228_0  COME_FROM           188  '188'

 L. 254       228  LOAD_FAST                'params_type_list'
              230  GET_ITER         
            232_0  COME_FROM           296  '296'
              232  FOR_ITER            298  'to 298'
              234  STORE_FAST               't'

 L. 255       236  LOAD_FAST                'data'
              238  LOAD_CONST               1
              240  BINARY_SUBSCR    
              242  STORE_FAST               'param_length'

 L. 256       244  LOAD_FAST                'data'
              246  LOAD_CONST               2
              248  LOAD_CONST               2
              250  LOAD_FAST                'param_length'
              252  BINARY_ADD       
              254  BUILD_SLICE_2         2 
              256  BINARY_SUBSCR    
              258  STORE_FAST               'param_value'

 L. 257       260  LOAD_FAST                'data'
              262  LOAD_CONST               2
              264  LOAD_FAST                'param_length'
              266  BINARY_ADD       
              268  LOAD_CONST               None
              270  BUILD_SLICE_2         2 
              272  BINARY_SUBSCR    
              274  STORE_FAST               'data'

 L. 258       276  LOAD_GLOBAL              byte_to_value
              278  LOAD_FAST                't'
              280  LOAD_FAST                'param_value'
              282  CALL_FUNCTION_2       2  ''
              284  STORE_FAST               'param_value'

 L. 260       286  LOAD_FAST                'user_data'
              288  LOAD_METHOD              append
              290  LOAD_FAST                'param_value'
              292  CALL_METHOD_1         1  ''
              294  POP_TOP          
              296  JUMP_LOOP           232  'to 232'
            298_0  COME_FROM           232  '232'

 L. 262       298  LOAD_FAST                'cb'
              300  LOAD_FAST                'self'
              302  BUILD_TUPLE_1         1 
              304  LOAD_FAST                'user_data'
              306  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              308  CALL_FUNCTION_EX      0  'positional arguments only'
              310  POP_TOP          
            312_0  COME_FROM           140  '140'

 L. 263       312  LOAD_FAST                'event_client'
              314  LOAD_METHOD              resp_ok
              316  LOAD_FAST                'msg'
              318  CALL_METHOD_1         1  ''
              320  POP_TOP          
            322_0  COME_FROM           124  '124'
            322_1  COME_FROM           108  '108'
            322_2  COME_FROM            96  '96'
              322  POP_BLOCK        
              324  JUMP_FORWARD        380  'to 380'
            326_0  COME_FROM_FINALLY    86  '86'

 L. 265       326  DUP_TOP          
              328  LOAD_GLOBAL              Exception
              330  COMPARE_OP               exception-match
          332_334  POP_JUMP_IF_FALSE   378  'to 378'
              336  POP_TOP          
              338  STORE_FAST               'e'
              340  POP_TOP          
              342  SETUP_FINALLY       366  'to 366'

 L. 266       344  LOAD_GLOBAL              logger
              346  LOAD_METHOD              fatal
              348  LOAD_STR                 'action_trigger_preocess error , error msg: %s'
              350  LOAD_GLOBAL              str
              352  LOAD_FAST                'e'
              354  CALL_FUNCTION_1       1  ''
              356  BINARY_MODULO    
              358  CALL_METHOD_1         1  ''
              360  POP_TOP          
              362  POP_BLOCK        
              364  BEGIN_FINALLY    
            366_0  COME_FROM_FINALLY   342  '342'
              366  LOAD_CONST               None
              368  STORE_FAST               'e'
              370  DELETE_FAST              'e'
              372  END_FINALLY      
              374  POP_EXCEPT       
              376  JUMP_FORWARD        380  'to 380'
            378_0  COME_FROM           332  '332'
              378  END_FINALLY      
            380_0  COME_FROM           376  '376'
            380_1  COME_FROM           324  '324'

Parse error at or near `LOAD_CONST' instruction at offset 224