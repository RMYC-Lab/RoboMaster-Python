# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: .\lib\dji_scratch_project_parser.py
# Compiled at: 2022-01-12 15:45:07
# Size of source mod 2**32: 4625 bytes
import xml.dom.minidom
from hashlib import md5
import rm_log, rm_define
logger = rm_log.dji_scratch_logger_get()

def getStringMD5(str):
    m = md5()
    m.update(str)
    return m.hexdigest()[7:-9]


class DSPXMLParser(object):

    def __init__(self):
        self.key = '12345678'
        self.DSP_SEGMENT_DJI_STR = 'dji'
        self.DSP_SEGMENT_ATTR_STR = 'attribute'
        self.DSP_SEGMENT_CODE_STR = 'code'
        attr_list = [
         'creation_date','title','creator','firmware_version_dependency','guid','sign','code_type']
        cdata_list = ['python_code', 'scratch_description']
        self.elem_dict = {}
        self.elem_dict[self.DSP_SEGMENT_ATTR_STR] = attr_list
        self.elem_dict[self.DSP_SEGMENT_CODE_STR] = cdata_list
        self.dsp_dict = {}
        self.audio_list = []

    def parseDSPString--- This code section failed: ---

 L.  31         0  SETUP_FINALLY       218  'to 218'

 L.  32         2  LOAD_GLOBAL              xml
                4  LOAD_ATTR                dom
                6  LOAD_ATTR                minidom
                8  LOAD_METHOD              parseString
               10  LOAD_FAST                'xml_str'
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'dom_tree'

 L.  33        16  LOAD_FAST                'dom_tree'
               18  LOAD_ATTR                documentElement
               20  STORE_FAST               'collection'

 L.  35        22  LOAD_FAST                'collection'
               24  LOAD_METHOD              getElementsByTagName
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                DSP_SEGMENT_DJI_STR
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'dji_elem'

 L.  36        34  LOAD_FAST                'collection'
               36  LOAD_METHOD              getElementsByTagName
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                DSP_SEGMENT_ATTR_STR
               42  CALL_METHOD_1         1  ''
               44  LOAD_CONST               0
               46  BINARY_SUBSCR    
               48  STORE_FAST               'attr_elem'

 L.  37        50  LOAD_FAST                'collection'
               52  LOAD_METHOD              getElementsByTagName
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                DSP_SEGMENT_CODE_STR
               58  CALL_METHOD_1         1  ''
               60  LOAD_CONST               0
               62  BINARY_SUBSCR    
               64  STORE_FAST               'code_elem'

 L.  39        66  LOAD_FAST                'self'
               68  LOAD_ATTR                elem_dict
               70  LOAD_METHOD              items
               72  CALL_METHOD_0         0  ''
               74  GET_ITER         
             76_0  COME_FROM           162  '162'
             76_1  COME_FROM           132  '132'
             76_2  COME_FROM           122  '122'
               76  FOR_ITER            164  'to 164'
               78  UNPACK_SEQUENCE_2     2 
               80  STORE_FAST               'k'
               82  STORE_FAST               'v_list'

 L.  40        84  LOAD_FAST                'k'
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                DSP_SEGMENT_ATTR_STR
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE   124  'to 124'

 L.  41        94  LOAD_FAST                'v_list'
               96  GET_ITER         
             98_0  COME_FROM           120  '120'
               98  FOR_ITER            122  'to 122'
              100  STORE_FAST               'attr'

 L.  42       102  LOAD_FAST                'self'
              104  LOAD_METHOD              parseDSPElement
              106  LOAD_FAST                'attr_elem'
              108  LOAD_FAST                'attr'
              110  CALL_METHOD_2         2  ''
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                dsp_dict
              116  LOAD_FAST                'attr'
              118  STORE_SUBSCR     
              120  JUMP_LOOP            98  'to 98'
            122_0  COME_FROM            98  '98'
              122  JUMP_LOOP            76  'to 76'
            124_0  COME_FROM            92  '92'

 L.  43       124  LOAD_FAST                'k'
              126  LOAD_FAST                'self'
              128  LOAD_ATTR                DSP_SEGMENT_CODE_STR
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_FALSE_LOOP    76  'to 76'

 L.  44       134  LOAD_FAST                'v_list'
              136  GET_ITER         
            138_0  COME_FROM           160  '160'
              138  FOR_ITER            162  'to 162'
              140  STORE_FAST               'cdata'

 L.  45       142  LOAD_FAST                'self'
              144  LOAD_METHOD              parseDSPCDATA
              146  LOAD_FAST                'code_elem'
              148  LOAD_FAST                'cdata'
              150  CALL_METHOD_2         2  ''
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                dsp_dict
              156  LOAD_FAST                'cdata'
              158  STORE_SUBSCR     
              160  JUMP_LOOP           138  'to 138'
            162_0  COME_FROM           138  '138'
              162  JUMP_LOOP            76  'to 76'
            164_0  COME_FROM            76  '76'

 L.  47       164  LOAD_FAST                'self'
              166  LOAD_ATTR                dsp_dict
              168  LOAD_STR                 'python_code'
              170  BINARY_SUBSCR    
              172  LOAD_METHOD              replace
              174  LOAD_STR                 '\\n'
              176  LOAD_STR                 '\n'
              178  CALL_METHOD_2         2  ''
              180  LOAD_FAST                'self'
              182  LOAD_ATTR                dsp_dict
              184  LOAD_STR                 'python_code'
              186  STORE_SUBSCR     

 L.  48       188  LOAD_FAST                'self'
              190  LOAD_ATTR                dsp_dict
              192  LOAD_STR                 'python_code'
              194  BINARY_SUBSCR    
              196  LOAD_METHOD              replace
              198  LOAD_STR                 '\\"'
              200  LOAD_STR                 '"'
              202  CALL_METHOD_2         2  ''
              204  LOAD_FAST                'self'
              206  LOAD_ATTR                dsp_dict
              208  LOAD_STR                 'python_code'
              210  STORE_SUBSCR     

 L.  50       212  POP_BLOCK        
              214  LOAD_CONST               0
              216  RETURN_VALUE     
            218_0  COME_FROM_FINALLY     0  '0'

 L.  51       218  DUP_TOP          
              220  LOAD_GLOBAL              Exception
              222  COMPARE_OP               exception-match
          224_226  POP_JUMP_IF_FALSE   274  'to 274'
              228  POP_TOP          
              230  STORE_FAST               'e'
              232  POP_TOP          
              234  SETUP_FINALLY       262  'to 262'

 L.  52       236  LOAD_GLOBAL              logger
              238  LOAD_METHOD              error
              240  LOAD_FAST                'e'
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          

 L.  53       246  BUILD_MAP_0           0 
              248  LOAD_FAST                'self'
              250  STORE_ATTR               dsp_dict

 L.  54       252  POP_BLOCK        
              254  POP_EXCEPT       
              256  CALL_FINALLY        262  'to 262'
              258  LOAD_CONST               -2
              260  RETURN_VALUE     
            262_0  COME_FROM           256  '256'
            262_1  COME_FROM_FINALLY   234  '234'
              262  LOAD_CONST               None
              264  STORE_FAST               'e'
              266  DELETE_FAST              'e'
              268  END_FINALLY      
              270  POP_EXCEPT       
              272  JUMP_FORWARD        276  'to 276'
            274_0  COME_FROM           224  '224'
              274  END_FINALLY      
            276_0  COME_FROM           272  '272'

