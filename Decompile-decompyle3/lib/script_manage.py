# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: .\lib\script_manage.py
# Compiled at: 2022-01-12 15:45:07
# Size of source mod 2**32: 78772 bytes
import os, socket, hashlib, builtins, math, codecs, json, shutil, threading, traceback, time, rm_define, duss_event_msg, duml_cmdset, dji_scratch_project_parser, rm_block_description, rm_ctrl, event_client, tools, builtins, rm_log, gc, rm_builtins, rm_path, base64
logger = rm_log.dji_scratch_logger_get()
rm_func_names = {'RmList':rm_builtins.RmList, 
 'rmround':rm_builtins.rmround, 
 'rmexit':rm_builtins.rmexit, 
 'number_mapping':tools.number_mapping}
safe_func_names = [
 'None',
 'False',
 'True',
 'Exception',
 'abs',
 'all',
 'bool',
 'callable',
 'chr',
 'complex',
 'divmod',
 'dict',
 'float',
 'hash',
 'hex',
 'id',
 'int',
 'isinstance',
 'issubclass',
 'list',
 'len',
 'oct',
 'ord',
 'pow',
 'range',
 'repr',
 'round',
 'slice',
 'str',
 'tuple',
 'zip',
 'exit',
 'globals',
 'locals',
 'print',
 'object',
 '__build_class__',
 '__name__',
 '__doc__']
safe_module_names = [
 'event_client',
 'rm_ctrl',
 'rm_define',
 'rm_block_description',
 'rm_log',
 'rm_communication',
 'tools',
 'time',
 'math',
 'random',
 'threading',
 'traceback',
 'tracemalloc',
 'widget',
 'multi_communication',
 'rm_socket']
safe_from_module_names = [
 'widget']

def _hook_import(name, *args, **kwargs):
    param = args[2]
    if name in safe_module_names:
        if param is None:
            return __import__(name, *args, **kwargs)
        if name in safe_from_module_names:
            return __import__(name, *args, **kwargs)
        raise RuntimeError('invalid module, the module is ' + str(name))
    else:
        raise RuntimeError('invalid module, the module is ' + str(name))


_builtins = {'__import__': _hook_import}
for name in safe_func_names:
    _builtins[name] = getattr(builtins, name)
