# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: .\sdk\plaintext_sdk\protocal_parser.py
# Compiled at: 2020-08-19 12:20:28
# Size of source mod 2**32: 30464 bytes
import queue, threading, time, json, traceback, os, re, event_client, rm_ctrl, rm_define, rm_log, tools, rm_socket
logger = rm_log.dji_scratch_logger_get()
PROTOCAL_MAPPING_TABLE_PATH = os.path.dirname(__file__) + '/protocal_mapping_table.json'
COMMAND_PORT = 40923
PUSH_PORT = 40924
EVENT_PORT = 40925
BROADCAST_PORT = 40926
INADDR_ANY = '0.0.0.0'
WIFI_DIRECT_CONNECTION_IP = '192.168.2.1'

class ProtocalParser(object):
    UART = 'uart'
    NETWORK = 'network'

    def __init__(self, event_dji_system, socket_obj, uart_obj):
        self.event_client = event_dji_system
        self.sdk_ctrl = rm_ctrl.SDKCtrl(event_dji_system)
        self.version = ''
        self.socket_obj = socket_obj
        self.uart_obj = uart_obj
        self.connection_obj = None
        self.command_socket_fd = None
        self.event_socket_fd = None
        self.push_socket_fd = None
        self.remote_host_ip = set()
        self.connection_socket_fd = {}
        self.data_queue = queue.Queue(512)
        self.uart_data_t = ''
        self.socket_data_t = ''
        self.command_execing_event = threading.Event()
        self.command_parser_callback = {'command':self.command_protocal_format_parser, 
         'version':self.version_protocal_format_parser, 
         'quit':self.quit_protocal_format_parser}
        self.data_process_thread = None
        self.protocal_mapping_table = None
        self.sdk_mode = False
        self.ctrl_obj = {}
        self.report_local_host_ip_timer = None

    def init(self, config={}):
        self.config = config
        f = open(PROTOCAL_MAPPING_TABLE_PATH, 'r')
        self.protocal_mapping_table = json.load(f)
        f.close()
        self.command_socket_fd = self.socket_obj.create((self.socket_obj.TCP_MODE),
          (
         INADDR_ANY, COMMAND_PORT),
          server=True,
          recv_msgq_size=8,
          send_msgq_size=8,
          connected_callback=(self._ProtocalParser__command_connected_callback),
          disconnected_callback=(self._ProtocalParser__command_disconnected_callback))
        if self.command_socket_fd:
            logger.info('command socket create successfully.')
        self.event_socket_fd = self.socket_obj.create((self.socket_obj.TCP_MODE),
          (
         INADDR_ANY, EVENT_PORT),
          server=True,
          recv_msgq_size=8,
          send_msgq_size=8,
          connected_callback=(self._ProtocalParser__event_connected_callback))
        if self.event_socket_fd:
            logger.info('event socket create successfully.')
        self.push_socket_fd = self.socket_obj.create((self.socket_obj.UDP_MODE),
          (
         INADDR_ANY, PUSH_PORT),
          server=False,
          recv_msgq_size=1,
          send_msgq_size=8)
        if self.push_socket_fd:
            logger.info('push socket create successfully.')
        self.broadcast_socket_fd = self.socket_obj.create((self.socket_obj.UDP_MODE),
          (
         INADDR_ANY, BROADCAST_PORT),
          server=False,
          recv_msgq_size=1,
          send_msgq_size=8)
        if self.broadcast_socket_fd:
            self.socket_obj.set_udp_default_target_addr(self.broadcast_socket_fd, ('<broadcast>', BROADCAST_PORT))
            logger.info('broadcast socket create successfully.')
        self.ctrl_obj = {}
        if self.report_local_host_ip_timer == None:
            self.report_local_host_ip_timer = tools.get_timer(2, self.report_local_host_ip)
            self.report_local_host_ip_timer.start()
        self.uart_obj.sdk_process_callback_register(self._ProtocalParser__uart_command_recv_callback)

    def __event_connected_callback(self, fd, new_fd):
        logger.info('New event connected')
        self.socket_obj.update_socket_info(new_fd,
          recv_msgq_size=1,
          send_msgq_size=8)
        if fd not in self.connection_socket_fd.keys():
            self.connection_socket_fd[fd] = []
        self.connection_socket_fd[fd].append(new_fd)

    def __event_recv_callback(self, fd, data):
        pass

    def __event_disconnected_callback(self, fd):
        pass

    def __command_connected_callback(self, fd, new_fd):
        if self.connection_obj == self.uart_obj:
            logger.info('Uart has already connected')
            return
        logger.info('New command connected')
        self.connection_status_report('connected', fd, new_fd)
        self.socket_obj.update_socket_info(new_fd,
          recv_msgq_size=8,
          send_msgq_size=8,
          recv_callback=(self._ProtocalParser__command_recv_callback))
        self.remote_host_ip.add(self.socket_obj.get_remote_host_ip(new_fd))
        if fd not in self.connection_socket_fd.keys():
            self.connection_socket_fd[fd] = []
        self.connection_socket_fd[fd].append(new_fd)

    def __command_recv_callback(self, fd, data):
        if self.connection_obj == self.uart_obj:
            logger.info('Uart has already connected')
            return
        self.socket_data_t += data
        if ';' in self.socket_data_t:
            data_list = self.socket_data_t.split(';')
            self.socket_data_t = data_list.pop(-1)
            for msg in data_list:
                self.protocal_parser(fd, msg, self.NETWORK)

        else:
            logger.info('Not found ; in data_list, waitting for next data')
            return

    def __command_disconnected_callback(self, fd):
        self.quit_protocal_format_parser(self.NETWORK, fd, None)
        self.connection_status_report('disconnected', fd, None)

    def __uart_command_recv_callback(self, data):
        logger.info(data)
        if self.connection_obj == self.socket_obj:
            logger.info('Network has already connected')
        else:
            self.uart_data_t += data
            if ';' in self.uart_data_t:
                data_list = self.uart_data_t.split(';')
                self.uart_data_t = data_list.pop(-1)
                logger.info(data_list)
                for msg in data_list:
                    self.protocal_parser(None, msg, self.UART)

            else:
                logger.info('Not found ; in data_list, waitting for next data')
                return

    def command_execing_start(self):
        self.command_execing_event.set()

    def command_execing_is_finish(self):
        self.command_execing_event.is_set()

    def command_execing_finish(self):
        self.command_execing_event.clear()

    def report_local_host_ip(self):
        ip = self.socket_obj.get_local_host_ip()
        if ip:
            if tools.is_station_mode():
                self.socket_obj.send(self.broadcast_socket_fd, 'robot ip %s' % ip)

    def sdk_robot_ctrl(self, ctrl):

        def init():
            self.ctrl_obj['event'] = event_client.EventClient()
            self.ctrl_obj['modulesStatus_ctrl'] = rm_ctrl.ModulesStatusCtrl(self.ctrl_obj['event'])
            self.ctrl_obj['blaster_ctrl'] = rm_ctrl.GunCtrl(self.ctrl_obj['event'])
            self.ctrl_obj['armor_ctrl'] = rm_ctrl.ArmorCtrl(self.ctrl_obj['event'])
            self.ctrl_obj['AI_ctrl'] = rm_ctrl.VisionCtrl(self.ctrl_obj['event'])
            self.ctrl_obj['chassis_ctrl'] = rm_ctrl.ChassisCtrl(self.ctrl_obj['event'])
            self.ctrl_obj['gimbal_ctrl'] = rm_ctrl.GimbalCtrl(self.ctrl_obj['event'])
            self.ctrl_obj['robot_ctrl'] = rm_ctrl.RobotCtrl(self.ctrl_obj['event'], self.ctrl_obj['chassis_ctrl'], self.ctrl_obj['gimbal_ctrl'])
            self.ctrl_obj['led_ctrl'] = rm_ctrl.LedCtrl(self.ctrl_obj['event'])
            self.ctrl_obj['media_ctrl'] = rm_ctrl.MediaCtrl(self.ctrl_obj['event'])
            self.ctrl_obj['mobile_ctrl'] = rm_ctrl.MobileCtrl(self.ctrl_obj['event'])
            self.ctrl_obj['tools'] = rm_ctrl.RobotTools(self.ctrl_obj['event'])
            self.ctrl_obj['sensor_adapter_ctrl'] = rm_ctrl.SensorAdapterCtrl(self.ctrl_obj['event'])
            self.ctrl_obj['ir_distance_sensor_ctrl'] = rm_ctrl.IrDistanceSensorCtrl(self.ctrl_obj['event'])
            self.ctrl_obj['servo_ctrl'] = rm_ctrl.ServoCtrl(self.ctrl_obj['event'])
            self.ctrl_obj['robotic_arm_ctrl'] = rm_ctrl.RoboticArmCtrl(self.ctrl_obj['event'])
            self.ctrl_obj['gripper_ctrl'] = rm_ctrl.RoboticGripperCtrl(self.ctrl_obj['event'])
            self.ctrl_obj['sdk_ctrl'] = rm_ctrl.SDKCtrl(self.ctrl_obj['event'])

        def ready():
            self.ctrl_obj['robot_ctrl'].init()
            self.ctrl_obj['modulesStatus_ctrl'].init()
            self.ctrl_obj['gimbal_ctrl'].init()
            self.ctrl_obj['chassis_ctrl'].init()
            self.ctrl_obj['led_ctrl'].init()
            self.ctrl_obj['blaster_ctrl'].init()
            self.ctrl_obj['mobile_ctrl'].init()
            self.ctrl_obj['servo_ctrl'].init()
            self.ctrl_obj['ir_distance_sensor_ctrl'].init()
            self.ctrl_obj['tools'].init()
            self.ctrl_obj['robot_ctrl'].enable_sdk_mode()
            self.ctrl_obj['robot_ctrl'].set_mode(rm_define.robot_mode_gimbal_follow)
            self.ctrl_obj['chassis_ctrl'].stop()
            self.ctrl_obj['tools'].program_timer_start()
            self.ctrl_obj['AI_ctrl'].sdk_info_push_callback_register(self.AI_info_push_callback)
            self.ctrl_obj['armor_ctrl'].sdk_event_push_callback_register(self.armor_event_push_callback)
            self.ctrl_obj['media_ctrl'].sdk_event_push_callback_register(self.applause_event_push_callback)
            self.ctrl_obj['chassis_ctrl'].sdk_info_push_callback_register(self.chassis_info_push_callback)
            self.ctrl_obj['gimbal_ctrl'].sdk_info_push_callback_register(self.gimbal_info_push_callback)
            self.ctrl_obj['sensor_adapter_ctrl'].sdk_event_push_callback_register(self.io_level_event_push_callback)

        def stop():
            self.ctrl_obj['blaster_ctrl'].stop()
            self.ctrl_obj['chassis_ctrl'].stop()
            self.ctrl_obj['gimbal_ctrl'].stop()
            self.ctrl_obj['media_ctrl'].stop()
            self.ctrl_obj['AI_ctrl'].stop()
            self.ctrl_obj['armor_ctrl'].stop()

        def exit():
            stop()
            self.ctrl_obj['robot_ctrl'].disable_sdk_mode()
            self.ctrl_obj['robot_ctrl'].exit()
            self.ctrl_obj['gimbal_ctrl'].exit()
            self.ctrl_obj['chassis_ctrl'].exit()
            self.ctrl_obj['blaster_ctrl'].exit()
            self.ctrl_obj['mobile_ctrl'].exit()
            self.ctrl_obj['armor_ctrl'].exit()
            self.ctrl_obj['media_ctrl'].exit()
            self.ctrl_obj['sdk_ctrl'].exit()
            self.ctrl_obj['ir_distance_sensor_ctrl'].exit()
            self.ctrl_obj['sensor_adapter_ctrl'].exit()
            self.ctrl_obj['servo_ctrl'].exit()
            self.ctrl_obj['gripper_ctrl'].exit()
            self.ctrl_obj['event'].stop()
            self.ctrl_obj.clear()

        if ctrl == 'init':
            init()
        else:
            if ctrl == 'ready':
                ready()
            else:
                if ctrl == 'stop':
                    stop()
                else:
                    if ctrl == 'exit':
                        exit()

    def __data_process--- This code section failed: ---

 L. 313         0  LOAD_FAST                'self'
                2  LOAD_METHOD              sdk_robot_ctrl
                4  LOAD_STR                 'init'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 314        10  LOAD_FAST                'self'
               12  LOAD_METHOD              sdk_robot_ctrl
               14  LOAD_STR                 'ready'
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          
             20_0  COME_FROM           730  '730'
             20_1  COME_FROM           216  '216'
             20_2  COME_FROM            74  '74'

 L. 316        20  LOAD_FAST                'self'
               22  LOAD_ATTR                sdk_mode
            24_26  POP_JUMP_IF_FALSE   732  'to 732'

 L. 317        28  LOAD_CONST               False
               30  STORE_FAST               'result'

 L. 318        32  SETUP_FINALLY        56  'to 56'

 L. 319        34  LOAD_FAST                'self'
               36  LOAD_ATTR                data_queue
               38  LOAD_ATTR                get
               40  LOAD_CONST               1
               42  LOAD_CONST               ('timeout',)
               44  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               46  UNPACK_SEQUENCE_2     2 
               48  STORE_FAST               'fd'
               50  STORE_FAST               'data'
               52  POP_BLOCK        
               54  JUMP_FORWARD         82  'to 82'
             56_0  COME_FROM_FINALLY    32  '32'

 L. 320        56  DUP_TOP          
               58  LOAD_GLOBAL              queue
               60  LOAD_ATTR                Empty
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE    80  'to 80'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L. 321        72  POP_EXCEPT       
               74  JUMP_LOOP            20  'to 20'
               76  POP_EXCEPT       
               78  JUMP_FORWARD         82  'to 82'
             80_0  COME_FROM            64  '64'
               80  END_FINALLY      
             82_0  COME_FROM            78  '78'
             82_1  COME_FROM            54  '54'

 L. 322        82  LOAD_FAST                'self'
               84  LOAD_METHOD              command_execing_start
               86  CALL_METHOD_0         0  ''
               88  POP_TOP          

 L. 323        90  LOAD_FAST                'data'
               92  LOAD_ATTR                req_type
               94  LOAD_STR                 'set'
               96  COMPARE_OP               ==
           98_100  POP_JUMP_IF_FALSE   402  'to 402'

 L. 324       102  LOAD_GLOBAL              str
              104  LOAD_FAST                'data'
              106  LOAD_ATTR                obj
              108  CALL_FUNCTION_1       1  ''
              110  LOAD_STR                 '.'
              112  BINARY_ADD       
              114  LOAD_GLOBAL              str
              116  LOAD_FAST                'data'
              118  LOAD_ATTR                function
              120  CALL_FUNCTION_1       1  ''
              122  BINARY_ADD       
              124  LOAD_GLOBAL              str
              126  LOAD_FAST                'data'
              128  LOAD_ATTR                param
              130  CALL_FUNCTION_1       1  ''
              132  BINARY_ADD       
              134  STORE_FAST               'cmd'

 L. 326       136  LOAD_GLOBAL              logger
              138  LOAD_METHOD              info
              140  LOAD_FAST                'cmd'
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          

 L. 328       146  SETUP_FINALLY       164  'to 164'

 L. 329       148  LOAD_GLOBAL              eval
              150  LOAD_FAST                'cmd'
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                ctrl_obj
              156  CALL_FUNCTION_2       2  ''
              158  STORE_FAST               'result'
              160  POP_BLOCK        
              162  JUMP_FORWARD        236  'to 236'
            164_0  COME_FROM_FINALLY   146  '146'

 L. 331       164  DUP_TOP          
              166  LOAD_GLOBAL              Exception
              168  COMPARE_OP               exception-match
              170  POP_JUMP_IF_FALSE   234  'to 234'
              172  POP_TOP          
              174  STORE_FAST               'e'
              176  POP_TOP          
              178  SETUP_FINALLY       222  'to 222'

 L. 332       180  LOAD_GLOBAL              logger
              182  LOAD_METHOD              fatal
              184  LOAD_GLOBAL              traceback
              186  LOAD_METHOD              format_exc
              188  CALL_METHOD_0         0  ''
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          

 L. 333       194  LOAD_FAST                'self'
              196  LOAD_METHOD              ack
              198  LOAD_FAST                'fd'
              200  LOAD_STR                 'fail'
              202  LOAD_FAST                'data'
              204  LOAD_ATTR                seq
              206  CALL_METHOD_3         3  ''
              208  POP_TOP          

 L. 334       210  POP_BLOCK        
              212  POP_EXCEPT       
              214  CALL_FINALLY        222  'to 222'
              216  JUMP_LOOP            20  'to 20'
              218  POP_BLOCK        
              220  BEGIN_FINALLY    
            222_0  COME_FROM           214  '214'
            222_1  COME_FROM_FINALLY   178  '178'
              222  LOAD_CONST               None
              224  STORE_FAST               'e'
              226  DELETE_FAST              'e'
              228  END_FINALLY      
              230  POP_EXCEPT       
              232  JUMP_FORWARD        236  'to 236'
            234_0  COME_FROM           170  '170'
              234  END_FINALLY      
            236_0  COME_FROM           232  '232'
            236_1  COME_FROM           162  '162'

 L. 335       236  LOAD_GLOBAL              type
              238  LOAD_FAST                'result'
              240  CALL_FUNCTION_1       1  ''
              242  LOAD_GLOBAL              tuple
              244  COMPARE_OP               ==
          246_248  POP_JUMP_IF_FALSE   264  'to 264'
              250  LOAD_FAST                'result'
              252  LOAD_CONST               -1
              254  BINARY_SUBSCR    
              256  LOAD_CONST               0
              258  COMPARE_OP               is
          260_262  POP_JUMP_IF_TRUE    308  'to 308'
            264_0  COME_FROM           246  '246'
              264  LOAD_GLOBAL              type
              266  LOAD_FAST                'result'
              268  CALL_FUNCTION_1       1  ''
              270  LOAD_GLOBAL              bool
              272  COMPARE_OP               ==
          274_276  POP_JUMP_IF_FALSE   288  'to 288'
              278  LOAD_FAST                'result'
              280  LOAD_CONST               True
              282  COMPARE_OP               ==
          284_286  POP_JUMP_IF_TRUE    308  'to 308'
            288_0  COME_FROM           274  '274'
              288  LOAD_FAST                'result'
              290  LOAD_CONST               None
              292  COMPARE_OP               ==
          294_296  POP_JUMP_IF_TRUE    308  'to 308'
              298  LOAD_FAST                'result'
              300  LOAD_CONST               0
              302  COMPARE_OP               is
          304_306  POP_JUMP_IF_FALSE   326  'to 326'
            308_0  COME_FROM           294  '294'
            308_1  COME_FROM           284  '284'
            308_2  COME_FROM           260  '260'

 L. 336       308  LOAD_FAST                'self'
              310  LOAD_METHOD              ack
              312  LOAD_FAST                'fd'
              314  LOAD_STR                 'ok'
              316  LOAD_FAST                'data'
              318  LOAD_ATTR                seq
              320  CALL_METHOD_3         3  ''
              322  POP_TOP          
              324  JUMP_FORWARD        342  'to 342'
            326_0  COME_FROM           304  '304'

 L. 338       326  LOAD_FAST                'self'
              328  LOAD_METHOD              ack
              330  LOAD_FAST                'fd'
              332  LOAD_STR                 'fail'
              334  LOAD_FAST                'data'
              336  LOAD_ATTR                seq
              338  CALL_METHOD_3         3  ''
              340  POP_TOP          
            342_0  COME_FROM           324  '324'

 L. 339       342  LOAD_GLOBAL              logger
              344  LOAD_METHOD              fatal
              346  LOAD_STR                 'process : '
              348  LOAD_GLOBAL              str
              350  LOAD_FAST                'data'
              352  LOAD_ATTR                obj
              354  CALL_FUNCTION_1       1  ''
              356  BINARY_ADD       
              358  LOAD_STR                 '.'
              360  BINARY_ADD       
              362  LOAD_GLOBAL              str
              364  LOAD_FAST                'data'
              366  LOAD_ATTR                function
              368  CALL_FUNCTION_1       1  ''
              370  BINARY_ADD       
              372  LOAD_GLOBAL              str
              374  LOAD_FAST                'data'
              376  LOAD_ATTR                param
              378  CALL_FUNCTION_1       1  ''
              380  BINARY_ADD       
              382  LOAD_STR                 ' exec_result:'
              384  BINARY_ADD       
              386  LOAD_GLOBAL              str
              388  LOAD_FAST                'result'
              390  CALL_FUNCTION_1       1  ''
              392  BINARY_ADD       
              394  CALL_METHOD_1         1  ''
              396  POP_TOP          
          398_400  JUMP_FORWARD        722  'to 722'
            402_0  COME_FROM            98  '98'

 L. 340       402  LOAD_FAST                'data'
              404  LOAD_ATTR                req_type
              406  LOAD_STR                 'get'
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   712  'to 712'

 L. 341       414  LOAD_FAST                'data'
              416  LOAD_ATTR                param
              418  LOAD_CONST               None
              420  COMPARE_OP               ==
          422_424  POP_JUMP_IF_FALSE   456  'to 456'

 L. 342       426  LOAD_GLOBAL              str
              428  LOAD_FAST                'data'
              430  LOAD_ATTR                obj
              432  CALL_FUNCTION_1       1  ''
              434  LOAD_STR                 '.'
              436  BINARY_ADD       
              438  LOAD_GLOBAL              str
              440  LOAD_FAST                'data'
              442  LOAD_ATTR                function
              444  CALL_FUNCTION_1       1  ''
              446  BINARY_ADD       
              448  LOAD_STR                 '()'
              450  BINARY_ADD       
              452  STORE_FAST               'cmd'
              454  JUMP_FORWARD        490  'to 490'
            456_0  COME_FROM           422  '422'

 L. 344       456  LOAD_GLOBAL              str
              458  LOAD_FAST                'data'
              460  LOAD_ATTR                obj
              462  CALL_FUNCTION_1       1  ''
              464  LOAD_STR                 '.'
              466  BINARY_ADD       
              468  LOAD_GLOBAL              str
              470  LOAD_FAST                'data'
              472  LOAD_ATTR                function
              474  CALL_FUNCTION_1       1  ''
              476  BINARY_ADD       
              478  LOAD_GLOBAL              str
              480  LOAD_FAST                'data'
              482  LOAD_ATTR                param
              484  CALL_FUNCTION_1       1  ''
              486  BINARY_ADD       
              488  STORE_FAST               'cmd'
            490_0  COME_FROM           454  '454'

 L. 346       490  LOAD_GLOBAL              logger
              492  LOAD_METHOD              info
              494  LOAD_FAST                'cmd'
              496  CALL_METHOD_1         1  ''
              498  POP_TOP          

 L. 348       500  SETUP_FINALLY       518  'to 518'

 L. 349       502  LOAD_GLOBAL              eval
              504  LOAD_FAST                'cmd'
              506  LOAD_FAST                'self'
              508  LOAD_ATTR                ctrl_obj
              510  CALL_FUNCTION_2       2  ''
              512  STORE_FAST               'result'
              514  POP_BLOCK        
              516  JUMP_FORWARD        584  'to 584'
            518_0  COME_FROM_FINALLY   500  '500'

 L. 351       518  DUP_TOP          
              520  LOAD_GLOBAL              Exception
              522  COMPARE_OP               exception-match
          524_526  POP_JUMP_IF_FALSE   582  'to 582'
              528  POP_TOP          
              530  STORE_FAST               'e'
              532  POP_TOP          
              534  SETUP_FINALLY       570  'to 570'

 L. 352       536  LOAD_GLOBAL              logger
              538  LOAD_METHOD              fatal
              540  LOAD_GLOBAL              traceback
              542  LOAD_METHOD              format_exc
              544  CALL_METHOD_0         0  ''
              546  CALL_METHOD_1         1  ''
              548  POP_TOP          

 L. 353       550  LOAD_FAST                'self'
              552  LOAD_METHOD              ack
              554  LOAD_FAST                'fd'
              556  LOAD_STR                 'fail'
              558  LOAD_FAST                'data'
              560  LOAD_ATTR                seq
              562  CALL_METHOD_3         3  ''
              564  POP_TOP          
              566  POP_BLOCK        
              568  BEGIN_FINALLY    
            570_0  COME_FROM_FINALLY   534  '534'
              570  LOAD_CONST               None
              572  STORE_FAST               'e'
              574  DELETE_FAST              'e'
              576  END_FINALLY      
              578  POP_EXCEPT       
              580  JUMP_FORWARD        584  'to 584'
            582_0  COME_FROM           524  '524'
              582  END_FINALLY      
            584_0  COME_FROM           580  '580'
            584_1  COME_FROM           516  '516'

 L. 354       584  LOAD_FAST                'data'
              586  LOAD_ATTR                seq
              588  STORE_FAST               'seq'

 L. 355       590  LOAD_STR                 ''
              592  STORE_FAST               'data'

 L. 356       594  LOAD_GLOBAL              type
              596  LOAD_FAST                'result'
              598  CALL_FUNCTION_1       1  ''
              600  LOAD_GLOBAL              tuple
              602  COMPARE_OP               ==
          604_606  POP_JUMP_IF_TRUE    622  'to 622'
              608  LOAD_GLOBAL              type
              610  LOAD_FAST                'result'
              612  CALL_FUNCTION_1       1  ''
              614  LOAD_GLOBAL              list
              616  COMPARE_OP               ==
          618_620  POP_JUMP_IF_FALSE   684  'to 684'
            622_0  COME_FROM           604  '604'

 L. 357       622  LOAD_FAST                'result'
              624  GET_ITER         
            626_0  COME_FROM           678  '678'
            626_1  COME_FROM           660  '660'
              626  FOR_ITER            682  'to 682'
              628  STORE_FAST               'i'

 L. 358       630  LOAD_GLOBAL              type
              632  LOAD_FAST                'i'
              634  CALL_FUNCTION_1       1  ''
              636  LOAD_GLOBAL              float
              638  COMPARE_OP               ==
          640_642  POP_JUMP_IF_FALSE   662  'to 662'

 L. 359       644  LOAD_FAST                'data'
              646  LOAD_STR                 '%.3f'
              648  LOAD_FAST                'i'
              650  BINARY_MODULO    
              652  BINARY_ADD       
              654  LOAD_STR                 ' '
              656  BINARY_ADD       
              658  STORE_FAST               'data'
              660  JUMP_LOOP           626  'to 626'
            662_0  COME_FROM           640  '640'

 L. 361       662  LOAD_FAST                'data'
              664  LOAD_GLOBAL              str
              666  LOAD_FAST                'i'
              668  CALL_FUNCTION_1       1  ''
              670  BINARY_ADD       
              672  LOAD_STR                 ' '
              674  BINARY_ADD       
              676  STORE_FAST               'data'
          678_680  JUMP_LOOP           626  'to 626'
            682_0  COME_FROM           626  '626'
              682  JUMP_FORWARD        696  'to 696'
            684_0  COME_FROM           618  '618'

 L. 363       684  LOAD_GLOBAL              str
              686  LOAD_FAST                'result'
              688  CALL_FUNCTION_1       1  ''
              690  LOAD_STR                 ' '
              692  BINARY_ADD       
              694  STORE_FAST               'data'
            696_0  COME_FROM           682  '682'

 L. 364       696  LOAD_FAST                'self'
              698  LOAD_METHOD              ack
              700  LOAD_FAST                'fd'
              702  LOAD_FAST                'data'
              704  LOAD_FAST                'seq'
              706  CALL_METHOD_3         3  ''
              708  POP_TOP          
              710  JUMP_FORWARD        722  'to 722'
            712_0  COME_FROM           410  '410'

 L. 366       712  LOAD_GLOBAL              time
              714  LOAD_METHOD              sleep
              716  LOAD_CONST               0.05
              718  CALL_METHOD_1         1  ''
              720  POP_TOP          
            722_0  COME_FROM           710  '710'
            722_1  COME_FROM           398  '398'

 L. 367       722  LOAD_FAST                'self'
              724  LOAD_METHOD              command_execing_finish
              726  CALL_METHOD_0         0  ''
              728  POP_TOP          
              730  JUMP_LOOP            20  'to 20'
            732_0  COME_FROM            24  '24'

 L. 369       732  LOAD_FAST                'self'
              734  LOAD_METHOD              sdk_robot_ctrl
              736  LOAD_STR                 'exit'
              738  CALL_METHOD_1         1  ''
              740  POP_TOP          