Parse error at or near `POP_EXCEPT' instruction at offset 254

    def parseDSPElement(self, node, name):
        data_list = node.getElementsByTagName(name)
        if len(data_list) == 0:
            logger.error('PARSE DSP ELEMENT ERROR, NO TAG NAME %s, REUTRN NOTHING' % name)
            return ''
        if data_list[0].firstChild == None:
            return ''
        return data_list[0].firstChild.data

    def parseDSPCDATA(self, node, name):
        data_list = node.getElementsByTagName(name)
        if len(data_list) == 0:
            logger.error('PARSE DSP CDATA ERROR, NO TAG NAME %s, REUTRN NOTHING' % name)
            return ''
        if data_list[0].firstChild == None:
            return ''
        return data_list[0].firstChild.wholeText.strip()

    def parseDSPAudio--- This code section failed: ---

 L.  79       0_2  SETUP_FINALLY       258  'to 258'

 L.  80         4  LOAD_GLOBAL              xml
                6  LOAD_ATTR                dom
                8  LOAD_ATTR                minidom
               10  LOAD_METHOD              parseString
               12  LOAD_FAST                'xml_str'
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'dom_tree'

 L.  81        18  LOAD_FAST                'dom_tree'
               20  LOAD_ATTR                documentElement
               22  STORE_FAST               'collection'

 L.  83        24  LOAD_FAST                'self'
               26  LOAD_METHOD              get_xmlnode
               28  LOAD_FAST                'collection'
               30  LOAD_STR                 'audio'
               32  CALL_METHOD_2         2  ''
               34  STORE_FAST               'audio_nodes'

 L.  85        36  LOAD_FAST                'audio_nodes'
               38  GET_ITER         
             40_0  COME_FROM           250  '250'
               40  FOR_ITER            252  'to 252'
               42  STORE_FAST               'node'

 L.  86        44  LOAD_GLOBAL              int
               46  LOAD_FAST                'self'
               48  LOAD_METHOD              get_attrvalue
               50  LOAD_FAST                'node'
               52  LOAD_STR                 'id'
               54  CALL_METHOD_2         2  ''
               56  CALL_FUNCTION_1       1  ''
               58  LOAD_GLOBAL              rm_define
               60  LOAD_ATTR                media_custom_audio_0
               62  BINARY_ADD       
               64  STORE_FAST               'audio_id'

 L.  87        66  LOAD_FAST                'self'
               68  LOAD_METHOD              get_attrvalue
               70  LOAD_FAST                'node'
               72  LOAD_STR                 'name'
               74  CALL_METHOD_2         2  ''
               76  STORE_FAST               'audio_name'

 L.  88        78  LOAD_FAST                'self'
               80  LOAD_METHOD              get_attrvalue
               82  LOAD_FAST                'node'
               84  LOAD_STR                 'type'
               86  CALL_METHOD_2         2  ''
               88  STORE_FAST               'audio_type'

 L.  89        90  LOAD_FAST                'self'
               92  LOAD_METHOD              get_attrvalue
               94  LOAD_FAST                'node'
               96  LOAD_STR                 'md5'
               98  CALL_METHOD_2         2  ''
              100  STORE_FAST               'audio_md5'

 L.  90       102  LOAD_FAST                'self'
              104  LOAD_METHOD              get_attrvalue
              106  LOAD_FAST                'node'
              108  LOAD_STR                 'modify'
              110  CALL_METHOD_2         2  ''
              112  STORE_FAST               'audio_modify'

 L.  91       114  LOAD_FAST                'self'
              116  LOAD_METHOD              get_xmlnode
              118  LOAD_FAST                'node'
              120  LOAD_STR                 'audio_data'
              122  CALL_METHOD_2         2  ''
              124  STORE_FAST               'node_data'

 L.  93       126  LOAD_FAST                'audio_modify'
              128  LOAD_STR                 'true'
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_FALSE   150  'to 150'

 L.  94       134  LOAD_FAST                'self'
              136  LOAD_METHOD              get_nodevalue
              138  LOAD_FAST                'node_data'
              140  LOAD_CONST               0
              142  BINARY_SUBSCR    
              144  CALL_METHOD_1         1  ''
              146  STORE_FAST               'audio_data'
              148  JUMP_FORWARD        154  'to 154'
            150_0  COME_FROM           132  '132'

 L.  96       150  LOAD_STR                 ''
              152  STORE_FAST               'audio_data'
            154_0  COME_FROM           148  '148'

 L.  98       154  BUILD_MAP_0           0 
              156  STORE_FAST               'audio'

 L. 100       158  LOAD_GLOBAL              int
              160  LOAD_FAST                'audio_id'
              162  CALL_FUNCTION_1       1  ''

 L. 100       164  LOAD_FAST                'audio_name'

 L. 100       166  LOAD_FAST                'audio_type'

 L. 100       168  LOAD_FAST                'audio_md5'

 L. 100       170  LOAD_FAST                'audio_modify'

 L. 100       172  LOAD_FAST                'audio_data'

 L.  99       174  BUILD_TUPLE_6         6 
              176  UNPACK_SEQUENCE_6     6 
              178  LOAD_FAST                'audio'
              180  LOAD_STR                 'id'
              182  STORE_SUBSCR     
              184  LOAD_FAST                'audio'
              186  LOAD_STR                 'name'
              188  STORE_SUBSCR     
              190  LOAD_FAST                'audio'
              192  LOAD_STR                 'type'
              194  STORE_SUBSCR     
              196  LOAD_FAST                'audio'
              198  LOAD_STR                 'md5'
              200  STORE_SUBSCR     
              202  LOAD_FAST                'audio'
              204  LOAD_STR                 'modify'
              206  STORE_SUBSCR     
              208  LOAD_FAST                'audio'
              210  LOAD_STR                 'data'
              212  STORE_SUBSCR     

 L. 102       214  LOAD_FAST                'self'
              216  LOAD_ATTR                audio_list
              218  LOAD_METHOD              append
              220  LOAD_FAST                'audio'
              222  CALL_METHOD_1         1  ''
              224  POP_TOP          

 L. 103       226  LOAD_GLOBAL              logger
              228  LOAD_METHOD              info
              230  LOAD_STR                 'audio msg is %s, %s, %s, %s, %s'
              232  LOAD_FAST                'audio_id'
              234  LOAD_FAST                'audio_name'
              236  LOAD_FAST                'audio_type'
              238  LOAD_FAST                'audio_md5'
              240  LOAD_FAST                'audio_modify'
              242  BUILD_TUPLE_5         5 
              244  BINARY_MODULO    
              246  CALL_METHOD_1         1  ''
              248  POP_TOP          
              250  JUMP_LOOP            40  'to 40'
            252_0  COME_FROM            40  '40'

 L. 104       252  POP_BLOCK        
              254  LOAD_CONST               0
              256  RETURN_VALUE     
            258_0  COME_FROM_FINALLY     0  '0'

 L. 106       258  DUP_TOP          
              260  LOAD_GLOBAL              Exception
              262  COMPARE_OP               exception-match
          264_266  POP_JUMP_IF_FALSE   314  'to 314'
              268  POP_TOP          
              270  STORE_FAST               'e'
              272  POP_TOP          
              274  SETUP_FINALLY       302  'to 302'

 L. 107       276  LOAD_GLOBAL              logger
              278  LOAD_METHOD              error
              280  LOAD_FAST                'e'
              282  CALL_METHOD_1         1  ''
              284  POP_TOP          

 L. 108       286  BUILD_LIST_0          0 
              288  LOAD_FAST                'self'
              290  STORE_ATTR               audio_list

 L. 109       292  POP_BLOCK        
              294  POP_EXCEPT       
              296  CALL_FINALLY        302  'to 302'
              298  LOAD_CONST               -2
              300  RETURN_VALUE     
            302_0  COME_FROM           296  '296'
            302_1  COME_FROM_FINALLY   274  '274'
              302  LOAD_CONST               None
              304  STORE_FAST               'e'
              306  DELETE_FAST              'e'
              308  END_FINALLY      
              310  POP_EXCEPT       
              312  JUMP_FORWARD        316  'to 316'
            314_0  COME_FROM           264  '264'
              314  END_FINALLY      
            316_0  COME_FROM           312  '312'

Parse error at or near `POP_EXCEPT' instruction at offset 294

    def get_attrvalue(self, node, attrname):
        if node:
            return node.getAttribute(attrname)
        return ''

    def get_nodevalue(self, node, index=0):
        if node:
            return node.childNodes[index].nodeValue
        return ''

    def get_xmlnode(self, node, name):
        if node:
            return node.getElementsByTagName(name)
        return []