else:
    for name, item in rm_func_names.items():
        _builtins[name] = item
    else:
        _globals = {'__builtins__': _builtins}
        _globals_exec = None

        class ScriptCtrl(object):

            def __init__(self, event_client, script_path=None):
                self.event_client = event_client
                self.msg_buff = duss_event_msg.EventMsg(tools.hostid2senderid(event_client.my_host_id))
                self.msg_buff.set_default_receiver(rm_define.mobile_id)
                self.msg_buff.set_default_cmdset(duml_cmdset.DUSS_MB_CMDSET_RM)
                self.msg_buff.set_default_cmdtype(duml_cmdset.REQ_PKG_TYPE)
                self.scratch_python_code_line_offset = 0
                self.get_framework_data()
                self.script_file_list = []
                self.has_scripts_stopping = False
                self.has_scripts_running = False
                self.run_script_id = '00000000000000000000000000000000'
                self.target_script = None
                self.scripts_running_thread_obj = None
                self.script_thread_mutex = threading.Lock()
                if script_path == None:
                    script_path = rm_path.make_data_full_path('file/')
                self.script_dirc = script_path
                if not os.path.exists(self.script_dirc):
                    logger.warn('%s is not exist! create first' % self.script_dirc)
                    os.makedirs(self.script_dirc)
                self.file_prefix = 'dji_scratch_'
                self.lab_prefix = '_lab'
                self.custom_prefix = '_custom'
                self.python_suffix = '.py'
                self.dsp_suffix = '.dsp'
                self.audio_opus_suffix = '.opus'
                self.audio_wav_suffix = '.wav'
                self.custome_skill_running = False
                self.off_control_running = False
                self.custom_skill_config_dict = {}
                self.custom_skill_config_dict = self.read_custome_skill_dict()
                self.time_counter = 0
                self.sorted_variable_name_list = None
                self.variable_name_wait_push_list = []
                self._ScriptCtrl__block_description_dict_list = []
                self._ScriptCtrl__scratch_block_state = 'IDLE'
                self._ScriptCtrl__scratch_block_dict = {'id':'ABCDEFGHIJ0123456789',  'name':'IDLE',  'type':'INFO_PUSH'}
                self._ScriptCtrl__scratch_variable_push_flag = False
                self._ScriptCtrl__scratch_variable_push_name = ''
                self.error_report_enable = True
                self.error_report_time = 0
                self.report_traceback_dict = { 'script_id': 0, 'traceback_msg': '', 'traceback_line': 0, 'traceback_len': 0, 'traceback_valid': 0}
                self.report_traceback_dict_mutex = threading.Lock()
                self.block_description_mutex = threading.Lock()
                self.block_push_timer = tools.get_timer(0.02, self.scatch_script_block_push_timer)
                self.block_push_timer.start()
                self.query()
                self.socket_obj = None
                self.uart_obj = None
                self.modules_status_ctrl_obj = None
                self.edu_enable = False

            def register_socket_obj(self, socket_obj):
                if socket_obj:
                    self.socket_obj = socket_obj

            def register_modulesStatusCtrl_obj(self, modulesStatusCtrl):
                if modulesStatusCtrl:
                    self.modules_status_ctrl_obj = modulesStatusCtrl

            def register_uart_obj(self, uart_obj):
                if uart_obj:
                    self.uart_obj = uart_obj

            def register_pipe_obj(self, pipe_obj):
                if pipe_obj:
                    self.pipe_obj = pipe_obj

            def set_edu_status(self, status):
                self.edu_enable = status

            def stop(self):
                self.block_push_timer.join()
                self.block_push_timer.stop()
                self.block_push_timer.destory()
                logger.info('SCRIPT_CTRL: STOP')

            def find_script_file_in_list(self, file_list, guid, suffix='.py'):
                target_file = None
                file_suffix = guid + suffix
                for file in file_list:
                    if file.endswith(file_suffix):
                        target_file = file
                        break
                else:
                    return target_file

            def find_audio_file_in_list(self, file_list, guid, soundid=None):
                target_file = None
                if soundid == None:
                    opus_suffix = guid + self.audio_opus_suffix
                    wav_suffix = guid + self.audio_wav_suffix
                    for file in file_list:
                        while not file.endswith(opus_suffix):
                            if file.endswith(opus_suffix):
                                pass
                            target_file = file
                            break

                else:
                    opus_suffix = str(hex(soundid)) + '_' + guid + self.audio_opus_suffix
                    wav_suffix = str(hex(soundid)) + '_' + guid + self.audio_wav_suffix
                for file in file_list:
                    while not file.endswith(opus_suffix):
                        if file.endswith(opus_suffix):
                            pass
                        target_file = file
                        break

                    return target_file

            def check_dsp_file(self, guid, sign):
                self.query()
                target_file = self.find_script_file_in_list(self.script_file_list, guid, self.dsp_suffix)
                if target_file == None:
                    return duml_cmdset.DUSS_MB_RET_NO_EXIST_DSP
                dsp_str = self.read_script_string(os.path.join(self.script_dirc, target_file))
                dsp_parser = dji_scratch_project_parser.DSPXMLParser()
                dsp_parser.parseDSPString(dsp_str)
                if 'sign' not in dsp_parser.dsp_dict.keys() or dsp_parser.dsp_dict['sign'] != sign:
                    return duml_cmdset.DUSS_MB_RET_NO_EXIST_DSP
                return duml_cmdset.DUSS_MB_RET_OK

            def check_audio_file--- This code section failed: ---

 L. 270         0  LOAD_FAST                'self'
                2  LOAD_METHOD              query
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 271         8  BUILD_LIST_0          0 
               10  STORE_FAST               'match_list'

 L. 272        12  LOAD_FAST                'self'
               14  LOAD_METHOD              find_script_file_in_list
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                script_file_list
               20  LOAD_FAST                'guid'
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                dsp_suffix
               26  CALL_METHOD_3         3  ''
               28  STORE_FAST               'target_file'

 L. 273        30  LOAD_FAST                'target_file'
               32  LOAD_CONST               None
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    48  'to 48'

 L. 274        38  LOAD_GLOBAL              duml_cmdset
               40  LOAD_ATTR                DUSS_MB_RET_NO_EXIST_DSP
               42  LOAD_FAST                'match_list'
               44  BUILD_TUPLE_2         2 
               46  RETURN_VALUE     
             48_0  COME_FROM            36  '36'

 L. 276     48_50  SETUP_FINALLY       626  'to 626'

 L. 277        52  LOAD_GLOBAL              open
               54  LOAD_GLOBAL              os
               56  LOAD_ATTR                path
               58  LOAD_METHOD              join
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                script_dirc
               64  LOAD_FAST                'target_file'
               66  CALL_METHOD_2         2  ''
               68  LOAD_STR                 'rb'
               70  CALL_FUNCTION_2       2  ''
               72  STORE_FAST               'fd'

 L. 278        74  LOAD_FAST                'fd'
               76  LOAD_METHOD              read
               78  CALL_METHOD_0         0  ''
               80  STORE_FAST               'dsp_buff'

 L. 279        82  LOAD_FAST                'fd'
               84  LOAD_METHOD              close
               86  CALL_METHOD_0         0  ''
               88  POP_TOP          

 L. 280        90  LOAD_GLOBAL              dji_scratch_project_parser
               92  LOAD_METHOD              DSPXMLParser
               94  CALL_METHOD_0         0  ''
               96  STORE_FAST               'dsp_parser'

 L. 281        98  LOAD_FAST                'dsp_parser'
              100  LOAD_METHOD              parseDSPAudio
              102  LOAD_FAST                'dsp_buff'
              104  CALL_METHOD_1         1  ''
              106  STORE_FAST               'dsp_res'

 L. 282       108  LOAD_FAST                'dsp_res'
              110  LOAD_CONST               -2
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   148  'to 148'

 L. 283       116  LOAD_GLOBAL              logger
              118  LOAD_METHOD              error
              120  LOAD_STR                 'SCRIPT_CTRL: audio file parse failure'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          

 L. 284       126  LOAD_GLOBAL              logger
              128  LOAD_METHOD              error
              130  LOAD_GLOBAL              dsp_buffer
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          

 L. 285       136  LOAD_GLOBAL              rm_define
              138  LOAD_ATTR                DUSS_ERR_FAILURE
              140  LOAD_FAST                'match_list'
              142  BUILD_TUPLE_2         2 
              144  POP_BLOCK        
              146  RETURN_VALUE     
            148_0  COME_FROM           114  '114'

 L. 286       148  LOAD_FAST                'dsp_parser'
              150  LOAD_ATTR                audio_list
              152  STORE_FAST               'aud_list'

 L. 288       154  LOAD_GLOBAL              len
              156  LOAD_FAST                'aud_list'
              158  CALL_FUNCTION_1       1  ''
              160  LOAD_GLOBAL              len
              162  LOAD_FAST                'dict'
              164  CALL_FUNCTION_1       1  ''
              166  COMPARE_OP               >
          168_170  POP_JUMP_IF_FALSE   374  'to 374'

 L. 289       172  LOAD_FAST                'aud_list'
              174  GET_ITER         
            176_0  COME_FROM           372  '372'
            176_1  COME_FROM           360  '360'
            176_2  COME_FROM           208  '208'
              176  FOR_ITER            374  'to 374'
              178  STORE_FAST               'aud_dict'

 L. 290       180  LOAD_GLOBAL              str
              182  LOAD_FAST                'aud_dict'
              184  LOAD_STR                 'id'
              186  BINARY_SUBSCR    
              188  LOAD_GLOBAL              rm_define
              190  LOAD_ATTR                media_custom_audio_0
              192  BINARY_SUBTRACT  
              194  CALL_FUNCTION_1       1  ''
              196  STORE_FAST               'index'

 L. 291       198  LOAD_FAST                'index'
              200  LOAD_FAST                'dict'
              202  LOAD_METHOD              keys
              204  CALL_METHOD_0         0  ''
              206  COMPARE_OP               not-in
              208  POP_JUMP_IF_FALSE_LOOP   176  'to 176'

 L. 292       210  LOAD_FAST                'aud_dict'
              212  LOAD_STR                 'type'
              214  BINARY_SUBSCR    
              216  LOAD_STR                 'opus'
              218  COMPARE_OP               ==
          220_222  POP_JUMP_IF_FALSE   266  'to 266'

 L. 293       224  LOAD_FAST                'self'
              226  LOAD_ATTR                file_prefix
              228  LOAD_GLOBAL              str
              230  LOAD_GLOBAL              hex
              232  LOAD_FAST                'aud_dict'
              234  LOAD_STR                 'id'
              236  BINARY_SUBSCR    
              238  CALL_FUNCTION_1       1  ''
              240  CALL_FUNCTION_1       1  ''
              242  BINARY_ADD       
              244  LOAD_STR                 '_'
              246  BINARY_ADD       
              248  LOAD_GLOBAL              str
              250  LOAD_FAST                'guid'
              252  CALL_FUNCTION_1       1  ''
              254  BINARY_ADD       
              256  LOAD_FAST                'self'
              258  LOAD_ATTR                audio_opus_suffix
              260  BINARY_ADD       
              262  STORE_FAST               'file_name'
              264  JUMP_FORWARD        320  'to 320'
            266_0  COME_FROM           220  '220'

 L. 294       266  LOAD_FAST                'aud_dict'
              268  LOAD_STR                 'type'
              270  BINARY_SUBSCR    
              272  LOAD_STR                 'wav'
              274  COMPARE_OP               ==
          276_278  POP_JUMP_IF_FALSE   320  'to 320'

 L. 295       280  LOAD_FAST                'self'
              282  LOAD_ATTR                file_prefix
              284  LOAD_GLOBAL              str
              286  LOAD_GLOBAL              hex
              288  LOAD_FAST                'aud_dict'
              290  LOAD_STR                 'id'
              292  BINARY_SUBSCR    
              294  CALL_FUNCTION_1       1  ''
              296  CALL_FUNCTION_1       1  ''
              298  BINARY_ADD       
              300  LOAD_STR                 '_'
              302  BINARY_ADD       
              304  LOAD_GLOBAL              str
              306  LOAD_FAST                'guid'
              308  CALL_FUNCTION_1       1  ''
              310  BINARY_ADD       
              312  LOAD_FAST                'self'
              314  LOAD_ATTR                audio_wav_suffix
              316  BINARY_ADD       
              318  STORE_FAST               'file_name'
            320_0  COME_FROM           276  '276'
            320_1  COME_FROM           264  '264'

 L. 296       320  LOAD_GLOBAL              os
              322  LOAD_ATTR                path
              324  LOAD_METHOD              join
              326  LOAD_FAST                'self'
              328  LOAD_ATTR                script_dirc
              330  LOAD_FAST                'file_name'
              332  CALL_METHOD_2         2  ''
              334  STORE_FAST               'delete_file_name'

 L. 297       336  LOAD_GLOBAL              logger
              338  LOAD_METHOD              error
              340  LOAD_STR                 'SCRIPT_CTRL: delete audio file: '
              342  LOAD_FAST                'delete_file_name'
              344  BINARY_ADD       
              346  CALL_METHOD_1         1  ''
              348  POP_TOP          

 L. 298       350  LOAD_GLOBAL              os
              352  LOAD_ATTR                path
              354  LOAD_METHOD              exists
              356  LOAD_FAST                'delete_file_name'
              358  CALL_METHOD_1         1  ''
              360  POP_JUMP_IF_FALSE_LOOP   176  'to 176'

 L. 299       362  LOAD_GLOBAL              os
              364  LOAD_METHOD              remove
              366  LOAD_FAST                'delete_file_name'
              368  CALL_METHOD_1         1  ''
              370  POP_TOP          
              372  JUMP_LOOP           176  'to 176'
            374_0  COME_FROM           176  '176'
            374_1  COME_FROM           168  '168'

 L. 301       374  LOAD_FAST                'aud_list'
              376  GET_ITER         
            378_0  COME_FROM           610  '610'
              378  FOR_ITER            614  'to 614'
              380  STORE_FAST               'aud_dict'

 L. 302       382  LOAD_CONST               0
              384  STORE_FAST               'match'

 L. 303       386  LOAD_GLOBAL              str
              388  LOAD_FAST                'aud_dict'
              390  LOAD_STR                 'id'
              392  BINARY_SUBSCR    
              394  LOAD_GLOBAL              rm_define
              396  LOAD_ATTR                media_custom_audio_0
              398  BINARY_SUBTRACT  
              400  CALL_FUNCTION_1       1  ''
              402  STORE_FAST               'index'

 L. 305       404  LOAD_FAST                'aud_dict'
              406  LOAD_STR                 'type'
              408  BINARY_SUBSCR    
              410  LOAD_STR                 'opus'
              412  COMPARE_OP               ==
          414_416  POP_JUMP_IF_FALSE   460  'to 460'

 L. 306       418  LOAD_FAST                'self'
              420  LOAD_ATTR                file_prefix
              422  LOAD_GLOBAL              str
              424  LOAD_GLOBAL              hex
              426  LOAD_FAST                'aud_dict'
              428  LOAD_STR                 'id'
              430  BINARY_SUBSCR    
              432  CALL_FUNCTION_1       1  ''
              434  CALL_FUNCTION_1       1  ''
              436  BINARY_ADD       
              438  LOAD_STR                 '_'
              440  BINARY_ADD       
              442  LOAD_GLOBAL              str
              444  LOAD_FAST                'guid'
              446  CALL_FUNCTION_1       1  ''
              448  BINARY_ADD       
              450  LOAD_FAST                'self'
              452  LOAD_ATTR                audio_opus_suffix
              454  BINARY_ADD       
              456  STORE_FAST               'file_name'
              458  JUMP_FORWARD        514  'to 514'
            460_0  COME_FROM           414  '414'

 L. 307       460  LOAD_FAST                'aud_dict'
              462  LOAD_STR                 'type'
              464  BINARY_SUBSCR    
              466  LOAD_STR                 'wav'
              468  COMPARE_OP               ==
          470_472  POP_JUMP_IF_FALSE   514  'to 514'

 L. 308       474  LOAD_FAST                'self'
              476  LOAD_ATTR                file_prefix
              478  LOAD_GLOBAL              str
              480  LOAD_GLOBAL              hex
              482  LOAD_FAST                'aud_dict'
              484  LOAD_STR                 'id'
              486  BINARY_SUBSCR    
              488  CALL_FUNCTION_1       1  ''
              490  CALL_FUNCTION_1       1  ''
              492  BINARY_ADD       
              494  LOAD_STR                 '_'
              496  BINARY_ADD       
              498  LOAD_GLOBAL              str
              500  LOAD_FAST                'guid'
              502  CALL_FUNCTION_1       1  ''
              504  BINARY_ADD       
              506  LOAD_FAST                'self'
              508  LOAD_ATTR                audio_wav_suffix
              510  BINARY_ADD       
              512  STORE_FAST               'file_name'
            514_0  COME_FROM           470  '470'
            514_1  COME_FROM           458  '458'

 L. 309       514  LOAD_GLOBAL              os
              516  LOAD_ATTR                path
              518  LOAD_METHOD              join
              520  LOAD_FAST                'self'
              522  LOAD_ATTR                script_dirc
              524  LOAD_FAST                'file_name'
              526  CALL_METHOD_2         2  ''
              528  STORE_FAST               'audio_file_name'

 L. 311       530  LOAD_FAST                'index'
              532  LOAD_FAST                'dict'
              534  LOAD_METHOD              keys
              536  CALL_METHOD_0         0  ''
              538  COMPARE_OP               not-in
          540_542  POP_JUMP_IF_FALSE   550  'to 550'

 L. 312       544  POP_TOP          
          546_548  BREAK_LOOP          614  'to 614'
            550_0  COME_FROM           540  '540'

 L. 313       550  LOAD_FAST                'aud_dict'
              552  LOAD_STR                 'md5'
              554  BINARY_SUBSCR    
              556  LOAD_FAST                'dict'
              558  LOAD_FAST                'index'
              560  BINARY_SUBSCR    
              562  COMPARE_OP               ==
          564_566  POP_JUMP_IF_FALSE   586  'to 586'
              568  LOAD_GLOBAL              os
              570  LOAD_ATTR                path
              572  LOAD_METHOD              exists
              574  LOAD_FAST                'audio_file_name'
              576  CALL_METHOD_1         1  ''
          578_580  POP_JUMP_IF_FALSE   586  'to 586'

 L. 314       582  LOAD_CONST               1
              584  STORE_FAST               'match'
            586_0  COME_FROM           578  '578'
            586_1  COME_FROM           564  '564'

 L. 315       586  LOAD_FAST                'match_list'
              588  LOAD_METHOD              append
              590  LOAD_GLOBAL              int
              592  LOAD_FAST                'index'
              594  CALL_FUNCTION_1       1  ''
              596  CALL_METHOD_1         1  ''
              598  POP_TOP          

 L. 316       600  LOAD_FAST                'match_list'
              602  LOAD_METHOD              append
              604  LOAD_FAST                'match'
              606  CALL_METHOD_1         1  ''
              608  POP_TOP          
          610_612  JUMP_LOOP           378  'to 378'
            614_0  COME_FROM           546  '546'
            614_1  COME_FROM           378  '378'

 L. 317       614  LOAD_GLOBAL              duml_cmdset
              616  LOAD_ATTR                DUSS_MB_RET_OK
              618  LOAD_FAST                'match_list'
              620  BUILD_TUPLE_2         2 
              622  POP_BLOCK        
              624  RETURN_VALUE     
            626_0  COME_FROM_FINALLY    48  '48'

 L. 318       626  POP_TOP          
              628  POP_TOP          
              630  POP_TOP          

 L. 319       632  LOAD_GLOBAL              logger
              634  LOAD_METHOD              fatal
              636  LOAD_GLOBAL              traceback
              638  LOAD_METHOD              format_exc
              640  CALL_METHOD_0         0  ''
              642  CALL_METHOD_1         1  ''
              644  POP_TOP          

 L. 320       646  LOAD_GLOBAL              duml_cmdset
              648  LOAD_ATTR                DUSS_MB_RET_INVALID_STATE
              650  LOAD_FAST                'match_list'
              652  BUILD_TUPLE_2         2 
              654  ROT_FOUR         
              656  POP_EXCEPT       
              658  RETURN_VALUE     
              660  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 644

            def transcode_audio_file(self, guid, customid, event_client, msg):
                duss_result = rm_define.DUSS_SUCCESS
                self.query()
                if customid != None:
                    if customid not in self.custom_skill_config_dict.keys():
                        logger.warn('SCRIPT_CTRL: auto program is not configured')
                        return rm_define.DUSS_ERR_FAILURE
                    guid = self.custom_skill_config_dict[customid]
                logger.info('SCRIPT_CTRL: transcode_audio_file guid is ' + str(guid))
                if self.find_audio_file_in_list(self.script_file_list, guid) != None:
                    for sound_id in range(rm_define.media_custom_audio_0, rm_define.media_custom_audio_9 + 1):
                        target_file = self.find_audio_file_in_list(self.script_file_list, guid, sound_id)
                        if target_file == None:
                            action = 0
                            sound_type = 0
                        else:
                            action = 1
                            if target_file.endswith(self.audio_opus_suffix):
                                sound_type = 0
                            else:
                                if target_file.endswith(self.audio_wav_suffix):
                                    sound_type = 1
                        self.msg_buff.init()
                        self.msg_buff.append('action', 'uint8', action)
                        self.msg_buff.append('type', 'uint8', sound_type)
                        self.msg_buff.append('soundid', 'uint32', sound_id)
                        self.msg_buff.append('guid', 'string', guid)
                        self.msg_buff.receiver = rm_define.hdvt_uav_id
                        self.msg_buff.cmd_id = duml_cmdset.DUSS_MB_CMD_RM_CUSTOM_SOUND_CONVERT
                        duss_result, resp = self.event_client.send_sync(self.msg_buff)
                        if duss_result != rm_define.DUSS_SUCCESS:
                            return duss_result

                else:
                    return duss_result
                return duss_result

            def exit_low_power_mode(self, event_client, msg):
                self.msg_buff.init()
                self.msg_buff.append('action', 'uint8', 0)
                self.msg_buff.receiver = rm_define.hdvt_uav_id
                self.msg_buff.cmd_id = duml_cmdset.DUSS_MB_CMD_RM_EXIT_LOW_POWER_MODE
                duss_result, resp = self.event_client.send_sync(self.msg_buff)
                return duss_result

            def query(self):
                try:
                    if not os.path.exists(self.script_dirc):
                        os.makedirs(self.script_dirc)
                    self.script_file_list = os.listdir(self.script_dirc)
                except:
                    logger.fatal(traceback.format_exc())

            def scratch_python_code_line_offset_get(self, framework_data):
                script_data_list = framework_data.splitlines()
                try:
                    self.scratch_python_code_line_offset = script_data_list.index('SCRATCH_PYTHON_CODE')
                    logger.info('user python code offset is %d' % self.scratch_python_code_line_offset)
                except:
                    logger.error('GET SCRATCH_PYTHON_CODE OFFSET ERROR')
                    self.scratch_python_code_line_offset = 0

            def get_framework_data(self):
                try:
                    framework_fd = codecs.open((rm_path.make_src_full_path('framework/script_framework.py')), 'r', encoding='utf-8')
                    self.framework_data = framework_fd.read()
                    self.scratch_python_code_line_offset_get(self.framework_data)
                    framework_fd.close()
                    custom_skill_framework_fd = codecs.open((rm_path.make_src_full_path('framework/custom_skill_framework.py')), 'r', encoding='utf-8')
                    self.custome_skill_framework_data = custom_skill_framework_fd.read()
                    custom_skill_framework_fd.close()
                except:
                    logger.fatal("SCRIPT_CTRL: No framework code file, please make sure the 'framework.py' exits")

            def read_script_string--- This code section failed: ---

 L. 399         0  SETUP_FINALLY        40  'to 40'

 L. 400         2  LOAD_GLOBAL              codecs
                4  LOAD_ATTR                open
                6  LOAD_FAST                'file_name'
                8  LOAD_STR                 'r'
               10  LOAD_STR                 'utf-8'
               12  LOAD_CONST               ('encoding',)
               14  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               16  STORE_FAST               'fd'

 L. 401        18  LOAD_FAST                'fd'
               20  LOAD_METHOD              read
               22  CALL_METHOD_0         0  ''
               24  STORE_FAST               'str'

 L. 402        26  LOAD_FAST                'fd'
               28  LOAD_METHOD              close
               30  CALL_METHOD_0         0  ''
               32  POP_TOP          

 L. 403        34  LOAD_FAST                'str'
               36  POP_BLOCK        
               38  RETURN_VALUE     
             40_0  COME_FROM_FINALLY     0  '0'

 L. 404        40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 405        46  LOAD_GLOBAL              logger
               48  LOAD_METHOD              fatal
               50  LOAD_GLOBAL              traceback
               52  LOAD_METHOD              format_exc
               54  CALL_METHOD_0         0  ''
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
               64  END_FINALLY      
             66_0  COME_FROM            62  '62'