Parse error at or near `JUMP_LOOP' instruction at offset 216

    def protocal_parser(self, fd, data, mode=None):
        logger.info('Recv string: %s' % data)
        command = data.split(' ')
        if len(command) == 0:
            return
        seq = None
        if 'seq' in command:
            seq_pos = command.index('seq')
            if len(command) > seq_pos + 1:
                seq = command[seq_pos + 1]
                if seq.isdigit():
                    seq = int(seq)
                else:
                    if re.match('^0x[0-9a-fA-F]+$', seq):
                        seq = int(seq, 16)
                    else:
                        self.ack(fd, 'command format error: seq parse error')
            else:
                self.ack(fd, 'command format error: no seq value')
            command = command[0:seq_pos]
        if self.command_execing_is_finish():
            self.ack(fd, 'error', seq)
            return False
        command_obj = command[0]
        if command_obj in self.command_parser_callback.keys():
            result = self.command_parser_callback[command_obj](mode, fd, seq)
            if result == False or result == None:
                self.ack(fd, '%s exec error' % command_obj, seq)
            else:
                if result == True:
                    self.ack(fd, 'ok', seq)
                else:
                    self.ack(fd, result, seq)
        else:
            if not self.sdk_mode:
                self.ack(fd, 'not in sdk mode', seq)
                return False
            result = self.ctrl_protocal_format_parser(command, seq)
        if result == False or result == None:
            self.ack(fd, 'command format error: command parse error', seq)
        else:
            if not self.data_queue.full():
                try:
                    self.data_queue.put_nowait((fd, result))
                except Exception as e:
                    try:
                        logger.fatal(e)
                    finally:
                        e = None
                        del e

    def command_protocal_format_parser(self, mode, fd, seq):
        if self.sdk_mode == False:
            self.sdk_mode = True
            if self.data_process_thread == None or self.data_process_thread.is_alive() == False:
                self.data_process_thread = threading.Thread(target=(self._ProtocalParser__data_process))
                self.data_process_thread.start()
            if self.report_local_host_ip_timer:
                if self.report_local_host_ip_timer.is_start():
                    self.report_local_host_ip_timer.join()
                    self.report_local_host_ip_timer.stop()
            if mode == self.UART:
                self.connection_obj = self.uart_obj
                self.uart_data_t = ''
            else:
                if mode == self.NETWORK:
                    self.connection_obj = self.socket_obj
                    self.socket_data_t = ''
            return True
        return 'Already in SDK mode'

    def version_protocal_format_parser(self, mode, fd, seq):
        if 'version' in self.config.keys():
            return 'version ' + self.config['version']

    def quit_protocal_format_parser(self, mode, fd, seq):
        if self.data_process_thread:
            if self.data_process_thread.is_alive():
                if self.report_local_host_ip_timer == None:
                    self.report_local_host_ip_timer = tools.get_timer(2, self.connection_obj.report_local_host_ip)
                    self.report_local_host_ip_timer.start()
                else:
                    self.report_local_host_ip_timer.start()
                self.sdk_mode = False
                self.data_process_thread.join()
                self.ack(fd, 'ok', seq)
                if mode:
                    self.connection_obj = None
                    self.socket_data_t = ''
                    self.uart_data_t = ''
                return True
        self.ack(fd, 'quit sdk mode failed', seq)
        if mode:
            self.connection_obj = None
        return False

    def ctrl_protocal_format_parser--- This code section failed: ---

 L. 474         0  LOAD_GLOBAL              CommandPackage
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'cmdpkg'

 L. 475         6  LOAD_FAST                'seq'
                8  LOAD_FAST                'cmdpkg'
               10  STORE_ATTR               seq

 L. 477     12_14  SETUP_FINALLY      1346  'to 1346'

 L. 479        16  LOAD_FAST                'command'
               18  LOAD_CONST               0
               20  BINARY_SUBSCR    
               22  STORE_FAST               'obj'

 L. 480        24  LOAD_FAST                'obj'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                protocal_mapping_table
               30  LOAD_METHOD              keys
               32  CALL_METHOD_0         0  ''
               34  COMPARE_OP               in
               36  POP_JUMP_IF_FALSE    56  'to 56'

 L. 481        38  LOAD_FAST                'self'
               40  LOAD_ATTR                protocal_mapping_table
               42  LOAD_FAST                'obj'
               44  BINARY_SUBSCR    
               46  LOAD_STR                 'obj'
               48  BINARY_SUBSCR    
               50  LOAD_FAST                'cmdpkg'
               52  STORE_ATTR               obj
               54  JUMP_FORWARD         72  'to 72'
             56_0  COME_FROM            36  '36'

 L. 483        56  LOAD_GLOBAL              logger
               58  LOAD_METHOD              error
               60  LOAD_STR                 'obj parse error'
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          

 L. 484        66  POP_BLOCK        
               68  LOAD_CONST               False
               70  RETURN_VALUE     
             72_0  COME_FROM            54  '54'

 L. 487        72  LOAD_FAST                'command'
               74  LOAD_CONST               1
               76  BINARY_SUBSCR    
               78  STORE_FAST               'function'

 L. 488        80  LOAD_FAST                'function'
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                protocal_mapping_table
               86  LOAD_FAST                'obj'
               88  BINARY_SUBSCR    
               90  LOAD_STR                 'functions'
               92  BINARY_SUBSCR    
               94  LOAD_METHOD              keys
               96  CALL_METHOD_0         0  ''
               98  COMPARE_OP               in
          100_102  POP_JUMP_IF_FALSE  1326  'to 1326'

 L. 489       104  LOAD_FAST                'self'
              106  LOAD_ATTR                protocal_mapping_table
              108  LOAD_FAST                'obj'
              110  BINARY_SUBSCR    
              112  LOAD_STR                 'functions'
              114  BINARY_SUBSCR    
              116  LOAD_FAST                'function'
              118  BINARY_SUBSCR    
              120  STORE_FAST               'function_dict'

 L. 492       122  LOAD_STR                 '?'
              124  LOAD_FAST                'command'
              126  COMPARE_OP               in
          128_130  POP_JUMP_IF_FALSE   746  'to 746'

 L. 493       132  LOAD_FAST                'command'
              134  LOAD_CONST               2
              136  LOAD_CONST               None
              138  BUILD_SLICE_2         2 
              140  BINARY_SUBSCR    
              142  STORE_FAST               'params_list'

 L. 494       144  LOAD_STR                 '?'
              146  LOAD_FAST                'params_list'
              148  COMPARE_OP               in
              150  POP_JUMP_IF_FALSE   162  'to 162'

 L. 495       152  LOAD_FAST                'params_list'
              154  LOAD_METHOD              remove
              156  LOAD_STR                 '?'
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          
            162_0  COME_FROM           150  '150'

 L. 496       162  LOAD_FAST                'function_dict'
              164  LOAD_STR                 'get'
              166  BINARY_SUBSCR    
              168  LOAD_CONST               0
              170  BINARY_SUBSCR    
              172  LOAD_FAST                'cmdpkg'
              174  STORE_ATTR               function

 L. 497       176  LOAD_STR                 'get'
              178  LOAD_FAST                'cmdpkg'
              180  STORE_ATTR               req_type

 L. 498       182  BUILD_LIST_0          0 
              184  STORE_FAST               'params'

 L. 505       186  LOAD_FAST                'function_dict'
              188  LOAD_STR                 'get'
              190  BINARY_SUBSCR    
              192  LOAD_CONST               1
              194  LOAD_CONST               None
              196  BUILD_SLICE_2         2 
              198  BINARY_SUBSCR    
              200  GET_ITER         
            202_0  COME_FROM           718  '718'
            202_1  COME_FROM           706  '706'
          202_204  FOR_ITER            720  'to 720'
              206  STORE_FAST               'param'

 L. 507       208  LOAD_GLOBAL              len
              210  LOAD_FAST                'function_dict'
              212  LOAD_STR                 'get'
              214  BINARY_SUBSCR    
              216  LOAD_CONST               1
              218  LOAD_CONST               None
              220  BUILD_SLICE_2         2 
              222  BINARY_SUBSCR    
              224  CALL_FUNCTION_1       1  ''
              226  LOAD_CONST               1
              228  COMPARE_OP               ==
          230_232  POP_JUMP_IF_FALSE   490  'to 490'

 L. 508       234  LOAD_CONST               None
              236  STORE_FAST               'value'

 L. 509       238  LOAD_GLOBAL              len
              240  LOAD_FAST                'params_list'
              242  CALL_FUNCTION_1       1  ''
              244  LOAD_CONST               0
              246  COMPARE_OP               ==
          248_250  POP_JUMP_IF_FALSE   258  'to 258'

 L. 510       252  LOAD_CONST               None
              254  STORE_FAST               'value'
              256  JUMP_FORWARD        320  'to 320'
            258_0  COME_FROM           248  '248'

 L. 511       258  LOAD_GLOBAL              len
              260  LOAD_FAST                'params_list'
              262  CALL_FUNCTION_1       1  ''
              264  LOAD_CONST               1
              266  COMPARE_OP               ==
          268_270  POP_JUMP_IF_FALSE   282  'to 282'

 L. 512       272  LOAD_FAST                'params_list'
              274  LOAD_CONST               0
              276  BINARY_SUBSCR    
              278  STORE_FAST               'value'
              280  JUMP_FORWARD        320  'to 320'
            282_0  COME_FROM           268  '268'

 L. 513       282  LOAD_FAST                'params_list'
              284  LOAD_CONST               0
              286  BINARY_SUBSCR    
              288  LOAD_FAST                'function_dict'
              290  LOAD_STR                 'get'
              292  BINARY_SUBSCR    
              294  LOAD_CONST               1
              296  LOAD_CONST               None
              298  BUILD_SLICE_2         2 
              300  BINARY_SUBSCR    
              302  LOAD_CONST               0
              304  BINARY_SUBSCR    
              306  COMPARE_OP               ==
          308_310  POP_JUMP_IF_FALSE   320  'to 320'

 L. 514       312  LOAD_FAST                'params_list'
              314  LOAD_CONST               1
              316  BINARY_SUBSCR    
              318  STORE_FAST               'value'
            320_0  COME_FROM           308  '308'
            320_1  COME_FROM           280  '280'
            320_2  COME_FROM           256  '256'

 L. 515       320  LOAD_FAST                'value'
          322_324  POP_JUMP_IF_FALSE   346  'to 346'
              326  LOAD_FAST                'value'
              328  LOAD_METHOD              isdigit
              330  CALL_METHOD_0         0  ''
          332_334  POP_JUMP_IF_FALSE   346  'to 346'

 L. 516       336  LOAD_GLOBAL              int
              338  LOAD_FAST                'value'
              340  CALL_FUNCTION_1       1  ''
              342  STORE_FAST               'value'
              344  JUMP_FORWARD        474  'to 474'
            346_0  COME_FROM           332  '332'
            346_1  COME_FROM           322  '322'

 L. 517       346  LOAD_GLOBAL              re
              348  LOAD_METHOD              match
              350  LOAD_STR                 '^0x[0-9a-fA-F]+$'
              352  LOAD_FAST                'value'
              354  CALL_METHOD_2         2  ''
          356_358  POP_JUMP_IF_FALSE   372  'to 372'

 L. 518       360  LOAD_GLOBAL              int
              362  LOAD_FAST                'value'
              364  LOAD_CONST               16
              366  CALL_FUNCTION_2       2  ''
              368  STORE_FAST               'value'
              370  JUMP_FORWARD        474  'to 474'
            372_0  COME_FROM           356  '356'

 L. 519       372  LOAD_FAST                'value'
              374  LOAD_STR                 'True'
              376  COMPARE_OP               ==
          378_380  POP_JUMP_IF_TRUE    392  'to 392'
              382  LOAD_FAST                'value'
              384  LOAD_STR                 'true'
              386  COMPARE_OP               ==
          388_390  POP_JUMP_IF_FALSE   398  'to 398'
            392_0  COME_FROM           378  '378'

 L. 520       392  LOAD_CONST               True
              394  STORE_FAST               'value'
              396  JUMP_FORWARD        474  'to 474'
            398_0  COME_FROM           388  '388'

 L. 521       398  LOAD_FAST                'value'
              400  LOAD_STR                 'False'
              402  COMPARE_OP               ==
          404_406  POP_JUMP_IF_TRUE    418  'to 418'
              408  LOAD_FAST                'value'
              410  LOAD_STR                 'false'
              412  COMPARE_OP               ==
          414_416  POP_JUMP_IF_FALSE   424  'to 424'
            418_0  COME_FROM           404  '404'

 L. 522       418  LOAD_CONST               False
              420  STORE_FAST               'value'
              422  JUMP_FORWARD        474  'to 474'
            424_0  COME_FROM           414  '414'

 L. 524       424  SETUP_FINALLY       438  'to 438'

 L. 525       426  LOAD_GLOBAL              float
              428  LOAD_FAST                'value'
              430  CALL_FUNCTION_1       1  ''
              432  STORE_FAST               'value'
              434  POP_BLOCK        
              436  JUMP_FORWARD        474  'to 474'
            438_0  COME_FROM_FINALLY   424  '424'

 L. 526       438  DUP_TOP          
              440  LOAD_GLOBAL              Exception
              442  COMPARE_OP               exception-match
          444_446  POP_JUMP_IF_FALSE   472  'to 472'
              448  POP_TOP          
              450  STORE_FAST               'e'
              452  POP_TOP          
              454  SETUP_FINALLY       460  'to 460'

 L. 527       456  POP_BLOCK        
              458  BEGIN_FINALLY    
            460_0  COME_FROM_FINALLY   454  '454'
              460  LOAD_CONST               None
              462  STORE_FAST               'e'
              464  DELETE_FAST              'e'
              466  END_FINALLY      
              468  POP_EXCEPT       
              470  JUMP_FORWARD        474  'to 474'
            472_0  COME_FROM           444  '444'
              472  END_FINALLY      
            474_0  COME_FROM           470  '470'
            474_1  COME_FROM           436  '436'
            474_2  COME_FROM           422  '422'
            474_3  COME_FROM           396  '396'
            474_4  COME_FROM           370  '370'
            474_5  COME_FROM           344  '344'

 L. 528       474  LOAD_FAST                'params'
              476  LOAD_METHOD              append
              478  LOAD_FAST                'value'
              480  CALL_METHOD_1         1  ''
              482  POP_TOP          

 L. 529       484  POP_TOP          
          486_488  JUMP_FORWARD        720  'to 720'
            490_0  COME_FROM           230  '230'

 L. 532       490  LOAD_FAST                'param'
              492  LOAD_FAST                'params_list'
              494  COMPARE_OP               in
          496_498  POP_JUMP_IF_FALSE   708  'to 708'
              500  LOAD_FAST                'params_list'
              502  LOAD_METHOD              index
              504  LOAD_FAST                'param'
              506  CALL_METHOD_1         1  ''
              508  LOAD_CONST               1
              510  BINARY_ADD       
              512  LOAD_GLOBAL              len
              514  LOAD_FAST                'params_list'
              516  CALL_FUNCTION_1       1  ''
              518  COMPARE_OP               <
          520_522  POP_JUMP_IF_FALSE   708  'to 708'

 L. 533       524  LOAD_FAST                'params_list'
              526  LOAD_FAST                'params_list'
              528  LOAD_METHOD              index
              530  LOAD_FAST                'param'
              532  CALL_METHOD_1         1  ''
              534  LOAD_CONST               1
              536  BINARY_ADD       
              538  BINARY_SUBSCR    
              540  STORE_FAST               'value'

 L. 534       542  LOAD_FAST                'value'
          544_546  POP_JUMP_IF_FALSE   568  'to 568'
              548  LOAD_FAST                'value'
              550  LOAD_METHOD              isdigit
              552  CALL_METHOD_0         0  ''
          554_556  POP_JUMP_IF_FALSE   568  'to 568'

 L. 535       558  LOAD_GLOBAL              int
              560  LOAD_FAST                'value'
              562  CALL_FUNCTION_1       1  ''
              564  STORE_FAST               'value'
              566  JUMP_FORWARD        696  'to 696'
            568_0  COME_FROM           554  '554'
            568_1  COME_FROM           544  '544'

 L. 536       568  LOAD_GLOBAL              re
              570  LOAD_METHOD              match
              572  LOAD_STR                 '^0x[0-9a-fA-F]+$'
              574  LOAD_FAST                'value'
              576  CALL_METHOD_2         2  ''
          578_580  POP_JUMP_IF_FALSE   594  'to 594'

 L. 537       582  LOAD_GLOBAL              int
              584  LOAD_FAST                'value'
              586  LOAD_CONST               16
              588  CALL_FUNCTION_2       2  ''
              590  STORE_FAST               'value'
              592  JUMP_FORWARD        696  'to 696'
            594_0  COME_FROM           578  '578'

 L. 538       594  LOAD_FAST                'value'
              596  LOAD_STR                 'True'
              598  COMPARE_OP               ==
          600_602  POP_JUMP_IF_TRUE    614  'to 614'
              604  LOAD_FAST                'value'
              606  LOAD_STR                 'true'
              608  COMPARE_OP               ==
          610_612  POP_JUMP_IF_FALSE   620  'to 620'
            614_0  COME_FROM           600  '600'

 L. 539       614  LOAD_CONST               True
              616  STORE_FAST               'value'
              618  JUMP_FORWARD        696  'to 696'
            620_0  COME_FROM           610  '610'

 L. 540       620  LOAD_FAST                'value'
              622  LOAD_STR                 'False'
              624  COMPARE_OP               ==
          626_628  POP_JUMP_IF_TRUE    640  'to 640'
              630  LOAD_FAST                'value'
              632  LOAD_STR                 'false'
              634  COMPARE_OP               ==
          636_638  POP_JUMP_IF_FALSE   646  'to 646'
            640_0  COME_FROM           626  '626'

 L. 541       640  LOAD_CONST               False
              642  STORE_FAST               'value'
              644  JUMP_FORWARD        696  'to 696'
            646_0  COME_FROM           636  '636'

 L. 543       646  SETUP_FINALLY       660  'to 660'

 L. 544       648  LOAD_GLOBAL              float
              650  LOAD_FAST                'value'
              652  CALL_FUNCTION_1       1  ''
              654  STORE_FAST               'value'
              656  POP_BLOCK        
              658  JUMP_FORWARD        696  'to 696'
            660_0  COME_FROM_FINALLY   646  '646'

 L. 545       660  DUP_TOP          
              662  LOAD_GLOBAL              Exception
              664  COMPARE_OP               exception-match
          666_668  POP_JUMP_IF_FALSE   694  'to 694'
              670  POP_TOP          
              672  STORE_FAST               'e'
              674  POP_TOP          
              676  SETUP_FINALLY       682  'to 682'

 L. 546       678  POP_BLOCK        
              680  BEGIN_FINALLY    
            682_0  COME_FROM_FINALLY   676  '676'
              682  LOAD_CONST               None
              684  STORE_FAST               'e'
              686  DELETE_FAST              'e'
              688  END_FINALLY      
              690  POP_EXCEPT       
              692  JUMP_FORWARD        696  'to 696'
            694_0  COME_FROM           666  '666'
              694  END_FINALLY      
            696_0  COME_FROM           692  '692'
            696_1  COME_FROM           658  '658'
            696_2  COME_FROM           644  '644'
            696_3  COME_FROM           618  '618'
            696_4  COME_FROM           592  '592'
            696_5  COME_FROM           566  '566'

 L. 547       696  LOAD_FAST                'params'
              698  LOAD_METHOD              append
              700  LOAD_FAST                'value'
              702  CALL_METHOD_1         1  ''
              704  POP_TOP          
              706  JUMP_LOOP           202  'to 202'
            708_0  COME_FROM           520  '520'
            708_1  COME_FROM           496  '496'

 L. 549       708  LOAD_FAST                'params'
              710  LOAD_METHOD              append
              712  LOAD_CONST               None
              714  CALL_METHOD_1         1  ''
              716  POP_TOP          
              718  JUMP_LOOP           202  'to 202'
            720_0  COME_FROM           486  '486'
            720_1  COME_FROM           202  '202'

 L. 551       720  LOAD_GLOBAL              tuple
              722  LOAD_FAST                'params'
              724  CALL_FUNCTION_1       1  ''
              726  LOAD_FAST                'cmdpkg'
              728  STORE_ATTR               param

 L. 552       730  LOAD_GLOBAL              logger
              732  LOAD_METHOD              info
              734  LOAD_FAST                'cmdpkg'
              736  LOAD_ATTR                param
              738  CALL_METHOD_1         1  ''
              740  POP_TOP          
          742_744  JUMP_FORWARD       1342  'to 1342'
            746_0  COME_FROM           128  '128'

 L. 557       746  LOAD_FAST                'command'
              748  LOAD_CONST               2
              750  LOAD_CONST               None
              752  BUILD_SLICE_2         2 
              754  BINARY_SUBSCR    
              756  STORE_FAST               'params_list'

 L. 558       758  LOAD_FAST                'function_dict'
              760  LOAD_STR                 'set'
              762  BINARY_SUBSCR    
              764  LOAD_CONST               0
              766  BINARY_SUBSCR    
              768  LOAD_FAST                'cmdpkg'
              770  STORE_ATTR               function

 L. 559       772  LOAD_STR                 'set'
              774  LOAD_FAST                'cmdpkg'
              776  STORE_ATTR               req_type

 L. 560       778  BUILD_LIST_0          0 
              780  STORE_FAST               'params'

 L. 562       782  LOAD_FAST                'function_dict'
              784  LOAD_STR                 'set'
              786  BINARY_SUBSCR    
              788  LOAD_CONST               1
              790  LOAD_CONST               None
              792  BUILD_SLICE_2         2 
              794  BINARY_SUBSCR    
              796  GET_ITER         
            798_0  COME_FROM          1298  '1298'
            798_1  COME_FROM          1286  '1286'
          798_800  FOR_ITER           1302  'to 1302'
              802  STORE_FAST               'param'

 L. 564       804  LOAD_GLOBAL              len
              806  LOAD_FAST                'function_dict'
              808  LOAD_STR                 'set'
              810  BINARY_SUBSCR    
              812  LOAD_CONST               1
              814  LOAD_CONST               None
              816  BUILD_SLICE_2         2 
              818  BINARY_SUBSCR    
              820  CALL_FUNCTION_1       1  ''
              822  LOAD_CONST               1
              824  COMPARE_OP               ==
          826_828  POP_JUMP_IF_FALSE  1076  'to 1076'

 L. 565       830  LOAD_CONST               None
              832  STORE_FAST               'value'

 L. 566       834  LOAD_GLOBAL              len
              836  LOAD_FAST                'params_list'
              838  CALL_FUNCTION_1       1  ''
              840  LOAD_CONST               0
              842  COMPARE_OP               ==
          844_846  POP_JUMP_IF_FALSE   854  'to 854'

 L. 567       848  LOAD_CONST               None
              850  STORE_FAST               'value'
              852  JUMP_FORWARD        900  'to 900'
            854_0  COME_FROM           844  '844'

 L. 568       854  LOAD_GLOBAL              len
              856  LOAD_FAST                'params_list'
              858  CALL_FUNCTION_1       1  ''
              860  LOAD_CONST               1
              862  COMPARE_OP               ==
          864_866  POP_JUMP_IF_FALSE   878  'to 878'

 L. 569       868  LOAD_FAST                'params_list'
              870  LOAD_CONST               0
              872  BINARY_SUBSCR    
              874  STORE_FAST               'value'
              876  JUMP_FORWARD        900  'to 900'
            878_0  COME_FROM           864  '864'

 L. 570       878  LOAD_GLOBAL              len
              880  LOAD_FAST                'params_list'
              882  CALL_FUNCTION_1       1  ''
              884  LOAD_CONST               2
              886  COMPARE_OP               ==
          888_890  POP_JUMP_IF_FALSE   900  'to 900'

 L. 571       892  LOAD_FAST                'params_list'
              894  LOAD_CONST               1
              896  BINARY_SUBSCR    
              898  STORE_FAST               'value'
            900_0  COME_FROM           888  '888'
            900_1  COME_FROM           876  '876'
            900_2  COME_FROM           852  '852'

 L. 572       900  LOAD_FAST                'value'
          902_904  POP_JUMP_IF_FALSE   926  'to 926'
              906  LOAD_FAST                'value'
              908  LOAD_METHOD              isdigit
              910  CALL_METHOD_0         0  ''
          912_914  POP_JUMP_IF_FALSE   926  'to 926'

 L. 573       916  LOAD_GLOBAL              int
              918  LOAD_FAST                'value'
              920  CALL_FUNCTION_1       1  ''
              922  STORE_FAST               'value'
              924  JUMP_FORWARD       1060  'to 1060'
            926_0  COME_FROM           912  '912'
            926_1  COME_FROM           902  '902'

 L. 574       926  LOAD_FAST                'value'
          928_930  POP_JUMP_IF_FALSE   958  'to 958'
              932  LOAD_GLOBAL              re
              934  LOAD_METHOD              match
              936  LOAD_STR                 '^0x[0-9a-fA-F]+$'
              938  LOAD_FAST                'value'
              940  CALL_METHOD_2         2  ''
          942_944  POP_JUMP_IF_FALSE   958  'to 958'

 L. 575       946  LOAD_GLOBAL              int
              948  LOAD_FAST                'value'
              950  LOAD_CONST               16
              952  CALL_FUNCTION_2       2  ''
              954  STORE_FAST               'value'
              956  JUMP_FORWARD       1060  'to 1060'
            958_0  COME_FROM           942  '942'
            958_1  COME_FROM           928  '928'

 L. 576       958  LOAD_FAST                'value'
              960  LOAD_STR                 'True'
              962  COMPARE_OP               ==
          964_966  POP_JUMP_IF_TRUE    978  'to 978'
              968  LOAD_FAST                'value'
              970  LOAD_STR                 'true'
              972  COMPARE_OP               ==
          974_976  POP_JUMP_IF_FALSE   984  'to 984'
            978_0  COME_FROM           964  '964'

 L. 577       978  LOAD_CONST               True
              980  STORE_FAST               'value'
              982  JUMP_FORWARD       1060  'to 1060'
            984_0  COME_FROM           974  '974'

 L. 578       984  LOAD_FAST                'value'
              986  LOAD_STR                 'False'
              988  COMPARE_OP               ==
          990_992  POP_JUMP_IF_TRUE   1004  'to 1004'
              994  LOAD_FAST                'value'
              996  LOAD_STR                 'false'
              998  COMPARE_OP               ==
         1000_1002  POP_JUMP_IF_FALSE  1010  'to 1010'
           1004_0  COME_FROM           990  '990'

 L. 579      1004  LOAD_CONST               False
             1006  STORE_FAST               'value'
             1008  JUMP_FORWARD       1060  'to 1060'
           1010_0  COME_FROM          1000  '1000'

 L. 581      1010  SETUP_FINALLY      1024  'to 1024'

 L. 582      1012  LOAD_GLOBAL              float
             1014  LOAD_FAST                'value'
             1016  CALL_FUNCTION_1       1  ''
             1018  STORE_FAST               'value'
             1020  POP_BLOCK        
             1022  JUMP_FORWARD       1060  'to 1060'
           1024_0  COME_FROM_FINALLY  1010  '1010'

 L. 583      1024  DUP_TOP          
             1026  LOAD_GLOBAL              Exception
             1028  COMPARE_OP               exception-match
         1030_1032  POP_JUMP_IF_FALSE  1058  'to 1058'
             1034  POP_TOP          
             1036  STORE_FAST               'e'
             1038  POP_TOP          
             1040  SETUP_FINALLY      1046  'to 1046'

 L. 584      1042  POP_BLOCK        
             1044  BEGIN_FINALLY    
           1046_0  COME_FROM_FINALLY  1040  '1040'
             1046  LOAD_CONST               None
             1048  STORE_FAST               'e'
             1050  DELETE_FAST              'e'
             1052  END_FINALLY      
             1054  POP_EXCEPT       
             1056  JUMP_FORWARD       1060  'to 1060'
           1058_0  COME_FROM          1030  '1030'
             1058  END_FINALLY      
           1060_0  COME_FROM          1056  '1056'
           1060_1  COME_FROM          1022  '1022'
           1060_2  COME_FROM          1008  '1008'
           1060_3  COME_FROM           982  '982'
           1060_4  COME_FROM           956  '956'
           1060_5  COME_FROM           924  '924'

 L. 585      1060  LOAD_FAST                'params'
             1062  LOAD_METHOD              append
             1064  LOAD_FAST                'value'
             1066  CALL_METHOD_1         1  ''
             1068  POP_TOP          

 L. 586      1070  POP_TOP          
         1072_1074  JUMP_FORWARD       1302  'to 1302'
           1076_0  COME_FROM           826  '826'

 L. 589      1076  LOAD_FAST                'param'
             1078  LOAD_FAST                'params_list'
             1080  COMPARE_OP               in
         1082_1084  POP_JUMP_IF_FALSE  1288  'to 1288'
             1086  LOAD_FAST                'params_list'
             1088  LOAD_METHOD              index
             1090  LOAD_FAST                'param'
             1092  CALL_METHOD_1         1  ''
             1094  LOAD_CONST               1
             1096  BINARY_ADD       
             1098  LOAD_GLOBAL              len
             1100  LOAD_FAST                'params_list'
             1102  CALL_FUNCTION_1       1  ''
             1104  COMPARE_OP               <
         1106_1108  POP_JUMP_IF_FALSE  1288  'to 1288'

 L. 590      1110  LOAD_FAST                'params_list'
             1112  LOAD_FAST                'params_list'
             1114  LOAD_METHOD              index
             1116  LOAD_FAST                'param'
             1118  CALL_METHOD_1         1  ''
             1120  LOAD_CONST               1
             1122  BINARY_ADD       
             1124  BINARY_SUBSCR    
             1126  STORE_FAST               'value'

 L. 591      1128  LOAD_FAST                'value'
             1130  LOAD_METHOD              isdigit
             1132  CALL_METHOD_0         0  ''
         1134_1136  POP_JUMP_IF_FALSE  1148  'to 1148'

 L. 592      1138  LOAD_GLOBAL              int
             1140  LOAD_FAST                'value'
             1142  CALL_FUNCTION_1       1  ''
             1144  STORE_FAST               'value'
             1146  JUMP_FORWARD       1276  'to 1276'
           1148_0  COME_FROM          1134  '1134'

 L. 593      1148  LOAD_GLOBAL              re
             1150  LOAD_METHOD              match
             1152  LOAD_STR                 '^0x[0-9a-fA-F]+$'
             1154  LOAD_FAST                'value'
             1156  CALL_METHOD_2         2  ''
         1158_1160  POP_JUMP_IF_FALSE  1174  'to 1174'

 L. 594      1162  LOAD_GLOBAL              int
             1164  LOAD_FAST                'value'
             1166  LOAD_CONST               16
             1168  CALL_FUNCTION_2       2  ''
             1170  STORE_FAST               'value'
             1172  JUMP_FORWARD       1276  'to 1276'
           1174_0  COME_FROM          1158  '1158'

 L. 595      1174  LOAD_FAST                'value'
             1176  LOAD_STR                 'True'
             1178  COMPARE_OP               ==
         1180_1182  POP_JUMP_IF_TRUE   1194  'to 1194'
             1184  LOAD_FAST                'value'
             1186  LOAD_STR                 'true'
             1188  COMPARE_OP               ==
         1190_1192  POP_JUMP_IF_FALSE  1200  'to 1200'
           1194_0  COME_FROM          1180  '1180'

 L. 596      1194  LOAD_CONST               True
             1196  STORE_FAST               'value'
             1198  JUMP_FORWARD       1276  'to 1276'
           1200_0  COME_FROM          1190  '1190'

 L. 597      1200  LOAD_FAST                'value'
             1202  LOAD_STR                 'False'
             1204  COMPARE_OP               ==
         1206_1208  POP_JUMP_IF_TRUE   1220  'to 1220'
             1210  LOAD_FAST                'value'
             1212  LOAD_STR                 'false'
             1214  COMPARE_OP               ==
         1216_1218  POP_JUMP_IF_FALSE  1226  'to 1226'
           1220_0  COME_FROM          1206  '1206'

 L. 598      1220  LOAD_CONST               False
             1222  STORE_FAST               'value'
             1224  JUMP_FORWARD       1276  'to 1276'
           1226_0  COME_FROM          1216  '1216'

 L. 600      1226  SETUP_FINALLY      1240  'to 1240'

 L. 601      1228  LOAD_GLOBAL              float
             1230  LOAD_FAST                'value'
             1232  CALL_FUNCTION_1       1  ''
             1234  STORE_FAST               'value'
             1236  POP_BLOCK        
             1238  JUMP_FORWARD       1276  'to 1276'
           1240_0  COME_FROM_FINALLY  1226  '1226'

 L. 602      1240  DUP_TOP          
             1242  LOAD_GLOBAL              Exception
             1244  COMPARE_OP               exception-match
         1246_1248  POP_JUMP_IF_FALSE  1274  'to 1274'
             1250  POP_TOP          
             1252  STORE_FAST               'e'
             1254  POP_TOP          
             1256  SETUP_FINALLY      1262  'to 1262'

 L. 603      1258  POP_BLOCK        
             1260  BEGIN_FINALLY    
           1262_0  COME_FROM_FINALLY  1256  '1256'
             1262  LOAD_CONST               None
             1264  STORE_FAST               'e'
             1266  DELETE_FAST              'e'
             1268  END_FINALLY      
             1270  POP_EXCEPT       
             1272  JUMP_FORWARD       1276  'to 1276'
           1274_0  COME_FROM          1246  '1246'
             1274  END_FINALLY      
           1276_0  COME_FROM          1272  '1272'
           1276_1  COME_FROM          1238  '1238'
           1276_2  COME_FROM          1224  '1224'
           1276_3  COME_FROM          1198  '1198'
           1276_4  COME_FROM          1172  '1172'
           1276_5  COME_FROM          1146  '1146'

 L. 604      1276  LOAD_FAST                'params'
             1278  LOAD_METHOD              append
             1280  LOAD_FAST                'value'
             1282  CALL_METHOD_1         1  ''
             1284  POP_TOP          
             1286  JUMP_LOOP           798  'to 798'
           1288_0  COME_FROM          1106  '1106'
           1288_1  COME_FROM          1082  '1082'

 L. 606      1288  LOAD_FAST                'params'
             1290  LOAD_METHOD              append
             1292  LOAD_CONST               None
             1294  CALL_METHOD_1         1  ''
             1296  POP_TOP          
         1298_1300  JUMP_LOOP           798  'to 798'
           1302_0  COME_FROM          1072  '1072'
           1302_1  COME_FROM           798  '798'

 L. 608      1302  LOAD_GLOBAL              tuple
             1304  LOAD_FAST                'params'
             1306  CALL_FUNCTION_1       1  ''
             1308  LOAD_FAST                'cmdpkg'
             1310  STORE_ATTR               param

 L. 609      1312  LOAD_GLOBAL              logger
             1314  LOAD_METHOD              info
             1316  LOAD_FAST                'cmdpkg'
             1318  LOAD_ATTR                param
             1320  CALL_METHOD_1         1  ''
             1322  POP_TOP          
             1324  JUMP_FORWARD       1342  'to 1342'
           1326_0  COME_FROM           100  '100'

 L. 611      1326  LOAD_GLOBAL              logger
             1328  LOAD_METHOD              error
             1330  LOAD_STR                 'function key parse error'
             1332  CALL_METHOD_1         1  ''
             1334  POP_TOP          

 L. 612      1336  POP_BLOCK        
             1338  LOAD_CONST               False
             1340  RETURN_VALUE     
           1342_0  COME_FROM          1324  '1324'
           1342_1  COME_FROM           742  '742'
             1342  POP_BLOCK        
             1344  JUMP_FORWARD       1402  'to 1402'
           1346_0  COME_FROM_FINALLY    12  '12'

 L. 613      1346  DUP_TOP          
             1348  LOAD_GLOBAL              Exception
             1350  COMPARE_OP               exception-match
         1352_1354  POP_JUMP_IF_FALSE  1400  'to 1400'
             1356  POP_TOP          
             1358  STORE_FAST               'e'
             1360  POP_TOP          
             1362  SETUP_FINALLY      1388  'to 1388'

 L. 614      1364  LOAD_GLOBAL              logger
             1366  LOAD_METHOD              fatal
             1368  LOAD_GLOBAL              traceback
             1370  LOAD_METHOD              format_exc
             1372  CALL_METHOD_0         0  ''
             1374  CALL_METHOD_1         1  ''
             1376  POP_TOP          

 L. 615      1378  POP_BLOCK        
             1380  POP_EXCEPT       
             1382  CALL_FINALLY       1388  'to 1388'
             1384  LOAD_CONST               False
             1386  RETURN_VALUE     
           1388_0  COME_FROM          1382  '1382'
           1388_1  COME_FROM_FINALLY  1362  '1362'
             1388  LOAD_CONST               None
             1390  STORE_FAST               'e'
             1392  DELETE_FAST              'e'
             1394  END_FINALLY      
             1396  POP_EXCEPT       
             1398  JUMP_FORWARD       1402  'to 1402'
           1400_0  COME_FROM          1352  '1352'
             1400  END_FINALLY      
           1402_0  COME_FROM          1398  '1398'
           1402_1  COME_FROM          1344  '1344'

 L. 617      1402  LOAD_FAST                'cmdpkg'
             1404  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 72_0

    def connection_status_report(self, status, fd, data):
        logger.info('connect status changed, local host ip info : %s remote host ip info: %s, cur status: %s' % (self.socket_obj.get_local_host_ip(data), self.socket_obj.get_remote_host_ip(data), status))
        mode = 'wifi'
        if data != None:
            ip = self.socket_obj.get_local_host_ip(data)
            if ip == tools.get_ip_by_dev_name('wlan0'):
                mode = 'wifi'
            else:
                if ip == tools.get_ip_by_dev_name('rndis0'):
                    mode = 'rndis'
            logger.info('connect mode: %s' % mode)
        if status == 'connected':
            self.sdk_ctrl.sdk_on(mode)
        else:
            if status == 'disconnected':
                self.sdk_ctrl.sdk_off()

    def armor_event_push_callback(self, event):
        if len(event) == 0:
            return
        msg = 'armor event'
        if 'hit' in event.keys():
            msg += ' hit %d %d ;' % event['hit']
        self.send('event', msg)

    def applause_event_push_callback(self, event):
        if len(event) == 0:
            return
        msg = 'sound event'
        if 'applause' in event.keys():
            msg += ' applause %d ;' % event['applause']
        self.send('event', msg)

    def io_level_event_push_callback(self, event):
        if len(event) == 0:
            return
        msg = 'sensor_adapter event'
        if 'io_level' in event.keys():
            msg += ' io_level %d ;' % event['io_level']
        self.send('event', msg)

    def chassis_position_info_push_callback(self, x, y):
        pass

    def chassis_info_push_callback(self, info):
        if len(info) == 0:
            return
        msg = 'chassis push'
        if 'position' in info.keys():
            msg += ' position %.3f %.3f ;' % info['position']
        if 'attitude' in info.keys():
            msg += ' attitude %.3f %.3f %.3f ;' % info['attitude']
        if 'status' in info.keys():
            msg += ' status %d %d %d %d %d %d %d %d %d %d %d ;' % info['status']
        self.send('push', msg)

    def gimbal_info_push_callback(self, info):
        if len(info) == 0:
            return
        msg = 'gimbal push'
        if 'attitude' in info.keys():
            msg += ' attitude %.3f %.3f ;' % info['attitude']
        self.send('push', msg)

    def AI_info_push_callback(self, info):
        msg = 'AI push'
        while 'people' in info.keys():
            msg += ' people %d' % len(info['people'])
            for i in info['people']:
                msg += ' %.3f %.3f %.3f %.3f' % (i.pos.x, i.pos.y, i.size.w, i.size.h)

        while 'pose' in info.keys():
            msg += ' pose %d' % len(info['pose'])
            for i in info['pose']:
                msg += ' %d %.3f %.3f %.3f %.3f' % (i.info, i.pos.x, i.pos.y, i.size.w, i.size.h)
            else:
                while 'marker' in info.keys():
                    msg += ' marker %d' % len(info['marker'])
                    for i in info['marker']:
                        msg += ' %d %.3f %.3f %.3f %.3f' % (i.info, i.pos.x, i.pos.y, i.size.w, i.size.h)

        while 'line' in info.keys():
            msg += ' line %d' % int(len(info['line']) / 10)
            for i in info['line']:
                msg += ' %.3f %.3f %.3f %.3f' % (i.pos.x, i.pos.y, i.size.w, i.size.h)
            else:
                while 'robot' in info.keys():
                    msg += ' robot %d' % len(info['robot'])
                    for i in info['robot']:
                        msg += ' %.3f %.3f %.3f %.3f' % (i.pos.x, i.pos.y, i.size.w, i.size.h)

        self.send('push', msg)

    def gimbal_status_info_push_callback(self):
        pass

    def ack(self, fd, data, seq=None):
        msg = data
        if seq != None:
            msg += ' seq %s' % str(seq)
        if self.connection_obj:
            self.connection_obj.send(fd, msg)

    def req(self):
        pass

    def send(self, obj, data):
        fd = None
        if self.connection_obj == self.uart_obj:
            self.connection_obj.send(None, data)
        else:
            if obj == 'command':
                if self.connection_obj:
                    return self.connection_obj.send(self.command_socket_fd, data)
                return
            else:
                if obj == 'event':
                    logger.info(self.connection_socket_fd)
                    for user_fd in self.connection_socket_fd[self.event_socket_fd]:
                        if self.connection_obj:
                            self.connection_obj.send(user_fd, data)
                        return 0

                    if obj == 'push':
                        for ip in self.remote_host_ip:
                            if self.connection_obj:
                                self.connection_obj.send(self.push_socket_fd, data, (ip, PUSH_PORT))
                            return 0

                    return

    def recv(self):
        pass


class CommandPackage(object):

    def __init__(self):
        self.obj = None
        self.function = None
        self.param = None
        self.seq = None
        self.req_type = None