Parse error at or near `POP_TOP' instruction at offset 58

            def write_script_string(self, file_name, buffer):
                try:
                    script_fd = codecs.open(file_name, 'w', encoding='utf-8')
                    script_fd.write(buffer)
                    script_fd.close()
                except:
                    logger.fatal(traceback.format_exc())

            def reset_states(self):
                logger.info('----reset_states start----')
                self.script_thread_mutex.acquire()
                self.has_scripts_stopping = False
                self.has_scripts_running = False
                self.run_script_id = '00000000000000000000000000000000'
                self.target_script = None
                self.scripts_running_thread_obj = None
                self.custome_skill_running = False
                self.off_control_running = False
                self.script_thread_mutex.release()
                logger.info('----reset_states end----')

            def set_states(self, running, script_id, target_script, thread_obj, custom, off_control):
                self.script_thread_mutex.acquire()
                self.has_scripts_running = running
                self.run_script_id = script_id
                self.target_script = target_script
                self.scripts_running_thread_obj = thread_obj
                self.custome_skill_running = custom
                self.off_control_running = off_control
                self.script_thread_mutex.release()

            def start_running(self, script_id, custome_id):
                self.query()
                if self.has_scripts_running:
                    logger.warn('SCRIPT_CTRL: has script running')
                    return rm_define.DUSS_ERR_BUSY
                if custome_id != None:
                    if custome_id not in self.custom_skill_config_dict.keys():
                        logger.warn('SCRIPT_CTRL: auto program is not configured')
                        return rm_define.DUSS_ERR_FAILURE
                    script_id = self.custom_skill_config_dict[custome_id]
                    file_suffix = self.custom_prefix + self.python_suffix
                    if int(custome_id) >= 0 and int(custome_id) <= 9:
                        logger.info('SCRIPT_CTRL: custome skill start!')
                        custom_skill_flag, off_control_flag = (True, False)
                    else:
                        logger.info('SCRIPT_CTRL: off control start!')
                        custom_skill_flag, off_control_flag = (False, True)
                else:
                    file_suffix = self.lab_prefix + self.python_suffix
                    custom_skill_flag, off_control_flag = (False, False)
                target_script = self.find_script_file_in_list(self.script_file_list, script_id, file_suffix)
                if target_script != None:
                    self.set_states(True, script_id, target_script, None, custom_skill_flag, off_control_flag)
                    script_thread_obj = threading.Thread(target=(self.execute_thread))
                    self.set_states(True, script_id, target_script, script_thread_obj, custom_skill_flag, off_control_flag)
                    script_thread_obj.start()
                    return rm_define.DUSS_SUCCESS
                logger.error('SCRIPT_CTRL: can not find script id = ' + str(script_id))
                return rm_define.DUSS_ERR_FAILURE

            def stop_running(self, script_id, custome_id):
                global _globals_exec
                if custome_id != None:
                    if custome_id not in self.custom_skill_config_dict.keys():
                        logger.error('SCRIPT_CTRL: custome skill is not configured')
                        return rm_define.DUSS_ERR_FAILURE
                    script_id = self.custom_skill_config_dict[custome_id]
                    file_suffix = self.custom_prefix + self.python_suffix
                else:
                    file_suffix = self.lab_prefix + self.python_suffix
                file_suffix = script_id + file_suffix
                if self.has_scripts_running == False or self.target_script == None or self.target_script.endswith(file_suffix):
                    logger.warn('SCRIPT_CTRL: no request script running!')
                    return rm_define.DUSS_ERR_FAILURE
                if self.has_scripts_stopping:
                    logger.warn('SCRIPT_CTRL: there is script has been stopping!')
                    return rm_define.DUSS_ERR_FAILURE
                logger.warn('SCRIPT_CTRL: cur script will enter stopping, set script_stopping status!')
                self.has_scripts_stopping = True
                try:
                    if isinstance(_globals_exec, dict) and 'event' in _globals_exec.keys() and _globals_exec['event'].script_state.check_script_has_stopped() == False:
                        _globals_exec['event'].script_state.set_stop_flag()
                        logger.warn('SCRIPT_CTRL: script are going to finish! not report error')
                        self.error_report_enable = False
                    else:
                        logger.warn('SCRIPT_CTRL: script are going to finish!')
                        return rm_define.DUSS_SUCCESS
                except Exception as e:
                    try:
                        logger.fatal(traceback.format_exc())
                    finally:
                        e = None
                        del e

                else:
                    logger.info('\n**************** script exit successful ****************')
                    return rm_define.DUSS_SUCCESS

            def reset_whole_script_state(self):
                logger.info('----reset_whole_script_state start----')
                self.reset_states()
                self.reset_block_state_pusher()
                logger.info('----reset_whole_script_state end----')

            def execute_thread(self):
                global _globals_exec
                script_file_name = self.script_dirc + self.target_script
                self.clear_report_traceback_msg()
                _error_msg = ''
                try:
                    try:
                        _globals['block_description_push'] = self.push_block_description_info_to_timer
                        _globals['_error_msg'] = ''
                        _globals['socket_ctrl'] = self.socket_obj
                        _globals['modules_status_ctrl'] = self.modules_status_ctrl_obj
                        _globals['__builtins__']['__import__'] = _hook_import
                        _globals['edu_enable'] = self.edu_enable
                        if self.edu_enable:
                            _globals['serial_ctrl'] = self.uart_obj
                        _globals_exec = dict(_globals)
                        script_str = self.read_script_string(script_file_name)
                        if self.custome_skill_running:
                            self.set_block_to_CUSTOME_SKILL()
                        else:
                            if self.off_control_running:
                                _globals_exec['speed_limit_mode'] = True
                                self.set_block_to_OFF_CONTROL()
                            else:
                                self.set_block_to_RUN()
                        logger.fatal('**************** script start successful ****************')
                        logger.fatal('MANAGER: EXEC filename = ' + script_file_name)
                        logger.fatal('MANAGER: EXEC code: ')
                        logger.info(script_str)
                        lt = time.time()
                        exec(script_str, _globals_exec)
                    except Exception as e:
                        try:
                            logger.fatal(traceback.format_exc())
                            _error_msg = traceback.format_exc()
                        finally:
                            e = None
                            del e

                finally:
                    self.uart_obj.reinit_event_client(self.event_client)
                    if _error_msg == '':
                        _error_msg = _globals_exec['_error_msg']
                    if self.error_report_enable:
                        logger.info('---error_report_enable---')
                        self.block_description_mutex.acquire()
                        block_id = self._ScriptCtrl__scratch_block_dict['id']
                        if len(self._ScriptCtrl__block_description_dict_list) != 0:
                            block_id = self._ScriptCtrl__block_description_dict_list[-1]['id']
                        self.block_description_mutex.release()
                        self.update_report_traceback_msg(self.run_script_id, block_id, _error_msg)
                    else:
                        logger.info('Not report traceback msg')
                        self.error_report_enable = True
                    logger.info('event stop start ----')
                    if isinstance(_globals_exec, dict):
                        if 'event' in _globals_exec.keys():
                            logger.info('event stop ing ----')
                            _globals_exec['event'].stop()
                            logger.info('event stop end1')
                            del _globals_exec['event']
                            logger.info('event stop end2')
                    logger.info('wait 3s start ---')
                    timeout_count = 0
                    while len(self.variable_name_wait_push_list) != 0:
                        while timeout_count < 150:
                            logger.info('wait 3s ing ---')
                            timeout_count += 1
                            time.sleep(0.02)

                    logger.info('variable push finish')
                    ct = time.time()
                    if ct - lt < 0.1:
                        logger.info('exec too fast, wait 0.1s to make sure block state to be updated successfully')
                        time.sleep(0.1)
                    logger.info('reset_whole_script_state start')
                    self.reset_whole_script_state()
                    logger.info('reset_whole_script_state finsh')
                    _globals_exec = None
                    gc.collect()
                    logger.fatal('\n**************** script finsh successful ****************')

            def get_script_data--- This code section failed: ---

 L. 608         0  LOAD_GLOBAL              duml_cmdset
                2  LOAD_ATTR                DUSS_MB_RET_FINSH
                4  STORE_FAST               'duss_result'

 L. 609         6  SETUP_FINALLY       164  'to 164'

 L. 610         8  LOAD_GLOBAL              dji_scratch_project_parser
               10  LOAD_METHOD              DSPXMLParser
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'dsp_parser'

 L. 611        16  LOAD_FAST                'dsp_parser'
               18  LOAD_METHOD              parseDSPString
               20  LOAD_FAST                'buffer'
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'dsp_res'

 L. 612        26  LOAD_FAST                'dsp_res'
               28  LOAD_CONST               -1
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    62  'to 62'

 L. 613        34  LOAD_GLOBAL              logger
               36  LOAD_METHOD              error
               38  LOAD_STR                 'SCRIPT_CTRL: dsp file MD5 check failure'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L. 614        44  LOAD_GLOBAL              duml_cmdset
               46  LOAD_ATTR                DUSS_MB_RET_MD5_CHECK_FAILUE
               48  LOAD_CONST               None
               50  LOAD_CONST               None
               52  LOAD_CONST               None
               54  LOAD_CONST               None
               56  BUILD_TUPLE_5         5 
               58  POP_BLOCK        
               60  RETURN_VALUE     
             62_0  COME_FROM            32  '32'

 L. 615        62  LOAD_FAST                'dsp_res'
               64  LOAD_CONST               -2
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE   108  'to 108'

 L. 616        70  LOAD_GLOBAL              logger
               72  LOAD_METHOD              error
               74  LOAD_STR                 'SCRIPT_CTRL: dsp file parse failure'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L. 617        80  LOAD_GLOBAL              logger
               82  LOAD_METHOD              error
               84  LOAD_FAST                'buffer'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          

 L. 618        90  LOAD_GLOBAL              rm_define
               92  LOAD_ATTR                DUSS_ERR_FAILURE
               94  LOAD_CONST               None
               96  LOAD_CONST               None
               98  LOAD_CONST               None
              100  LOAD_CONST               None
              102  BUILD_TUPLE_5         5 
              104  POP_BLOCK        
              106  RETURN_VALUE     
            108_0  COME_FROM            68  '68'

 L. 619       108  LOAD_FAST                'dsp_parser'
              110  LOAD_ATTR                dsp_dict
              112  LOAD_STR                 'python_code'
              114  BINARY_SUBSCR    
              116  STORE_FAST               'script_data'

 L. 620       118  LOAD_FAST                'dsp_parser'
              120  LOAD_ATTR                dsp_dict
              122  LOAD_STR                 'guid'
              124  BINARY_SUBSCR    
              126  STORE_FAST               'guid'

 L. 621       128  LOAD_FAST                'dsp_parser'
              130  LOAD_ATTR                dsp_dict
              132  LOAD_STR                 'sign'
              134  BINARY_SUBSCR    
              136  STORE_FAST               'sign'

 L. 622       138  LOAD_FAST                'dsp_parser'
              140  LOAD_ATTR                dsp_dict
              142  LOAD_STR                 'code_type'
              144  BINARY_SUBSCR    
              146  STORE_FAST               'code_type'

 L. 623       148  LOAD_FAST                'duss_result'
              150  LOAD_FAST                'script_data'
              152  LOAD_FAST                'guid'
              154  LOAD_FAST                'sign'
              156  LOAD_FAST                'code_type'
              158  BUILD_TUPLE_5         5 
              160  POP_BLOCK        
              162  RETURN_VALUE     
            164_0  COME_FROM_FINALLY     6  '6'

 L. 624       164  POP_TOP          
              166  POP_TOP          
              168  POP_TOP          

 L. 625       170  LOAD_GLOBAL              logger
              172  LOAD_METHOD              fatal
              174  LOAD_GLOBAL              traceback
              176  LOAD_METHOD              format_exc
              178  CALL_METHOD_0         0  ''
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          
              184  POP_EXCEPT       
              186  JUMP_FORWARD        190  'to 190'
              188  END_FINALLY      
            190_0  COME_FROM           186  '186'

Parse error at or near `POP_TOP' instruction at offset 182

            def get_audio_data--- This code section failed: ---

 L. 628         0  LOAD_GLOBAL              duml_cmdset
                2  LOAD_ATTR                DUSS_MB_RET_FINSH
                4  STORE_FAST               'duss_result'

 L. 629         6  SETUP_FINALLY        82  'to 82'

 L. 630         8  LOAD_GLOBAL              dji_scratch_project_parser
               10  LOAD_METHOD              DSPXMLParser
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'dsp_parser'

 L. 631        16  LOAD_FAST                'dsp_parser'
               18  LOAD_METHOD              parseDSPAudio
               20  LOAD_FAST                'buffer'
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'dsp_res'

 L. 632        26  LOAD_FAST                'dsp_res'
               28  LOAD_CONST               -2
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    66  'to 66'

 L. 633        34  LOAD_GLOBAL              logger
               36  LOAD_METHOD              error
               38  LOAD_STR                 'SCRIPT_CTRL: audio file parse failure'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L. 634        44  LOAD_GLOBAL              logger
               46  LOAD_METHOD              error
               48  LOAD_FAST                'buffer'
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L. 635        54  LOAD_GLOBAL              rm_define
               56  LOAD_ATTR                DUSS_ERR_FAILURE
               58  LOAD_CONST               None
               60  BUILD_TUPLE_2         2 
               62  POP_BLOCK        
               64  RETURN_VALUE     
             66_0  COME_FROM            32  '32'

 L. 636        66  LOAD_FAST                'dsp_parser'
               68  LOAD_ATTR                audio_list
               70  STORE_FAST               'aud_list'

 L. 637        72  LOAD_FAST                'duss_result'
               74  LOAD_FAST                'aud_list'
               76  BUILD_TUPLE_2         2 
               78  POP_BLOCK        
               80  RETURN_VALUE     
             82_0  COME_FROM_FINALLY     6  '6'

 L. 638        82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 639        88  LOAD_GLOBAL              logger
               90  LOAD_METHOD              fatal
               92  LOAD_GLOBAL              traceback
               94  LOAD_METHOD              format_exc
               96  CALL_METHOD_0         0  ''
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          
              102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
              106  END_FINALLY      
            108_0  COME_FROM           104  '104'

Parse error at or near `POP_TOP' instruction at offset 100

            def script_add_indent(self, script_data):
                script_data_list = script_data.splitlines()
                script_data = ''
                for script_oneline in script_data_list:
                    script_data = script_data + '    ' + script_oneline + '\n'
                else:
                    return script_data

            def parse_descriptions(self, script_data):
                script_data_list = script_data.splitlines()
                script_data = ''
                for script_oneline in script_data_list:
                    if script_oneline.find('#') != -1:
                        s_list = script_oneline.split('#', 1)
                        t_dict, res = rm_block_description.parse_oneline_block_description('#' + s_list[1])
                        if 'block' in t_dict.keys():
                            script_oneline = s_list[0] + 'block_description_push(' + s_list[1][len('block '):].replace(' ', ', ') + ')'
                    script_data = script_data + script_oneline + '\n'
                else:
                    return script_data

            def script_add_check_point(self, script_data):
                script_data_list = script_data.splitlines()
                script_data = ''
                for script_oneline in script_data_list:
                    if '#' not in script_oneline:
                        while not 'while ' in script_oneline:
                            if 'while(' in script_oneline or 'for ' in script_onelineand ' in ' in script_oneline and ' in ' in script_oneline:
                                space_num = 0
                                if 'while ' in script_oneline:
                                    space_num = script_oneline.find('while ')
                                if 'while(' in script_oneline:
                                    space_num = script_oneline.find('while(')
                                else:
                                    if 'for ' in script_oneline:
                                        if ' in ' in script_oneline:
                                            if ':' in script_oneline:
                                                space_num = script_oneline.find('for')
                                space_str = (4 + space_num) * ' '
                                add_str = '\n' + space_str + 'time.sleep(0.005)'
                                script_oneline += add_str
                            script_data = script_data + script_oneline + '\n'

                        return script_data

            def create_file(self, data, event_client):
                if not self.has_scripts_running:
                    self.set_block_to_START()
                duss_result = duml_cmdset.DUSS_MB_RET_FINSH
                self.query()
                dsp_buffer_byte = tools.pack_to_byte(data)
                dsp_buffer = dsp_buffer_byte.decode('utf-8')
                duss_result, script_data, file_guid, sign, code_type = self.get_script_data(dsp_buffer)
                if duss_result != duml_cmdset.DUSS_MB_RET_FINSH:
                    return duss_result
                script_data = self.script_add_check_point(script_data)
                script_data = self.script_add_indent(script_data)
                custom_script_data = script_data
                lab_script_data = script_data
                if code_type == 'scratch' or code_type == '':
                    logger.info('SCRIPT_CTRL: cur code type is scratch')
                    lab_script_data = self.parse_descriptions(script_data)
                else:
                    if code_type == 'python':
                        logger.info('SCRIPT_CTRL: cur code type is python')
                lab_script_data = self.framework_data.replace('SCRATCH_PYTHON_CODE', lab_script_data)
                custom_script_data = self.custome_skill_framework_data.replace('SCRATCH_PYTHON_CODE', custom_script_data)
                try:
                    for file in self.script_file_list:
                        if not os.path.isdir(os.path.join(self.script_dirc, file)):
                            if file.find(file_guid) != -1:
                                if file.find(self.audio_opus_suffix) == -1:
                                    if file.find(self.audio_wav_suffix) == -1:
                                        os.remove(os.path.join(self.script_dirc, file))
                                        logger.info('SCRIPT_CTRL: remove file: ' + file)

                except:
                    logger.fatal(traceback.format_exc())
                else:
                    python_file_name = self.file_prefix + time.strftime('%Y%m%d%H%M%S_') + file_guid
                    lab_script_name = python_file_name + self.lab_prefix + self.python_suffix
                    save_lab_script_name = os.path.join(self.script_dirc, lab_script_name)
                    self.write_script_string(save_lab_script_name, lab_script_data)
                    custom_script_name = python_file_name + self.custom_prefix + self.python_suffix
                    save_custom_script_name = os.path.join(self.script_dirc, custom_script_name)
                    self.write_script_string(save_custom_script_name, custom_script_data)
                    logger.info('SCRIPT_CTRL: create python file: %s(_custom/_lab).py' % python_file_name)
                    dsp_file_name = self.file_prefix + time.strftime('%Y%m%d%H%M%S_') + file_guid + self.dsp_suffix
                    save_dsp_file_name = os.path.join(self.script_dirc, dsp_file_name)
                    logger.info('SCRIPT_CTRL: create dsp file: ' + dsp_file_name)
                    self.write_script_string(save_dsp_file_name, dsp_buffer)
                    if not self.has_scripts_running:
                        self.set_block_to_IDLE()
                        while 'audio-list' in dsp_buffer:
                            duss_result, audio_list = self.get_audio_data(dsp_buffer)
                            for audio in audio_list:
                                if audio['modify'] == 'true':
                                    if audio['type'] == 'opus':
                                        audio_file_name = self.file_prefix + str(hex(audio['id'])) + '_' + file_guid + self.audio_opus_suffix
                                        sound_type = 0
                                    else:
                                        if audio['type'] == 'wav':
                                            audio_file_name = self.file_prefix + str(hex(audio['id'])) + '_' + file_guid + self.audio_wav_suffix
                                            sound_type = 1
                                    save_audio_file_name = os.path.join(self.script_dirc, audio_file_name)
                                    logger.info('SCRIPT_CTRL: create audio file: ' + audio_file_name)
                                    if os.path.exists(save_audio_file_name):
                                        logger.info('SCRIPT_CTRL: delete audio file: ' + audio_file_name)
                                        os.remove(save_audio_file_name)
                                        self.msg_buff.init()
                                        self.msg_buff.append('action', 'uint8', 0)
                                        self.msg_buff.append('type', 'uint8', sound_type)
                                        self.msg_buff.append('soundid', 'uint32', audio['id'])
                                        self.msg_buff.append('guid', 'string', file_guid)
                                        self.msg_buff.receiver = rm_define.hdvt_uav_id
                                        self.msg_buff.cmd_id = duml_cmdset.DUSS_MB_CMD_RM_CUSTOM_SOUND_CONVERT
                                        self.event_client.send_sync(self.msg_buff)
                                    else:
                                        b64_audio_data = base64.b64decode(audio['data'])
                                        fd = open(save_audio_file_name, 'wb')
                                        fd.write(b64_audio_data)
                                        fd.close()

                        self.query()
                        return duss_result

            def delete_file(self, guid, sign):
                self.query()
                target_file = self.find_script_file_in_list(self.script_file_list, guid, self.dsp_suffix)
                if target_file == None:
                    return rm_define.DUSS_ERR_FAILURE
                dsp_str = self.read_script_string(os.path.join(self.script_dirc, target_file))
                dsp_parser = dji_scratch_project_parser.DSPXMLParser()
                dsp_parser.parseDSPString(dsp_str)
                if dsp_parser.dsp_dict['sign'] == sign:
                    os.remove(os.path.join(self.script_dirc, target_file))
                    os.remove(os.path.join(self.script_dirc, target_file.replace(self.dsp_suffix, self.lab_prefix + self.python_suffix)))
                    os.remove(os.path.join(self.script_dirc, target_file.replace(self.dsp_suffix, self.custom_prefix + self.python_suffix)))
                    return rm_define.DUSS_SUCCESS
                return rm_define.DUSS_ERR_FAILURE

            def delete_all_file(self):
                duss_result = rm_define.DUSS_SUCCESS
                try:
                    shutil.rmtree(self.script_dirc)
                    os.mkdir(self.script_dirc)
                except:
                    logger.warn('SCRIPT_CTRL: delete all file failure')
                    duss_result = rm_define.DUSS_ERR_FAILURE
                else:
                    self.query()
                    return duss_result

            def load_custome_skill(self, custome_id, guid, sign):
                if self.has_scripts_running:
                    return rm_define.DUSS_ERR_FAILURE
                self.query()
                target_file = self.find_script_file_in_list(self.script_file_list, guid, self.dsp_suffix)
                if target_file == None:
                    return rm_define.DUSS_ERR_FAILURE
                dsp_str = self.read_script_string(os.path.join(self.script_dirc, target_file))
                dsp_parser = dji_scratch_project_parser.DSPXMLParser()
                dsp_parser.parseDSPString(dsp_str)
                if dsp_parser.dsp_dict['sign'] != sign:
                    return rm_define.DUSS_ERR_FAILURE
                self.custom_skill_config_dict[custome_id] = guid
                self.save_custome_skill_dict(self.custom_skill_config_dict)
                return rm_define.DUSS_SUCCESS

            def unload_custome_skill(self, custome_id):
                if self.has_scripts_running:
                    return rm_define.DUSS_ERR_FAILURE
                if custome_id in self.custom_skill_config_dict.keys():
                    self.custom_skill_config_dict.pop(custome_id)
                    self.save_custome_skill_dict(self.custom_skill_config_dict)
                return rm_define.DUSS_SUCCESS

            def query_custome_skill(self, custome_id):
                if custome_id not in self.custom_skill_config_dict.keys():
                    return (rm_define.DUSS_ERR_FAILURE, None, None)
                query_guid = self.custom_skill_config_dict[custome_id]
                self.query()
                target_file = self.find_script_file_in_list(self.script_file_list, query_guid, self.dsp_suffix)
                if target_file == None:
                    return (rm_define.DUSS_ERR_FAILURE, None, None)
                dsp_str = self.read_script_string(os.path.join(self.script_dirc, target_file))
                dsp_parser = dji_scratch_project_parser.DSPXMLParser()
                dsp_parser.parseDSPString(dsp_str)
                query_sign = dsp_parser.dsp_dict['sign']
                logger.info('SCRIPT_CTRL: query success, guid:%s, sign:%s' % (query_guid, query_sign))
                return (
                 rm_define.DUSS_SUCCESS, query_guid, query_sign)

            def save_custome_skill_dict(self, t_dict, file_name='custom_skill_config.json'):
                file_name = os.path.join(self.script_dirc, file_name)
                config_file = open(file_name, 'w')
                json.dump(t_dict, config_file, ensure_ascii=True)

            def read_custome_skill_dict(self, file_name='custom_skill_config.json'):
                t_dict = {}
                file_name = os.path.join(self.script_dirc, file_name)
                try:
                    config_file = open(file_name, 'r')
                    json_str = config_file.read()
                    t_dict = json.loads(json_str)
                except Exception as e:
                    try:
                        self.save_custome_skill_dict(t_dict)
                        logger.error('SCRIPT_CTRL: error! message: ')
                        logger.error('TRACEBACK:\n' + traceback.format_exc())
                    finally:
                        e = None
                        del e

                else:
                    return t_dict

            def update_scratch_block_state(self, block_dict):
                self._ScriptCtrl__scratch_block_state = block_dict['name']
                if block_dict['name'] != 'IDLE':
                    if block_dict['name'] != 'SCRIPT_START':
                        if block_dict['name'] != 'CUSTOME_SKILL':
                            if block_dict['name'] != 'OFF_CONTROL':
                                self._ScriptCtrl__scratch_block_state = 'SCRIPT_RUN'

            def scatch_script_block_push_timer(self, *arg, **kw):
                state_switch_flag = 'NO_CHANGE'
                have_block_description = False
                block_dict = {}
                self.block_description_mutex.acquire()
                if len(self._ScriptCtrl__block_description_dict_list) > 0:
                    have_block_description = True
                    block_dict = self._ScriptCtrl__block_description_dict_list.pop(0)
                self.block_description_mutex.release()
                if have_block_description:
                    if self._ScriptCtrl__scratch_block_dict['id'] != block_dict['id'] or 'data_' in block_dict['name']:
                        state_switch_flag = 'CHANGED'
                        if 'running_state' in self._ScriptCtrl__scratch_block_dict.keys():
                            if 'running_state' in block_dict.keys():
                                self._ScriptCtrl__scratch_block_dict['running_state'] = block_dict['running_state']
                                block_dict['running_state'] = rm_define.BLOCK_RUN_SUCCESS
                                self.state_pusher_send_msgbuf(state_switch_flag)
                        self._ScriptCtrl__scratch_block_dict = block_dict
                        self.update_scratch_block_state(block_dict)
                        logger.debug('BLOCK: state change to: ' + self._ScriptCtrl__scratch_block_state + ', block ID: ' + block_dict['id'])
                self.state_pusher_send_msgbuf(state_switch_flag)

            def set_block_to_CUSTOME_SKILL(self):
                self.push_block_description_info_to_timer(id='ABCDEFGHIJ1234567899', name='CUSTOME_SKILL', type='INFO_PUSH')

            def set_block_to_OFF_CONTROL(self):
                self.push_block_description_info_to_timer(id='ABCDEFGHIJ1234567898', name='OFF_CONTROL', type='INFO_PUSH')

            def set_block_to_IDLE(self):
                logger.info('----set_block_to_IDLE start----')
                self.push_block_description_info_to_timer(id='ABCDEFGHIJ1234567897', name='IDLE', type='INFO_PUSH')
                logger.info('----set_block_to_IDLE end----')

            def set_block_to_START(self):
                self.push_block_description_info_to_timer(id='ABCDEFGHIJ1234567896', name='SCRIPT_START', type='INFO_PUSH')

            def set_block_to_RUN(self):
                self.push_block_description_info_to_timer(id='ABCDEFGHIJ1234567895', name='SCRIPT_RUN', type='INFO_PUSH')

            def get_sorted_variable_name_list(self):
                self.sorted_variable_name_list = []
                if isinstance(_globals_exec, dict):
                    for k, v in _globals_exec.items():
                        if isinstance(k, str):
                            if not k.startswith('variable_'):
                                if k.startswith('list_'):
                                    pass
                                self.sorted_variable_name_list.append(k)
                            else:
                                self.sorted_variable_name_list = sorted(self.sorted_variable_name_list)

                logger.info('BLOCK: sorted variable is %s' % str(self.sorted_variable_name_list))

            def get_target_variable_index_and_value(self, var_name):
                if self.sorted_variable_name_list == None:
                    return (None, None)
                if var_name != '':
                    if var_name in _globals_exec.keys():
                        if var_name in self.sorted_variable_name_list:
                            index = self.sorted_variable_name_list.index(var_name)
                            value = _globals_exec[var_name]
                            return (
                             index, value)
                return (None, None)

            def get_block_running_state(self):
                running_state = None
                if isinstance(_globals_exec, dict):
                    if 'event' in _globals_exec.keys():
                        running_state = _globals_exec['event'].script_state.get_block_running_state()
                return running_state

            def get_block_running_percent(self):
                percent = 100
                if isinstance(_globals_exec, dict):
                    if 'event' in _globals_exec.keys():
                        percent = _globals_exec['event'].script_state.get_block_running_percent()
                return percent

            def push_block_description_info_to_timer(self, **src_block_dict):
                block_running_state = self.get_block_running_state()
                block_dict = src_block_dict
                if 'id' not in block_dict.keys() or 'name' not in block_dict.keys():
                    return
                if 'name' in block_dict.keys():
                    if block_dict['name'] == 'robot_on_start':
                        self.get_sorted_variable_name_list()
                push_variable = ''
                if 'curvar' in block_dict.keys():
                    if self._ScriptCtrl__scratch_variable_push_flag:
                        self._ScriptCtrl__scratch_variable_push_flag = False
                        if self._ScriptCtrl__scratch_variable_push_name not in self.variable_name_wait_push_list:
                            self.variable_name_wait_push_list.append(self._ScriptCtrl__scratch_variable_push_name)
                    if block_dict['curvar'] != '':
                        self._ScriptCtrl__scratch_variable_push_flag = True
                        self._ScriptCtrl__scratch_variable_push_name = block_dict['curvar']
                if block_running_state != None:
                    block_dict['running_state'] = block_running_state
                self.block_description_mutex.acquire()
                self._ScriptCtrl__block_description_dict_list.append(block_dict)
                self.block_description_mutex.release()

            def state_pusher_send_msgbuf(self, push_flag):
                self.time_counter = self.time_counter + 1
                if push_flag == 'CHANGED' or self.time_counter == 10:
                    self.time_counter = 0
                    block_state_table = { 'IDLE': 0, 'SCRIPT_START': 1, 'SCRIPT_RUN': 2, 'CUSTOME_SKILL': 3, 'OFF_CONTROL': 4, 'ERROR': 5}
                    block_type_table = { 'SET_PROPERTY': 0, 'CONTINUE_CONTROL': 1, 'TASK': 2, 'RESPONSE_NOW': 3, 'INFO_PUSH': 4, 'EVENT': 5, 'CONDITION_WAIT': 6}
                    self.msg_buff.init()
                    percent = self.get_block_running_percent()
                    block_running_state = rm_define.BLOCK_RUN_SUCCESS
                    if 'running_state' in self._ScriptCtrl__scratch_block_dict.keys():
                        block_running_state = self._ScriptCtrl__scratch_block_dict['running_state']
                    self.msg_buff.append('script_state', 'uint8', block_state_table[self._ScriptCtrl__scratch_block_state])
                    self.msg_buff.append('script_id', 'bytes', tools.string_to_byte(self.run_script_id))
                    self.msg_buff.append('block_id_len', 'uint8', 20)
                    block_id_bytes = tools.string_to_byte(self._ScriptCtrl__scratch_block_dict['id'])
                    if len(block_id_bytes) != 20:
                        block_id_bytes = tools.string_to_byte('ABCDEFGHIJ4567890123')
                        logger.info('block_id length error')
                    self.msg_buff.append('block_id', 'bytes', block_id_bytes)
                    self.msg_buff.append('exec_result', 'uint8', block_running_state)
                    self.msg_buff.append('block_type', 'uint8', 0)
                    self.msg_buff.append('exec_precent', 'uint8', percent)
                    if len(self.variable_name_wait_push_list) != 0:
                        var_name = self.variable_name_wait_push_list.pop(0)
                        self.msg_buff.append('variable_len', 'uint16', 1)
                        index, value = self.get_target_variable_index_and_value(var_name)
                        if isinstance(value, rm_builtins.RmList) or isinstance(value, list):
                            offset = 0
                            if isinstance(value, rm_builtins.RmList):
                                offset = 1
                            if len(value) == 0:
                                idx = 32768 | index << 7
                                self.msg_buff.append('variable_len', 'uint16', 1)
                                self.msg_buff.append('var' + str(idx), 'uint16', idx)
                                self.msg_buff.append('var_value' + str(idx), 'float', 0)
                            else:
                                self.msg_buff.append('variable_len', 'uint16', len(value))
                                for index_t in range(len(value) + offset)[offset:]:
                                    if index_t >= 128:
                                        self.msg_buff.append('variable_len', 'uint16', 128)
                                        break
                                    else:
                                        idx = 16384 | index << 7 | index_t
                                        self.msg_buff.append('var' + str(idx), 'uint16', idx)
                                        self.msg_buff.append('var_value' + str(idx), 'float', value[index_t])

                        else:
                            if index != None:
                                index &= 127
                                self.msg_buff.append('var' + str(index), 'uint16', index)
                                self.msg_buff.append('var_value' + str(index), 'float', float(value))
                    else:
                        self.msg_buff.append('variable_len', 'uint16', 0)
                    self.msg_buff.cmd_id = duml_cmdset.DUSS_MB_CMD_RM_SCRIPT_BLOCK_STATUS_PUSH
                    self.msg_buff.receiver = rm_define.hdvt_uav_id
                    duss_result = self.event_client.send_msg(self.msg_buff)
                    if self._ScriptCtrl__scratch_block_state == 'IDLE':
                        self.report_traceback_dict_mutex.acquire()
                        if self.report_traceback_dict['traceback_valid'] != 0 and self.error_report_time < 3:
                            self.error_report_time = self.error_report_time + 1
                            logger.info('Report error %d th', self.error_report_time)
                            self.msg_buff.init()
                            self.msg_buff.append('script_state', 'uint8', block_state_table['ERROR'])
                            self.msg_buff.append('script_id', 'string', self.report_traceback_dict['script_id'])
                            self.msg_buff.append('traceback_valid', 'uint8', self.report_traceback_dict['traceback_valid'])
                            self.msg_buff.append('block_id_len', 'uint8', 20)
                            self.msg_buff.append('block_id', 'string', self.report_traceback_dict['block_id'])
                            self.msg_buff.append('err_code', 'uint8', tools.get_fatal_code(self.report_traceback_dict['traceback_msg']))
                            self.msg_buff.append('reserved', 'string', '\x00\x00')
                            self.msg_buff.append('traceback_line', 'uint32', self.report_traceback_dict['traceback_line'])
                            self.msg_buff.append('traceback_len', 'uint16', self.report_traceback_dict['traceback_len'])
                            self.msg_buff.append('traceback_msg', 'string', self.report_traceback_dict['traceback_msg'])
                            self.report_traceback_dict_mutex.release()
                        else:
                            if self.error_report_time > 0:
                                self.report_traceback_dict_mutex.release()
                                self.clear_report_traceback_msg()
                                self.error_report_time = 0
                            else:
                                self.report_traceback_dict_mutex.release()
                    self.msg_buff.receiver = rm_define.mobile_id
                    duss_result = self.event_client.send_msg(self.msg_buff)

            def reset_block_state_pusher(self):
                global _globals_exec
                logger.info('----reset_block_state_pusher start----')
                self.block_description_mutex.acquire()
                self._ScriptCtrl__block_description_dict_list = []
                self.block_description_mutex.release()
                self.sorted_variable_name_list = None
                self.set_block_to_IDLE()
                _globals_exec = None
                logger.info('BLOCK: reset, state change to IDLE')

            def update_report_traceback_msg(self, script_id, block_id, traceback_msg):
                self.report_traceback_dict_mutex.acquire()
                self.report_traceback_dict['script_id'] = script_id
                self.report_traceback_dict['block_id'] = block_id
                line = 0
                if len(traceback_msg) == 0:
                    self.report_traceback_dict['traceback_valid'] = 0
                else:
                    traceback_msg = traceback_msg.splitlines()
                    error_type = traceback_msg[-1]
                    traceback_msg_str = ''
                    break_flag = False
                if 'Exception:' in error_type or not 'NameError:' in error_type:
                    for msg in traceback_msg:
                        if 'File "<string>"' in msg:
                            traceback_msg_str = msg + '\n'
                        else:
                            if traceback_msg_str:
                                break

                else:
                    for msg in traceback_msg:
                        if break_flag:
                            traceback_msg_str += msg + '\n'
                            break
                            while 'File "<string>"' in msg:
                                traceback_msg_str = msg + '\n'

                            if traceback_msg_str:
                                traceback_msg_str += msg + '\n'
                                break_flag = True
                                continue
                    else:
                        traceback_msg_str = traceback_msg[0] + '\n' + traceback_msg_str + traceback_msg[-1] + '\n'
                        traceback_msg = traceback_msg_str
                        line_pos = traceback_msg.rfind('line')
                        line_str = traceback_msg[line_pos + len('line '):]
                        try:
                            line = int(line_str[0:line_str.find('\n')])
                        except:
                            try:
                                line = int(line_str[0:line_str.find(',')])
                            except:
                                line = 0

                        else:
                            if line >= self.scratch_python_code_line_offset:
                                new_line = line - self.scratch_python_code_line_offset
                            else:
                                new_line = 0
                            traceback_msg = traceback_msg.replace('line ' + str(line), 'line ' + str(new_line))
                            traceback_msg = traceback_msg.replace('<string>', '<CurFile>')
                            traceback_msg = traceback_msg.replace('<module>', '<CurModule>')
                            line = new_line
                            self.report_traceback_dict['traceback_valid'] = 1
                            self.report_traceback_dict['traceback_line'] = line
                            self.report_traceback_dict['traceback_len'] = len(traceback_msg)
                            self.report_traceback_dict['traceback_msg'] = traceback_msg
                        self.report_traceback_dict_mutex.release()

            def clear_report_traceback_msg(self):
                self.report_traceback_dict_mutex.acquire()
                self.report_traceback_dict['script_id'] = ''
                self.report_traceback_dict['block_id'] = ''
                self.report_traceback_dict['traceback_valid'] = 0
                self.report_traceback_dict['traceback_line'] = 0
                self.report_traceback_dict['traceback_len'] = 0
                self.report_traceback_dict['traceback_msg'] = ''
                self.report_traceback_dict_mutex.release()

            def get_report_traceback_msg(self):
                return dict(self.report_traceback_dict)


        class ScriptProcessCtrl(object):

            def __init__(self, script_ctrl, local_sub_service):
                self.script_ctrl = script_ctrl
                self.local_sub_service = local_sub_service
                self.ftp_rcv_status = rm_define.ftp_idle
                self.ftp_dsp_path = os.path.join(rm_path.get_data_path(), 'data/ftp/python')
                self.ftp_file = 'python_raw.dsp'
                self.ftp_file_size = 0
                self.retry = 0
                self.script_raw_data = {}
                self.cmd_dict = {
                  1: 'QUERY',  2: 'RUN',  5: 'EXIT',  6: 'DELETE',  7: 'DEL_ALL',  8: 'CUSTOME_LOAD',
                  9: 'CUSTOME_UNLOAD',  10: 'CUSTOME_QUERY',  11: 'CUSTOME_RUN',  12: 'CUSTOME_EXIT',
                  13: 'QUERY_FILE'}
                if not os.path.exists(self.ftp_dsp_path):
                    logger.warn('%s is not exist! create first' % self.ftp_dsp_path)
                    os.makedirs(self.ftp_dsp_path)

            def get_local_ip--- This code section failed: ---

 L.1177         0  SETUP_FINALLY        54  'to 54'

 L.1178         2  LOAD_GLOBAL              socket
                4  LOAD_METHOD              socket
                6  LOAD_GLOBAL              socket
                8  LOAD_ATTR                AF_INET
               10  LOAD_GLOBAL              socket
               12  LOAD_ATTR                SOCK_DGRAM
               14  CALL_METHOD_2         2  ''
               16  STORE_FAST               'csock'

 L.1179        18  LOAD_FAST                'csock'
               20  LOAD_METHOD              connect
               22  LOAD_CONST               ('192.168.2.1', 80)
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          

 L.1180        28  LOAD_FAST                'csock'
               30  LOAD_METHOD              getsockname
               32  CALL_METHOD_0         0  ''
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'addr'
               38  STORE_FAST               'port'

 L.1181        40  LOAD_FAST                'csock'
               42  LOAD_METHOD              close
               44  CALL_METHOD_0         0  ''
               46  POP_TOP          

 L.1182        48  LOAD_FAST                'addr'
               50  POP_BLOCK        
               52  RETURN_VALUE     
             54_0  COME_FROM_FINALLY     0  '0'

 L.1183        54  DUP_TOP          
               56  LOAD_GLOBAL              socket
               58  LOAD_ATTR                error
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    76  'to 76'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L.1184        70  POP_EXCEPT       
               72  LOAD_STR                 '192.168.2.1'
               74  RETURN_VALUE     
             76_0  COME_FROM            62  '62'
               76  END_FINALLY      

Parse error at or near `LOAD_STR' instruction at offset 72

            def request_recv_script_file(self, event_client, msg):
                logger.info('REQUEST_CTRL-----: receive cmd 0xA1')
                buff = msg['data']
                if len(buff) < 4:
                    logger.error('REQUEST_CTRL: data length is less than 4!')
                    event_client.resp_retcode(msg, duml_cmdset.DUSS_MB_RET_DOWNLOAD_FAILUE)
                    return
                enc_type = buff[0]
                seq_num = buff[1]
                length = buff[3] << 8 | buff[2]
                if length != len(buff) - 4:
                    logger.error('REQUEST_CTRL: data length check failure!')
                    event_client.resp_retcode(msg, duml_cmdset.DUSS_MB_RET_DOWNLOAD_FAILUE)
                    return
                if enc_type != 1:
                    data = buff[4:length + 4]
                    self.script_raw_data[seq_num] = data
                    event_client.resp_retcode(msg, duml_cmdset.DUSS_MB_RET_OK)
                else:
                    if enc_type == 1:
                        if length != 4:
                            logger.error('REQUEST_CTRL: FTP file size length check failure!')
                            event_client.resp_retcode(msg, duml_cmdset.DUSS_MB_RET_DOWNLOAD_FAILUE)
                            return
                        self.ftp_file_size = buff[7] << 24 | buff[6] << 16 | buff[5] << 8 | buff[4]
                        logger.info('REQUEST_CTRL: FTP file size is %d' % self.ftp_file_size)
                        self.ftp_rcv_status = rm_define.ftp_rcv_data
                        local_ip = self.get_local_ip()
                        logger.info('REQUEST_CTRL: ip address is %s' % local_ip)
                        ip_bytes = bytes(map(int, local_ip.split('.')))
                        event_msg = duss_event_msg.unpack2EventMsg(msg)
                        event_msg.clear()
                        event_msg.append('ret_code', 'uint8', duml_cmdset.DUSS_MB_RET_OK)
                        event_msg.append('ip_addr', 'uint32', ip_bytes[0] << 24 | ip_bytes[1] << 16 | ip_bytes[2] << 8 | ip_bytes[3])
                        event_msg.append('port', 'uint16', rm_path.get_ftp_server_port())
                        event_client.resp_event_msg(event_msg)

            def request_create_script_file(self, event_client, msg):
                logger.info('REQUEST_CTRL: receive cmd 0xA2')
                buff = msg['data']
                if len(buff) < 2:
                    logger.error('REQUEST_CTRL: data length is less than 2!')
                    event_client.resp_retcode(msg, duml_cmdset.DUSS_MB_RET_DOWNLOAD_FAILUE)
                    return
                resend_seq_list = []
                file_data = []
                enc_type = buff[0]
                seq_num = buff[1]
                if enc_type == 0:
                    if self.script_raw_data == {}:
                        logger.info('REQUEST_CTRL:raw_data is {}, not need resend')
                        return
                    for seq in range(seq_num + 1):
                        if seq not in self.script_raw_data.keys():
                            resend_seq_list.append(seq)
                    else:
                        if resend_seq_list:
                            logger.info('REQUEST_CTRL: resend package sequences: ' + str(resend_seq_list))
                            logger.info('REQUEST_CTRL: sequences max: ' + str(seq_num))
                            if self.retry >= 5:
                                logger.error('REQUEST_CTRL: retry achieve the max, send failure code to APP')
                                self.reset_states()
                                event_client.resp_retcode(msg, duml_cmdset.DUSS_MB_RET_DOWNLOAD_FAILUE)
                            else:
                                self.retry = self.retry + 1
                                event_msg = duss_event_msg.unpack2EventMsg(msg)
                                event_msg.clear()
                                event_msg.append('ret_code', 'uint8', duml_cmdset.DUSS_MB_RET_RESEND_REQUEST)
                                event_msg.append('resend_len', 'uint8', len(resend_seq_list))
                                event_msg.append('data', 'bytes', resend_seq_list)
                                event_client.resp_event_msg(event_msg)
                            return
                        logger.info('REQUEST_CTRL: sequence check success!')
                        for seq in range(seq_num + 1):
                            file_data.extend(self.script_raw_data[seq])

                else:
                    if enc_type == 1:
                        if self.ftp_rcv_status != rm_define.ftp_rcv_data:
                            logger.error('REQUEST_CTRL: ftp state check failure')
                            event_client.resp_retcode(msg, duml_cmdset.DUSS_MB_RET_NOT_IN_TRANSFER)
                            if os.path.exists(os.path.join(self.ftp_dsp_path, self.ftp_file)):
                                os.remove(os.path.join(self.ftp_dsp_path, self.ftp_file))
                            return
                        self.ftp_rcv_status = rm_define.ftp_idle
                        if not os.path.exists(os.path.join(self.ftp_dsp_path, self.ftp_file)):
                            logger.error('REQUEST_CTRL: FTP file not exsit')
                            event_client.resp_retcode(msg, duml_cmdset.DUSS_MB_RET_NO_EXIST_DSP)
                            return
                        with open(os.path.join(self.ftp_dsp_path, self.ftp_file), 'rb') as file_obj:
                            file_data.extend(file_obj.read())
                MD5 = buff[2:18]
                if enc_type == 0:
                    if not tools.md5_check(file_data, MD5):
                        logger.error('REQUEST_CTRL: MD5 check failure')
                        if self.retry >= 5:
                            logger.error('REQUEST_CTRL: retry achieve the max, send failure code to APP')
                            self.reset_states()
                            event_client.resp_retcode(msg, duml_cmdset.DUSS_MB_RET_DOWNLOAD_FAILUE)
                        else:
                            self.retry = self.retry + 1
                            event_client.resp_retcode(msg, duml_cmdset.DUSS_MB_RET_MD5_CHECK_FAILUE)
                        return
                    logger.info('REQUEST_CTRL: MD5 check success!')
                else:
                    if enc_type == 1:
                        file_size = os.path.getsize(os.path.join(self.ftp_dsp_path, self.ftp_file))
                        if self.ftp_file_size != file_size:
                            logger.error('REQUEST_CTRL: check FTP file size failure')
                            event_client.resp_retcode(msg, duml_cmdset.DUSS_MB_RET_SIZE_NOT_MATCH)
                            if os.path.exists(os.path.join(self.ftp_dsp_path, self.ftp_file)):
                                os.remove(os.path.join(self.ftp_dsp_path, self.ftp_file))
                            return
                        md5_str = ''
                        for value in MD5:
                            md5_str += hex(value)[2:].zfill(2)
                        else:
                            fp = open(os.path.join(self.ftp_dsp_path, self.ftp_file), 'rb')
                            contents = fp.read()
                            fp.close()
                            if md5_str == hashlib.md5(contents).hexdigest():
                                logger.info('REQUEST_CTRL: MD5 file check success!')
                                if os.path.exists(os.path.join(self.ftp_dsp_path, self.ftp_file)):
                                    os.remove(os.path.join(self.ftp_dsp_path, self.ftp_file))
                            else:
                                logger.info('REQUEST_CTRL: MD5 file check failure!')
                                event_client.resp_retcode(msg, duml_cmdset.DUSS_MB_RET_MD5_CHECK_FAILUE)
                                if os.path.exists(os.path.join(self.ftp_dsp_path, self.ftp_file)):
                                    os.remove(os.path.join(self.ftp_dsp_path, self.ftp_file))
                                return

                duss_result = self.script_ctrl.create_file(file_data, event_client)
                self.reset_states()
                logger.info('REQUEST_CTRL: file create success!')
                event_client.resp_retcode(msg, duss_result)

            def request_ctrl_script_file(self, event_client, msg):
                logger.info('REQUEST_CTRL: receive cmd 0xA3')
                buff = msg['data']
                if len(buff) < 1:
                    logger.error('REQUEST_CTRL: data length is less than 1!')
                    event_client.resp_retcode(msg, rm_define.DUSS_ERR_FAILURE)
                    return
                if buff[0] & 15 not in self.cmd_dict.keys():
                    logger.info('REQUEST_CTRL: unsupported CMD: ' + str(buff[0] & 15))
                    event_client.resp_retcode(msg, duml_cmdset.DUSS_MB_RET_INVALID_CMD)
                    return
                cmd = self.cmd_dict[buff[0] & 15]
                custome_id = str((buff[0] & 240) >> 4)
                if cmd != 'DEL_ALL':
                    if cmd != 'CUSTOME_QUERY':
                        if cmd != 'CUSTOME_RUN':
                            if cmd != 'CUSTOME_EXIT':
                                if cmd != 'CUSTOME_UNLOAD':
                                    if cmd != 'QUERY_FILE':
                                        if len(buff) < 49:
                                            logger.error('REQUEST_CTRL: cmd = %s, data length %d is less than 49!' % s(cmd, len(buff)))
                                            event_client.resp_retcode(msg, rm_define.DUSS_ERR_FAILURE)
                                            return
                                        guid_byte = tools.pack_to_byte(buff[1:33])
                                        sign_byte = tools.pack_to_byte(buff[33:49])
                                        guid = guid_byte.decode('utf-8')
                                        sign = sign_byte.decode('utf-8')
                if cmd == 'QUERY':
                    logger.info('REQUEST_CTRL: query script file: ' + str(guid) + ' sign: ' + str(sign))
                    duss_result = self.script_ctrl.check_dsp_file(guid, sign)
                else:
                    if cmd == 'RUN':
                        logger.info('REQUEST_CTRL: start running script file: ' + str(guid) + ' sign: ' + str(sign))
                        duss_result = self.script_ctrl.exit_low_power_mode(event_client, msg)
                        duss_result = self.script_ctrl.transcode_audio_file(guid, None, event_client, msg)
                        if duss_result == rm_define.DUSS_SUCCESS:
                            duss_result = self.script_ctrl.start_running(guid, None)
                    else:
                        if cmd == 'EXIT':
                            logger.info('REQUEST_CTRL: exiting the running script file: ' + str(guid) + ' sign: ' + str(sign))
                            duss_result = self.script_ctrl.stop_running(guid, None)
                        else:
                            if cmd == 'DELETE':
                                logger.info('REQUEST_CTRL: request delete script file: ' + str(guid) + ' sign: ' + str(sign))
                                duss_result = self.script_ctrl.delete_file(guid, sign)
                            else:
                                if cmd == 'DEL_ALL':
                                    logger.info('REQUEST_CTRL: request delete ALL script file')
                                    duss_result = self.script_ctrl.delete_all_file()
                                else:
                                    if cmd == 'CUSTOME_LOAD':
                                        logger.info('REQUEST_CTRL: load custome skill script, index: %s, guid: %s' % (custome_id, guid))
                                        duss_result = self.script_ctrl.load_custome_skill(custome_id, guid, sign)
                                        logger.info('REQUEST_CTRL: current custome skill:')
                                        logger.info(self.script_ctrl.custom_skill_config_dict)
                                    else:
                                        if cmd == 'CUSTOME_UNLOAD':
                                            logger.info('REQUEST_CTRL: unload custome skill script, index: %s' % custome_id)
                                            duss_result = self.script_ctrl.unload_custome_skill(custome_id)
                                            logger.info('REQUEST_CTRL: current custome skill:')
                                            logger.info(self.script_ctrl.custom_skill_config_dict)
                                        else:
                                            if cmd == 'CUSTOME_QUERY':
                                                logger.info('REQUEST_CTRL: query custome script, index: ' + custome_id)
                                                duss_result, guid, sign = self.script_ctrl.query_custome_skill(custome_id)
                                                if duss_result == rm_define.DUSS_SUCCESS:
                                                    event_msg = duss_event_msg.unpack2EventMsg(msg)
                                                    event_msg.clear()
                                                    event_msg.append('ret_code', 'uint8', duss_result)
                                                    event_msg.append('guid', 'bytes', tools.string_to_byte(guid))
                                                    event_msg.append('sign', 'bytes', tools.string_to_byte(sign))
                                                    event_client.resp_event_msg(event_msg)
                                                    return
                                            else:
                                                if cmd == 'CUSTOME_RUN':
                                                    logger.info('REQUEST_CTRL: run custome script, index: ' + custome_id)
                                                    duss_result = self.script_ctrl.transcode_audio_file(None, custome_id, event_client, msg)
                                                    if duss_result == rm_define.DUSS_SUCCESS:
                                                        duss_result = self.script_ctrl.start_running(None, custome_id)
                                                else:
                                                    if cmd == 'CUSTOME_EXIT':
                                                        logger.info('REQUEST_CTRL: exit custome script, index: ' + custome_id)
                                                        duss_result = self.script_ctrl.stop_running(None, custome_id)
                                                    else:
                                                        if cmd == 'QUERY_FILE':
                                                            guid_byte = tools.pack_to_byte(buff[1:33])
                                                            guid = guid_byte.decode('utf-8')
                                                            logger.info('REQUEST_CTRL: query file, index: ' + str(guid))
                                                            file_type = buff[33]
                                                            file_count = buff[34]
                                                            file_dict = {}
                                                            for i in range(0, file_count):
                                                                file_dict[str(buff[35 + i * 5])] = tools.byte2hex(buff[36 + i * 5:40 + i * 5])
                                                            else:
                                                                if file_type == rm_define.custom_audio_file:
                                                                    duss_result, match_list = (self.script_ctrl.check_audio_file)(guid, **file_dict)
                                                                    event_msg = duss_event_msg.unpack2EventMsg(msg)
                                                                    event_msg.clear()
                                                                    event_msg.append('ret_code', 'uint8', 0)
                                                                    event_msg.append('count', 'uint8', file_count)
                                                                    for i in range(len(match_list)):
                                                                        event_msg.append('match[%d]' % i, 'uint8', match_list[i])
                                                                    else:
                                                                        event_client.resp_event_msg(event_msg)
                                                                        return

                                                                duss_result = duml_cmdset.DUSS_MB_RET_OK

                                                        else:
                                                            logger.info('REQUEST_CTRL: unsupported CMD')
                                                            duss_result = duml_cmdset.DUSS_MB_RET_INVALID_CMD
                event_client.resp_retcode(msg, duss_result)

            def query_custom_skill_config(self, event_client, msg):
                logger.info('REQUEST_CTRL: receive cmd 0xA8')
                custom_skill_info_dict = {}
                for num, guid in self.script_ctrl.custom_skill_config_dict.items():
                    if int(num) < 10:
                        target_file = self.script_ctrl.find_script_file_in_list(self.script_ctrl.script_file_list, guid, self.script_ctrl.dsp_suffix)
                        if target_file:
                            dsp_str = self.script_ctrl.read_script_string(os.path.join(self.script_ctrl.script_dirc, target_file))
                            dsp_parser = dji_scratch_project_parser.DSPXMLParser()
                            dsp_parser.parseDSPString(dsp_str)
                            if 'title' in dsp_parser.dsp_dict.keys():
                                title = dsp_parser.dsp_dict['title'].encode('utf-8')[0:39]
                        if len(title) <= 39:
                            title += b'\n' * (40 - len(title))
                        else:
                            custom_skill_info_dict[int(num)] = {'guid':guid, 
                             'title':title}
                else:
                    logger.error(custom_skill_info_dict)
                    event_msg = duss_event_msg.unpack2EventMsg(msg)
                    event_msg.clear()
                    event_msg.append('ret_code', 'uint8', 0)
                    event_msg.append('num', 'uint8', len(custom_skill_info_dict))
                    for num, item in custom_skill_info_dict.items():
                        event_msg.append('number_%d' % num, 'uint8', num)
                        event_msg.append('guid_%d' % num, 'string', item['guid'])
                        event_msg.append('title_%d' % num, 'bytes', item['title'])
                    else:
                        event_client.resp_event_msg(event_msg)

            def request_auto_test--- This code section failed: ---

 L.1475         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              info
                4  LOAD_STR                 'REQUEST_CTRL: receive cmd 0xAF'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L.1476        10  LOAD_FAST                'msg'
               12  LOAD_STR                 'data'
               14  BINARY_SUBSCR    
               16  STORE_FAST               'buff'

 L.1477        18  LOAD_STR                 '/data/dji_scratch/tests/autotest'
               20  LOAD_GLOBAL              str
               22  LOAD_FAST                'buff'
               24  LOAD_CONST               0
               26  BINARY_SUBSCR    
               28  CALL_FUNCTION_1       1  ''
               30  BINARY_ADD       
               32  LOAD_STR                 '.py'
               34  BINARY_ADD       
               36  STORE_FAST               'test_case_name'

 L.1478        38  LOAD_FAST                'self'
               40  LOAD_ATTR                script_ctrl
               42  LOAD_METHOD              read_script_string
               44  LOAD_FAST                'test_case_name'
               46  CALL_METHOD_1         1  ''
               48  STORE_FAST               'script_str'

 L.1479        50  LOAD_GLOBAL              threading
               52  LOAD_ATTR                Thread
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                run_test_thread
               58  LOAD_FAST                'script_str'
               60  BUILD_TUPLE_1         1 
               62  LOAD_CONST               ('target', 'args')
               64  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               66  STORE_FAST               'script_thread_obj'

 L.1480        68  LOAD_FAST                'script_thread_obj'
               70  LOAD_METHOD              start
               72  CALL_METHOD_0         0  ''
               74  POP_TOP          

 L.1481        76  LOAD_GLOBAL              tools
               78  LOAD_METHOD              wait
               80  LOAD_CONST               1000
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          

 L.1483        86  LOAD_CONST               False
               88  STORE_FAST               'test_result'
             90_0  COME_FROM           138  '138'
             90_1  COME_FROM           110  '110'

 L.1485        90  LOAD_GLOBAL              tools
               92  LOAD_METHOD              wait
               94  LOAD_CONST               100
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          

 L.1487       100  LOAD_GLOBAL              _globals_exec
              102  LOAD_STR                 'test_client'
              104  BINARY_SUBSCR    
              106  LOAD_METHOD              get_test_finished
              108  CALL_METHOD_0         0  ''
              110  POP_JUMP_IF_FALSE_LOOP    90  'to 90'

 L.1488       112  LOAD_GLOBAL              _globals_exec
              114  LOAD_STR                 'test_client'
              116  BINARY_SUBSCR    
              118  LOAD_METHOD              get_test_result
              120  CALL_METHOD_0         0  ''
              122  STORE_FAST               'test_result'

 L.1489       124  LOAD_GLOBAL              _globals_exec
              126  LOAD_STR                 'test_client'
              128  BINARY_SUBSCR    
              130  LOAD_METHOD              set_test_exit
              132  CALL_METHOD_0         0  ''
              134  POP_TOP          

 L.1490       136  JUMP_FORWARD        140  'to 140'
              138  JUMP_LOOP            90  'to 90'
            140_0  COME_FROM           136  '136'

 L.1492       140  LOAD_GLOBAL              logger
              142  LOAD_METHOD              info
              144  LOAD_STR                 '%s, test result : %s'
              146  LOAD_FAST                'test_case_name'
              148  LOAD_GLOBAL              str
              150  LOAD_FAST                'test_result'
              152  CALL_FUNCTION_1       1  ''
              154  BUILD_TUPLE_2         2 
              156  BINARY_MODULO    
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          

 L.1494       162  LOAD_GLOBAL              duss_event_msg
              164  LOAD_METHOD              unpack2EventMsg
              166  LOAD_FAST                'msg'
              168  CALL_METHOD_1         1  ''
              170  STORE_FAST               'event_msg'

 L.1495       172  LOAD_FAST                'event_msg'
              174  LOAD_METHOD              clear
              176  CALL_METHOD_0         0  ''
              178  POP_TOP          

 L.1496       180  LOAD_FAST                'event_msg'
              182  LOAD_METHOD              append
              184  LOAD_STR                 'ret_code'
              186  LOAD_STR                 'uint8'
              188  LOAD_GLOBAL              duml_cmdset
              190  LOAD_ATTR                DUSS_MB_RET_OK
              192  CALL_METHOD_3         3  ''
              194  POP_TOP          

 L.1497       196  LOAD_FAST                'test_result'
              198  POP_JUMP_IF_FALSE   216  'to 216'

 L.1498       200  LOAD_FAST                'event_msg'
              202  LOAD_METHOD              append
              204  LOAD_STR                 'result'
              206  LOAD_STR                 'uint8'
              208  LOAD_CONST               0
              210  CALL_METHOD_3         3  ''
              212  POP_TOP          
              214  JUMP_FORWARD        230  'to 230'
            216_0  COME_FROM           198  '198'

 L.1500       216  LOAD_FAST                'event_msg'
              218  LOAD_METHOD              append
              220  LOAD_STR                 'result'
              222  LOAD_STR                 'uint8'
              224  LOAD_CONST               1
              226  CALL_METHOD_3         3  ''
              228  POP_TOP          
            230_0  COME_FROM           214  '214'

 L.1501       230  LOAD_FAST                'event_client'
              232  LOAD_METHOD              resp_event_msg
              234  LOAD_FAST                'event_msg'
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          

Parse error at or near `JUMP_LOOP' instruction at offset 138

            def run_test_thread(self, script_str):
                global _globals_exec
                try:
                    _globals_exec = {}
                    exec(script_str, _globals_exec)
                except Exception as e:
                    try:
                        logger.fatal(traceback.format_exc())
                    finally:
                        e = None
                        del e

            def reset_states(self):
                self.retry = 0
                self.script_raw_data = {}

            def get_link_state(self, event_client, msg):
                buff = msg['data']
                state = str(buff[0])
                logger.info('GET HDVT_UAV: link state changed to: %s' % state)
                if state == '0':
                    logger.info('GET HDVT_UAV: link down')
                    if self.script_ctrl.custome_skill_running == False and self.script_ctrl.off_control_running == False:
                        logger.info('stop script: %s' % self.script_ctrl.run_script_id)
                        self.script_ctrl.stop_running(self.script_ctrl.run_script_id, None)
                    else:
                        for custom_id in self.script_ctrl.custom_skill_config_dict.keys():
                            if custom_id <= '0':
                                if custom_id <= '9':
                                    logger.info('stop custome skill: %s' % custom_id)
                                    self.script_ctrl.stop_running(None, custom_id)

                else:
                    while state == '2':
                        for custom_id in self.script_ctrl.custom_skill_config_dict.keys():
                            if custom_id <= '0':
                                if custom_id <= '9':
                                    logger.info('stop custome skill: %s' % custom_id)
                                    self.script_ctrl.stop_running(None, custom_id)

            def request_get_version(self, event_client, msg):
                logger.info('REQUEST_CTRL: request version ')
                dev_ver_protol = 0
                dd = 0
                cc = 1
                bb = 0
                aa = 1
                service_name = 'DJI SCRATCH SYS'
                event_msg = duss_event_msg.unpack2EventMsg(msg)
                event_msg.clear()
                event_msg.append('ret_code', 'uint8', duml_cmdset.DUSS_MB_RET_OK)
                event_msg.append('dev_ver', 'uint8', dev_ver_protol)
                event_msg.append('name', 'string', service_name)
                event_msg.append('dd', 'uint8', dd)
                event_msg.append('cc', 'uint8', cc)
                event_msg.append('bb', 'uint8', bb)
                event_msg.append('aa', 'uint8', aa)
                event_msg.append('build', 'uint8', 5)
                event_msg.append('version', 'uint8', 0)
                event_msg.append('minor', 'uint8', 1)
                event_msg.append('major', 'uint8', 0)
                event_msg.append('cmdset', 'uint32', 0)
                event_msg.append('rooback', 'uint8', 0)
                event_client.resp_event_msg(event_msg)

            def request_push_heartbeat(self, event_client, msg):
                dev_ver_protol = 0
                service_name = 'DJI SCRATCH SYS'
                event_msg = duss_event_msg.unpack2EventMsg(msg)
                event_msg.clear()
                event_msg.append('ret_code', 'uint8', duml_cmdset.DUSS_MB_RET_OK)
                event_msg.append('dev_ver', 'uint8', dev_ver_protol)
                event_msg.append('name', 'string', service_name)
                event_msg.append('cmdset', 'uint32', 0)
                event_msg.append('rooback', 'uint8', 0)
                event_client.resp_event_msg(event_msg)

            def update_sys_date(self, event_client, msg):
                val = {
                  'year': 0, 'month': 0, 'day': 0, 'hour': 0, 'min': 0, 'sec': 0}
                buff = msg['data']
                val['year'] = buff[1] << 8 | buff[0]
                val['month'] = buff[2]
                val['day'] = buff[3]
                val['hour'] = buff[4]
                val['min'] = buff[5]
                val['sec'] = buff[6]
                val_year = str(val['year'])
                val_month = str(val['month'])
                val_day = str(val['day'])
                val_hour = str(val['hour'])
                val_min = str(val['min'])
                val_sec = str(val['sec'])
                val_str = val_year + '-' + val_month + '-' + val_day + ' ' + val_hour + ':' + val_min + ':' + val_sec
                t = time.strptime(val_str, '%Y-%m-%d %H:%M:%S')
                unlink_sys_time = time.mktime(t)
                link_sys_time = time.time()
                link_unlink_diff_time = link_sys_time - unlink_sys_time
                if link_unlink_diff_time > 10:
                    self.local_sub_service.set_sys_latest_start_time(link_unlink_diff_time)
                logger.info('UPDATE_DATE: date is:%s, %s, %s, %s, %s, %s' % (val['year'], val['month'], val['day'], val['hour'], val['min'], val['sec']))
                logger.info('SYS_TIME: unlinked_total_time is:%s' % unlink_sys_time)
                logger.info('SYS_TIME: link_sys_time is:%s' % link_sys_time)
                logger.info('SYS_TIME: link_unlink_diff_time is:%s' % link_unlink_diff_time)


        class LocalSubService(object):

            def __init__(self, event_client):
                self.event_client = event_client
                self.msg_buff = duss_event_msg.EventMsg(tools.hostid2senderid(event_client.my_host_id))
                self.armor_hit_info = {'id':0,  'time':0}
                self.sys_unixtime_info = 0
                self.sys_power_on_time = 0
                self.sys_latest_start_time = 0
                self.update_sys_time_flag = 0

            def init_sys_power_on_time(self):
                self.sys_power_on_time = time.time()
                logger.info('SYS_TIME: sys_power_on_time is:%s' % self.sys_power_on_time)

            def get_sys_latest_start_time(self):
                if self.update_sys_time_flag == 0:
                    logger.info('SYS_TIME: sys_latest_start_time is:%s' % self.sys_power_on_time)
                    return self.sys_power_on_time
                logger.info('SYS_TIME: sys_latest_start_time is:%s' % self.sys_latest_start_time)
                return self.sys_latest_start_time

            def set_sys_latest_start_time(self, diff_time):
                self.update_sys_time_flag = 1
                self.sys_latest_start_time = diff_time + self.sys_power_on_time
                logger.info('SYS_TIME: sys_latest_start_time is:%s' % self.sys_latest_start_time)

            def enable(self):
                self.enable_armor_hit_sub(self.armor_hit_process)
                self.info_query_register()

            def disable(self):
                self.disable_armor_hit_sub()

            def info_query_process(self, event_client, msg):
                data = msg['data']
                if data[0] == 1:
                    self.resp_armor_hit_info_req(event_client, msg)
                else:
                    if data[0] == 2:
                        self.unixtime_process()
                        self.resp_unixtime_info_req(event_client, msg)
                    else:
                        logger.fatal('NOT SUPPORT INFO QUERY TYPE')
                        event_client.resp_retcode(msg, duml_cmdset.DUSS_MB_RET_INVALID_PARAM)

            def info_query_register(self):
                cmd_set_id = duml_cmdset.DUSS_MB_CMDSET_RM << 8 | duml_cmdset.DUSS_MB_CMD_RM_SCRIPT_LOCAL_SUB_SERVICE
                self.event_client.async_req_register(cmd_set_id, self.info_query_process)

            def armor_hit_process(self, event_client, msg):
                data = msg['data']
                info = tools.byte_to_uint8(data[0:1])
                self.armor_hit_info['id'] = info >> 4
                self.armor_hit_info['time'] = int(time.time() * 1000 - self.get_sys_latest_start_time() * 1000)
                logger.info('ARMOR_HIT_TIME: armor_hit_info_time is:%s' % self.armor_hit_info['time'])

            def enable_armor_hit_sub(self, callback):
                cmd_set_id = duml_cmdset.DUSS_MB_CMDSET_RM << 8 | duml_cmdset.DUSS_MB_CMD_RM_HIT_EVENT
                self.event_client.async_req_register(cmd_set_id, callback)

            def disable_armor_hit_sub(self):
                cmd_set_id = duml_cmdset.DUSS_MB_CMDSET_RM << 8 | duml_cmdset.DUSS_MB_CMD_RM_HIT_EVENT
                self.event_client.async_req_unregister(cmd_set_id)

            def resp_armor_hit_info_req(self, event_msg, msg):
                armor_hit_info = dict(self.armor_hit_info)
                event_msg = duss_event_msg.unpack2EventMsg(msg)
                event_msg.clear()
                event_msg.append('ret_code', 'uint8', duml_cmdset.DUSS_MB_RET_OK)
                event_msg.append('id', 'uint8', armor_hit_info['id'])
                event_msg.append('timeH', 'uint32', armor_hit_info['time'] >> 32)
                event_msg.append('timeL', 'uint32', tools.to_uint32(armor_hit_info['time']))
                self.event_client.resp_event_msg(event_msg)

            def unixtime_process(self):
                self.sys_unixtime_info = int(time.time() * 1000 - self.get_sys_latest_start_time() * 1000)
                logger.info('SYS_TIME: sys_unixtime_info is:%s' % self.sys_unixtime_info)

            def resp_unixtime_info_req(self, event_msg, msg):
                event_msg = duss_event_msg.unpack2EventMsg(msg)
                event_msg.clear()
                event_msg.append('ret_code', 'uint8', duml_cmdset.DUSS_MB_RET_OK)
                event_msg.append('timeH', 'uint32', self.sys_unixtime_info >> 32)
                event_msg.append('timeL', 'uint32', tools.to_uint32(self.sys_unixtime_info))
                self.event_client.resp_event_msg(event_msg)