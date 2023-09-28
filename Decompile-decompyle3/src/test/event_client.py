# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: .\src\test\event_client.py
# Compiled at: 2022-01-12 15:45:07
# Size of source mod 2**32: 22591 bytes
import socket, select, threading, duss_event_msg, tools, rm_define, duml_cmdset, user_script_ctrl, sys, traceback, rm_log, time, random, string, rm_internal_command
logger = rm_log.dji_scratch_logger_get()
default_target_address = '\x00/duss/mb/0x900'
DUSS_EVENT_MSG_HEADER_LEN = 4

class EventAckIdentify(object):

    def __init__(self):
        self.valid = False
        self.identify = 0
        self.wait_ack_event = threading.Event()


class EventClient(object):
    DEFAULT_ROUTE_FILE = '/system/etc/dji.json'

    def __init__(self, host_id=rm_define.script_host_id):
        self.debug = False
        self.route_table = {}
        self.server_address = ('127.0.0.1', 32000)
        self.my_server_address = '../../file/server_address/' + ''.join((random.choice(string.ascii_lowercase) for i in range(5)))
        self.my_host_id = host_id
        self.wait_ack_list = {}
        self.wait_ack_mutex = threading.Lock()
        self.wait_ack_event_list = []
        self.cur_task_attri = {}
        self.finish = True
        self.script_state = user_script_ctrl.UserScriptCtrl()
        self.async_req_cb_list = {}
        self.async_ack_cb_list = {}
        self.event_process_mutex = threading.Lock()
        self.event_process_list = {}
        self.event_callback_list = {}
        self.event_notify_mutex = threading.Lock()
        self.event_notify_list = {}
        self.event_notify_not_register_dict = {}
        self.event_process_flag = False
        self.async_cb_mutex = threading.Lock()
        self.check_event_msg_invalid_callback = None
        self.already_finish_task_identify_set = set()
        self.heartbeat_time = time.time()
        self.heartbeat_thread = None
        self.task_push_cmdid_list = []
        for i in range(1, 9):
            ackIdentify = EventAckIdentify()
            self.wait_ack_event_list.append(ackIdentify)
        else:
            logger.info('WAIT ACK EVENT LIST LEN = ' + str(len(self.wait_ack_event_list)))
            self.socketfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.my_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                self.recv_thread = threading.Thread(target=(self._EventClient__recv_task))
                self.recv_thread.start()
            except Exception as e:
                try:
                    logger.fatal('EventClient: server error, message: ')
                    logger.fatal('TRACEBACK:\n' + traceback.format_exc())
                    sys.exit(-1)
                finally:
                    e = None
                    del e

    def stop(self):
        logger.info('EventClient: STOP')
        self.finish = True
        if self.my_server != None:
            self.my_server.close()
            self.my_server = None
        if self.recv_thread != None:
            self.recv_thread.join(3)
            logger.info('EventClient: recv thread alive = ' + str(self.recv_thread.isAlive()))
            self.recv_thread = None
        self.heartbeat_thread = None
        if self.socketfd != None:
            self.socketfd.close()
            self.socketfd = None
        logger.info('EventClient host id = ' + str(self.my_host_id) + ' Exit!!!')

    def finished(self):
        return self.finish

    def __recv_task--- This code section failed: ---

 L. 105         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              info
                4  LOAD_STR                 'START RECVING TASK...'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 106        10  LOAD_CONST               False
               12  LOAD_FAST                'self'
               14  STORE_ATTR               finish

 L. 107        16  LOAD_GLOBAL              tools
               18  LOAD_METHOD              is_windows_system
               20  CALL_METHOD_0         0  ''
               22  POP_JUMP_IF_FALSE    50  'to 50'

 L. 108        24  LOAD_STR                 'first message'
               26  STORE_FAST               'firstMessage'

 L. 109        28  LOAD_FAST                'self'
               30  LOAD_ATTR                my_server
               32  LOAD_METHOD              sendto
               34  LOAD_FAST                'firstMessage'
               36  LOAD_METHOD              encode
               38  LOAD_STR                 'utf-8'
               40  CALL_METHOD_1         1  ''
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                server_address
               46  CALL_METHOD_2         2  ''
               48  POP_TOP          
             50_0  COME_FROM           962  '962'
             50_1  COME_FROM           958  '958'
             50_2  COME_FROM           910  '910'
             50_3  COME_FROM           486  '486'
             50_4  COME_FROM           224  '224'
             50_5  COME_FROM           202  '202'
             50_6  COME_FROM           124  '124'
             50_7  COME_FROM            22  '22'

 L. 111        50  LOAD_FAST                'self'
               52  LOAD_ATTR                finish
               54  LOAD_CONST               False
               56  COMPARE_OP               ==
            58_60  POP_JUMP_IF_FALSE   964  'to 964'

 L. 112     62_64  SETUP_FINALLY       912  'to 912'

 L. 113        66  LOAD_FAST                'self'
               68  LOAD_ATTR                my_server
               70  LOAD_METHOD              recvfrom
               72  LOAD_CONST               1280
               74  CALL_METHOD_1         1  ''
               76  UNPACK_SEQUENCE_2     2 
               78  STORE_FAST               'recv_buff'
               80  STORE_FAST               'host'

 L. 115        82  LOAD_FAST                'self'
               84  LOAD_ATTR                finish
               86  POP_JUMP_IF_FALSE   104  'to 104'

 L. 116        88  LOAD_GLOBAL              logger
               90  LOAD_METHOD              info
               92  LOAD_STR                 'EventClient: NEED QUIT!'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          

 L. 117        98  POP_BLOCK        
          100_102  BREAK_LOOP          964  'to 964'
            104_0  COME_FROM            86  '86'

 L. 118       104  LOAD_FAST                'recv_buff'
              106  LOAD_CONST               None
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   126  'to 126'

 L. 119       112  LOAD_GLOBAL              logger
              114  LOAD_METHOD              fatal
              116  LOAD_STR                 'FATAL ERROR RECV BUFF = NONE!!!'
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          

 L. 120       122  POP_BLOCK        
              124  JUMP_LOOP            50  'to 50'
            126_0  COME_FROM           110  '110'

 L. 123       126  LOAD_GLOBAL              rm_internal_command
              128  LOAD_METHOD              is_internal_command
              130  LOAD_FAST                'recv_buff'
              132  CALL_METHOD_1         1  ''
              134  POP_JUMP_IF_FALSE   204  'to 204'

 L. 124       136  LOAD_FAST                'recv_buff'
              138  LOAD_CONST               2
              140  BINARY_SUBSCR    
              142  STORE_FAST               'cmd'

 L. 125       144  LOAD_FAST                'cmd'
              146  LOAD_GLOBAL              rm_internal_command
              148  LOAD_ATTR                CMD_PING
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE   166  'to 166'

 L. 127       154  LOAD_GLOBAL              time
              156  LOAD_METHOD              time
              158  CALL_METHOD_0         0  ''
              160  LOAD_FAST                'self'
              162  STORE_ATTR               heartbeat_time
              164  JUMP_FORWARD        200  'to 200'
            166_0  COME_FROM           152  '152'

 L. 128       166  LOAD_FAST                'cmd'
              168  LOAD_GLOBAL              rm_internal_command
              170  LOAD_ATTR                CMD_EXIT
              172  COMPARE_OP               ==
              174  POP_JUMP_IF_FALSE   200  'to 200'

 L. 129       176  LOAD_GLOBAL              logger
              178  LOAD_METHOD              info
              180  LOAD_STR                 'Recv CMD_EXIT'
              182  CALL_METHOD_1         1  ''
              184  POP_TOP          

 L. 130       186  LOAD_CONST               True
              188  LOAD_FAST                'self'
              190  STORE_ATTR               finish

 L. 131       192  LOAD_FAST                'self'
              194  LOAD_METHOD              stop
              196  CALL_METHOD_0         0  ''
              198  POP_TOP          
            200_0  COME_FROM           174  '174'
            200_1  COME_FROM           164  '164'

 L. 132       200  POP_BLOCK        
              202  JUMP_LOOP            50  'to 50'
            204_0  COME_FROM           134  '134'

 L. 135       204  LOAD_GLOBAL              duss_event_msg
              206  LOAD_METHOD              unpack
              208  LOAD_FAST                'recv_buff'
              210  CALL_METHOD_1         1  ''
              212  STORE_FAST               'msg'

 L. 137       214  LOAD_FAST                'msg'
              216  LOAD_CONST               None
              218  COMPARE_OP               ==
              220  POP_JUMP_IF_FALSE   226  'to 226'

 L. 138       222  POP_BLOCK        
              224  JUMP_LOOP            50  'to 50'
            226_0  COME_FROM           220  '220'

 L. 140       226  LOAD_STR                 '{:0>2d}'
              228  LOAD_METHOD              format
              230  LOAD_FAST                'msg'
              232  LOAD_STR                 'send_id'
              234  BINARY_SUBSCR    
              236  CALL_METHOD_1         1  ''
              238  LOAD_STR                 '{:0>2d}'
              240  LOAD_METHOD              format
              242  LOAD_FAST                'msg'
              244  LOAD_STR                 'send_module_id'
              246  BINARY_SUBSCR    
              248  CALL_METHOD_1         1  ''
              250  BINARY_ADD       
              252  STORE_FAST               'str_sender'

 L. 141       254  LOAD_STR                 '{:0>2d}'
              256  LOAD_METHOD              format
              258  LOAD_FAST                'msg'
              260  LOAD_STR                 'recv_id'
              262  BINARY_SUBSCR    
              264  CALL_METHOD_1         1  ''
              266  LOAD_STR                 '{:0>2d}'
              268  LOAD_METHOD              format
              270  LOAD_FAST                'msg'
              272  LOAD_STR                 'recv_module_id'
              274  BINARY_SUBSCR    
              276  CALL_METHOD_1         1  ''
              278  BINARY_ADD       
              280  STORE_FAST               'str_receiver'

 L. 144       282  LOAD_FAST                'msg'
              284  LOAD_STR                 'cmd_set'
              286  BINARY_SUBSCR    
              288  LOAD_CONST               63
              290  COMPARE_OP               !=
          292_294  POP_JUMP_IF_FALSE   372  'to 372'
              296  LOAD_FAST                'msg'
              298  LOAD_STR                 'cmd_id'
              300  BINARY_SUBSCR    
              302  LOAD_CONST               172
              304  COMPARE_OP               !=
          306_308  POP_JUMP_IF_FALSE   372  'to 372'

 L. 145       310  LOAD_GLOBAL              logger
              312  LOAD_METHOD              info
              314  LOAD_STR                 'RecvCommand: CmdSet = '
              316  LOAD_GLOBAL              str
              318  LOAD_GLOBAL              hex
              320  LOAD_FAST                'msg'
              322  LOAD_STR                 'cmd_set'
              324  BINARY_SUBSCR    
              326  CALL_FUNCTION_1       1  ''
              328  CALL_FUNCTION_1       1  ''
              330  BINARY_ADD       
              332  LOAD_STR                 ', CmdId = '
              334  BINARY_ADD       
              336  LOAD_GLOBAL              str
              338  LOAD_GLOBAL              hex
              340  LOAD_FAST                'msg'
              342  LOAD_STR                 'cmd_id'
              344  BINARY_SUBSCR    
              346  CALL_FUNCTION_1       1  ''
              348  CALL_FUNCTION_1       1  ''
              350  BINARY_ADD       
              352  LOAD_STR                 ', Sender = '
              354  BINARY_ADD       
              356  LOAD_FAST                'str_sender'
              358  BINARY_ADD       
              360  LOAD_STR                 ', Recveiver = '
              362  BINARY_ADD       
              364  LOAD_FAST                'str_receiver'
              366  BINARY_ADD       
              368  CALL_METHOD_1         1  ''
              370  POP_TOP          
            372_0  COME_FROM           306  '306'
            372_1  COME_FROM           292  '292'

 L. 148       372  LOAD_FAST                'msg'
              374  LOAD_STR                 'cmd_set'
              376  BINARY_SUBSCR    
              378  LOAD_GLOBAL              duml_cmdset
              380  LOAD_ATTR                DUSS_MB_CMDSET_RM
              382  COMPARE_OP               ==
          384_386  POP_JUMP_IF_TRUE    404  'to 404'
              388  LOAD_FAST                'msg'
              390  LOAD_STR                 'cmd_set'
              392  BINARY_SUBSCR    
              394  LOAD_GLOBAL              duml_cmdset
              396  LOAD_ATTR                DUSS_MB_CMDSET_EDU_PLATFORM
              398  COMPARE_OP               ==
          400_402  POP_JUMP_IF_FALSE   488  'to 488'
            404_0  COME_FROM           384  '384'

 L. 149       404  LOAD_FAST                'msg'
              406  LOAD_STR                 'cmd_id'
              408  BINARY_SUBSCR    
              410  LOAD_FAST                'self'
              412  LOAD_ATTR                task_push_cmdid_list
              414  COMPARE_OP               in
          416_418  POP_JUMP_IF_FALSE   488  'to 488'

 L. 150       420  LOAD_FAST                'msg'
              422  LOAD_STR                 'data'
              424  BINARY_SUBSCR    
              426  LOAD_CONST               0
              428  BINARY_SUBSCR    
              430  LOAD_FAST                'msg'
              432  LOAD_STR                 'task_id'
              434  STORE_SUBSCR     

 L. 151       436  LOAD_GLOBAL              str
              438  LOAD_FAST                'msg'
              440  LOAD_STR                 'cmd_set'
              442  BINARY_SUBSCR    
              444  CALL_FUNCTION_1       1  ''
              446  LOAD_GLOBAL              str
              448  LOAD_FAST                'msg'
              450  LOAD_STR                 'cmd_id'
              452  BINARY_SUBSCR    
              454  CALL_FUNCTION_1       1  ''
              456  BINARY_ADD       
              458  LOAD_GLOBAL              str
              460  LOAD_FAST                'msg'
              462  LOAD_STR                 'task_id'
              464  BINARY_SUBSCR    
              466  CALL_FUNCTION_1       1  ''
              468  BINARY_ADD       
              470  STORE_FAST               'task_identify'

 L. 152       472  LOAD_FAST                'self'
              474  LOAD_METHOD              task_sync_process
              476  LOAD_FAST                'task_identify'
              478  LOAD_FAST                'msg'
              480  CALL_METHOD_2         2  ''
              482  POP_TOP          

 L. 153       484  POP_BLOCK        
              486  JUMP_LOOP            50  'to 50'
            488_0  COME_FROM           416  '416'
            488_1  COME_FROM           400  '400'

 L. 156       488  LOAD_FAST                'msg'
              490  LOAD_STR                 'ack'
              492  BINARY_SUBSCR    
              494  LOAD_CONST               True
              496  COMPARE_OP               ==
          498_500  POP_JUMP_IF_FALSE   744  'to 744'

 L. 157       502  LOAD_GLOBAL              str
              504  LOAD_FAST                'msg'
              506  LOAD_STR                 'sender'
              508  BINARY_SUBSCR    
              510  CALL_FUNCTION_1       1  ''
              512  LOAD_GLOBAL              str
              514  LOAD_FAST                'msg'
              516  LOAD_STR                 'cmd_set'
              518  BINARY_SUBSCR    
              520  CALL_FUNCTION_1       1  ''
              522  BINARY_ADD       
              524  LOAD_GLOBAL              str
              526  LOAD_FAST                'msg'
              528  LOAD_STR                 'cmd_id'
              530  BINARY_SUBSCR    
              532  CALL_FUNCTION_1       1  ''
              534  BINARY_ADD       
              536  LOAD_GLOBAL              str
              538  LOAD_FAST                'msg'
              540  LOAD_STR                 'seq_num'
              542  BINARY_SUBSCR    
              544  CALL_FUNCTION_1       1  ''
              546  BINARY_ADD       
              548  STORE_FAST               'identify'

 L. 159       550  LOAD_FAST                'self'
              552  LOAD_ATTR                wait_ack_mutex
              554  LOAD_METHOD              acquire
              556  CALL_METHOD_0         0  ''
              558  POP_TOP          

 L. 160       560  LOAD_FAST                'identify'
              562  LOAD_FAST                'self'
              564  LOAD_ATTR                wait_ack_list
              566  LOAD_METHOD              keys
              568  CALL_METHOD_0         0  ''
              570  COMPARE_OP               in
          572_574  POP_JUMP_IF_FALSE   660  'to 660'

 L. 161       576  LOAD_GLOBAL              range
              578  LOAD_CONST               0
              580  LOAD_GLOBAL              len
              582  LOAD_FAST                'self'
              584  LOAD_ATTR                wait_ack_event_list
              586  CALL_FUNCTION_1       1  ''
              588  CALL_FUNCTION_2       2  ''
              590  GET_ITER         
            592_0  COME_FROM           654  '654'
            592_1  COME_FROM           624  '624'
            592_2  COME_FROM           606  '606'
              592  FOR_ITER            658  'to 658'
              594  STORE_FAST               'j'

 L. 162       596  LOAD_FAST                'self'
              598  LOAD_ATTR                wait_ack_event_list
              600  LOAD_FAST                'j'
              602  BINARY_SUBSCR    
              604  LOAD_ATTR                valid
          606_608  POP_JUMP_IF_FALSE_LOOP   592  'to 592'
              610  LOAD_FAST                'self'
              612  LOAD_ATTR                wait_ack_event_list
              614  LOAD_FAST                'j'
              616  BINARY_SUBSCR    
              618  LOAD_ATTR                identify
              620  LOAD_FAST                'identify'
              622  COMPARE_OP               ==
          624_626  POP_JUMP_IF_FALSE_LOOP   592  'to 592'

 L. 163       628  LOAD_FAST                'msg'
              630  LOAD_FAST                'self'
              632  LOAD_ATTR                wait_ack_list
              634  LOAD_FAST                'identify'
              636  STORE_SUBSCR     

 L. 164       638  LOAD_FAST                'self'
              640  LOAD_ATTR                wait_ack_event_list
              642  LOAD_FAST                'j'
              644  BINARY_SUBSCR    
              646  LOAD_ATTR                wait_ack_event
              648  LOAD_METHOD              set
              650  CALL_METHOD_0         0  ''
              652  POP_TOP          
          654_656  JUMP_LOOP           592  'to 592'
            658_0  COME_FROM           592  '592'
              658  JUMP_FORWARD        660  'to 660'
            660_0  COME_FROM           658  '658'
            660_1  COME_FROM           572  '572'

 L. 168       660  LOAD_FAST                'self'
              662  LOAD_ATTR                wait_ack_mutex
              664  LOAD_METHOD              release
              666  CALL_METHOD_0         0  ''
              668  POP_TOP          

 L. 171       670  LOAD_FAST                'msg'
              672  LOAD_STR                 'cmd_set'
              674  BINARY_SUBSCR    
              676  LOAD_CONST               8
              678  BINARY_LSHIFT    
              680  LOAD_FAST                'msg'
              682  LOAD_STR                 'cmd_id'
              684  BINARY_SUBSCR    
              686  BINARY_OR        
              688  STORE_FAST               'cmd_set_id'

 L. 172       690  LOAD_FAST                'self'
              692  LOAD_ATTR                async_cb_mutex
              694  LOAD_METHOD              acquire
              696  CALL_METHOD_0         0  ''
              698  POP_TOP          

 L. 173       700  LOAD_FAST                'cmd_set_id'
              702  LOAD_FAST                'self'
              704  LOAD_ATTR                async_ack_cb_list
              706  LOAD_METHOD              keys
              708  CALL_METHOD_0         0  ''
              710  COMPARE_OP               in
          712_714  POP_JUMP_IF_FALSE   732  'to 732'

 L. 175       716  LOAD_FAST                'self'
              718  LOAD_ATTR                async_ack_cb_list
              720  LOAD_FAST                'cmd_set_id'
              722  BINARY_SUBSCR    
              724  LOAD_FAST                'self'
              726  LOAD_FAST                'msg'
              728  CALL_FUNCTION_2       2  ''
              730  POP_TOP          
            732_0  COME_FROM           712  '712'

 L. 176       732  LOAD_FAST                'self'
              734  LOAD_ATTR                async_cb_mutex
              736  LOAD_METHOD              release
              738  CALL_METHOD_0         0  ''
              740  POP_TOP          
              742  JUMP_FORWARD        908  'to 908'
            744_0  COME_FROM           498  '498'

 L. 179       744  LOAD_FAST                'msg'
              746  LOAD_STR                 'cmd_set'
              748  BINARY_SUBSCR    
              750  LOAD_CONST               8
              752  BINARY_LSHIFT    
              754  LOAD_FAST                'msg'
              756  LOAD_STR                 'cmd_id'
              758  BINARY_SUBSCR    
              760  BINARY_OR        
              762  STORE_FAST               'cmd_set_id'

 L. 182       764  LOAD_FAST                'self'
              766  LOAD_ATTR                async_cb_mutex
              768  LOAD_METHOD              acquire
              770  CALL_METHOD_0         0  ''
              772  POP_TOP          

 L. 183       774  LOAD_FAST                'cmd_set_id'
              776  LOAD_FAST                'self'
              778  LOAD_ATTR                async_req_cb_list
              780  LOAD_METHOD              keys
              782  CALL_METHOD_0         0  ''
              784  COMPARE_OP               in
          786_788  POP_JUMP_IF_FALSE   820  'to 820'

 L. 185       790  LOAD_FAST                'self'
              792  LOAD_ATTR                async_req_cb_list
              794  LOAD_FAST                'cmd_set_id'
              796  BINARY_SUBSCR    
              798  GET_ITER         
            800_0  COME_FROM           814  '814'
              800  FOR_ITER            818  'to 818'
              802  STORE_FAST               'cb'

 L. 186       804  LOAD_FAST                'cb'
              806  LOAD_FAST                'self'
              808  LOAD_FAST                'msg'
              810  CALL_FUNCTION_2       2  ''
              812  POP_TOP          
          814_816  JUMP_LOOP           800  'to 800'
            818_0  COME_FROM           800  '800'
              818  JUMP_FORWARD        898  'to 898'
            820_0  COME_FROM           786  '786'

 L. 188       820  LOAD_GLOBAL              logger
              822  LOAD_METHOD              warn
              824  LOAD_STR                 'UNSUPPORT MSG, SENDER = '
              826  LOAD_GLOBAL              str
              828  LOAD_FAST                'msg'
              830  LOAD_STR                 'sender'
              832  BINARY_SUBSCR    
              834  CALL_FUNCTION_1       1  ''
              836  BINARY_ADD       
              838  LOAD_STR                 ', RECEIVER = '
              840  BINARY_ADD       
              842  LOAD_GLOBAL              str
              844  LOAD_FAST                'msg'
              846  LOAD_STR                 'receiver'
              848  BINARY_SUBSCR    
              850  CALL_FUNCTION_1       1  ''
              852  BINARY_ADD       
              854  LOAD_STR                 ', CMD SET = '
              856  BINARY_ADD       
              858  LOAD_GLOBAL              str
              860  LOAD_GLOBAL              hex
              862  LOAD_FAST                'msg'
              864  LOAD_STR                 'cmd_set'
              866  BINARY_SUBSCR    
              868  CALL_FUNCTION_1       1  ''
              870  CALL_FUNCTION_1       1  ''
              872  BINARY_ADD       
              874  LOAD_STR                 ', CMD ID = '
              876  BINARY_ADD       
              878  LOAD_GLOBAL              str
              880  LOAD_GLOBAL              hex
              882  LOAD_FAST                'msg'
              884  LOAD_STR                 'cmd_id'
              886  BINARY_SUBSCR    
              888  CALL_FUNCTION_1       1  ''
              890  CALL_FUNCTION_1       1  ''
              892  BINARY_ADD       
              894  CALL_METHOD_1         1  ''
              896  POP_TOP          
            898_0  COME_FROM           818  '818'

 L. 189       898  LOAD_FAST                'self'
              900  LOAD_ATTR                async_cb_mutex
              902  LOAD_METHOD              release
              904  CALL_METHOD_0         0  ''
              906  POP_TOP          
            908_0  COME_FROM           742  '742'
              908  POP_BLOCK        
              910  JUMP_LOOP            50  'to 50'
            912_0  COME_FROM_FINALLY    62  '62'

 L. 190       912  DUP_TOP          
              914  LOAD_GLOBAL              Exception
              916  COMPARE_OP               exception-match
          918_920  POP_JUMP_IF_FALSE   960  'to 960'
              922  POP_TOP          
              924  STORE_FAST               'e'
              926  POP_TOP          
              928  SETUP_FINALLY       948  'to 948'

 L. 191       930  LOAD_GLOBAL              logger
              932  LOAD_METHOD              info
              934  LOAD_STR                 'Recv Exception %s'
              936  LOAD_FAST                'e'
              938  BINARY_MODULO    
              940  CALL_METHOD_1         1  ''
              942  POP_TOP          
              944  POP_BLOCK        
              946  BEGIN_FINALLY    
            948_0  COME_FROM_FINALLY   928  '928'
              948  LOAD_CONST               None
              950  STORE_FAST               'e'
              952  DELETE_FAST              'e'
              954  END_FINALLY      
              956  POP_EXCEPT       
              958  JUMP_LOOP            50  'to 50'
            960_0  COME_FROM           918  '918'
              960  END_FINALLY      
              962  JUMP_LOOP            50  'to 50'
            964_0  COME_FROM           100  '100'
            964_1  COME_FROM            58  '58'

 L. 193       964  LOAD_GLOBAL              logger
              966  LOAD_METHOD              info
              968  LOAD_STR                 'RECV TASK FINISH!!!'
              970  CALL_METHOD_1         1  ''
              972  POP_TOP          

Parse error at or near `JUMP_LOOP' instruction at offset 124

    def send(self, data, target_address):
        try:
            self.my_server.sendto(data, self.server_address)
        except:
            return duml_cmdset.DUSS_MB_RET_ACK

    def start_monitor(self):
        if self.heartbeat_thread == None:
            self.heartbeat_thread = threading.Thread(target=(self._EventClient__heartbeat_monitor_task))
            self.heartbeat_thread.start()

    def __heartbeat_monitor_task--- This code section failed: ---

 L. 209         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              info
                4  LOAD_STR                 'Heartbeat Monitor Enter'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          
             10_0  COME_FROM            72  '72'
             10_1  COME_FROM            50  '50'

 L. 210        10  LOAD_FAST                'self'
               12  LOAD_ATTR                finish
               14  LOAD_CONST               False
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    74  'to 74'

 L. 211        20  LOAD_GLOBAL              time
               22  LOAD_METHOD              sleep
               24  LOAD_CONST               1
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 212        30  LOAD_GLOBAL              time
               32  LOAD_METHOD              time
               34  CALL_METHOD_0         0  ''
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                heartbeat_time
               40  BINARY_SUBTRACT  
               42  STORE_FAST               'elapsed'

 L. 213        44  LOAD_FAST                'elapsed'
               46  LOAD_CONST               2
               48  COMPARE_OP               >=
               50  POP_JUMP_IF_FALSE_LOOP    10  'to 10'

 L. 214        52  LOAD_GLOBAL              logger
               54  LOAD_METHOD              info
               56  LOAD_STR                 'Heartbeat TIMEOUT'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          

 L. 215        62  LOAD_FAST                'self'
               64  LOAD_METHOD              stop
               66  CALL_METHOD_0         0  ''
               68  POP_TOP          

 L. 216        70  JUMP_FORWARD         74  'to 74'
               72  JUMP_LOOP            10  'to 10'
             74_0  COME_FROM            70  '70'
             74_1  COME_FROM            18  '18'

Parse error at or near `JUMP_LOOP' instruction at offset 72

    def send2myself(self, data):
        try:
            self.socketfd.setblocking(0)
            self.socketfd.sendto(data.encode('utf-8'), '\x00/duss/mb/' + str(hex(self.my_host_id)))
        except Exception as e:
            try:
                logger.error('EVENT_CLIENT: send2myself() error, message: ')
                logger.error(traceback.logger.info_exc())
            finally:
                e = None
                del e

    def is_wait(self):
        return False

    def async_req_register(self, cmd_set_id, callback):
        logger.info('ASYNC REGISTER CMD_SETID = ' + str(hex(cmd_set_id)))
        self.async_cb_mutex.acquire()
        if cmd_set_id not in self.async_req_cb_list.keys():
            self.async_req_cb_list[cmd_set_id] = []
        if cmd_set_id not in self.async_req_cb_list[cmd_set_id]:
            self.async_req_cb_list[cmd_set_id].append(callback)
        self.async_cb_mutex.release()

    def async_req_unregister(self, cmd_set_id, cb=None):
        logger.info('ASYNC UNREGISTER CMD_SETID = ' + str(cmd_set_id))
        self.async_cb_mutex.acquire()
        if cb != None:
            if not cmd_set_id in self.async_req_cb_list.keys() or cb in self.async_req_cb_list[cmd_set_id]:
                self.self.async_req_cb_list[cmd_set_id].remove(cb)
        else:
            if cmd_set_id in self.async_req_cb_list.keys():
                self.async_req_cb_list.pop(cmd_set_id)
        self.async_cb_mutex.release()

    def async_ack_register(self, cmd_set_id, callback):
        self.async_cb_mutex.acquire()
        if cmd_set_id in self.async_req_cb_list.keys():
            self.async_ack_cb_list[cmd_set_id] = callback
        self.async_cb_mutex.release()

    def async_ack_unregister(self, cmd_set_id, callback):
        self.async_cb_mutex.acquire()
        if cmd_set_id in self.async_ack_cb_list.keys():
            self.async_ack_cb_list.pop(cmd_set_id)
        self.async_cb_mutex.release()

    def event_notify_register(self, event_name, robot_event):
        self.event_notify_mutex.acquire()
        if event_name in self.event_notify_not_register_dict.keys() and time.time() - self.event_notify_not_register_dict[event_name] < 5:
            robot_event.notify_for_task_complete()
            self.event_notify_not_register_dict.pop(event_name)
        else:
            self.event_notify_list[event_name] = robot_event
        self.event_notify_mutex.release()

    def event_notify(self, event_name):
        self.event_notify_mutex.acquire()
        if event_name in self.event_notify_list.keys():
            robot_event = self.event_notify_list[event_name]
            robot_event.notify_for_task_complete()
        else:
            self.event_notify_not_register_dict[event_name] = time.time()
        self.event_notify_mutex.release()

    def event_watchdog_set(self, event_name):
        self.event_notify_mutex.acquire()
        if event_name in self.event_notify_list.keys():
            robot_event = self.event_notify_list[event_name]
            robot_event.watchdog_set()
        self.event_notify_mutex.release()

    def event_notify_unregister(self, event_name):
        self.event_notify_mutex.acquire()
        if event_name in self.event_notify_list.keys():
            self.event_notify_list.pop(event_name)
        self.event_notify_mutex.release()

    def event_callback_register(self, event_name, callback):
        self.event_process_mutex.acquire()
        self.event_callback_list[event_name] = callback
        self.event_process_list[event_name] = {'callback':None,  'callback_data':None}
        self.event_process_mutex.release()

    def event_come_to_process(self, event_name, callback_data=None):
        self.event_process_mutex.acquire()
        if event_name in self.event_callback_list.keys():
            self.event_process_list[event_name]['callback'] = self.event_callback_list[event_name]
            self.event_process_list[event_name]['callback_data'] = callback_data
        else:
            logger.error('EVENTCTRL: NO CB REGISTER, FUNC IS %s', event_name)
        self.event_process_mutex.release()

    def wait_for_event_process(self, func_before_event):
        callback_list = []
        self.event_process_mutex.acquire()
        for event_name, callback_items in self.event_process_list.items():
            if callback_items['callback'] != None:
                if callback_items['callback'].__name__ != 'dummy_callback':
                    callback_list.append(callback_items)
                    self.event_process_list[event_name] = {'callback':None,  'callback_data':None}
        else:
            self.event_process_mutex.release()
            if len(callback_list) <= 0 or self.event_process_flag:
                return False
            if func_before_event != None:
                func_before_event()
            self.event_process_flag = True
            for item in callback_list:
                func = item['callback']
                data = item['callback_data']
                func(data)
            else:
                self.event_process_flag = False
                return True

    def ack_register_identify(self, event_msg):
        self.wait_ack_mutex.acquire()
        identify = str(event_msg.receiver) + str(event_msg.cmd_set) + str(event_msg.cmd_id) + str(event_msg.seq_num)
        self.wait_ack_list[identify] = True
        self.wait_ack_mutex.release()
        return identify

    def ack_unregister_identify(self, identify):
        resp = {}
        self.wait_ack_mutex.acquire()
        if identify in self.wait_ack_list.keys():
            resp = self.wait_ack_list.pop(identify)
        self.wait_ack_mutex.release()
        return resp

    def send_msg--- This code section failed: ---

 L. 353         0  SETUP_FINALLY       114  'to 114'

 L. 354         2  LOAD_FAST                'self'
                4  LOAD_ATTR                debug
                6  POP_JUMP_IF_FALSE    24  'to 24'

 L. 355         8  LOAD_GLOBAL              logger
               10  LOAD_METHOD              info
               12  LOAD_GLOBAL              str
               14  LOAD_FAST                'event_msg'
               16  LOAD_ATTR                data
               18  CALL_FUNCTION_1       1  ''
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          
             24_0  COME_FROM             6  '6'

 L. 357        24  LOAD_GLOBAL              default_target_address
               26  STORE_FAST               'target_address'

 L. 358        28  LOAD_FAST                'event_msg'
               30  LOAD_ATTR                receiver
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                route_table
               36  LOAD_METHOD              keys
               38  CALL_METHOD_0         0  ''
               40  COMPARE_OP               in
               42  POP_JUMP_IF_FALSE    60  'to 60'

 L. 359        44  LOAD_FAST                'self'
               46  LOAD_ATTR                route_table
               48  LOAD_FAST                'event_msg'
               50  LOAD_ATTR                receiver
               52  BINARY_SUBSCR    
               54  LOAD_STR                 'target_address'
               56  BINARY_SUBSCR    
               58  STORE_FAST               'target_address'
             60_0  COME_FROM            42  '42'

 L. 360        60  LOAD_FAST                'event_msg'
               62  LOAD_ATTR                cmd_type
               64  LOAD_GLOBAL              duml_cmdset
               66  LOAD_ATTR                NEED_ACK_TYPE
               68  BINARY_AND       
               70  POP_JUMP_IF_FALSE    90  'to 90'

 L. 361        72  LOAD_FAST                'event_msg'
               74  DUP_TOP          
               76  LOAD_ATTR                cmd_type
               78  LOAD_GLOBAL              duml_cmdset
               80  LOAD_ATTR                NO_ACK_TYPE
               82  UNARY_INVERT     
               84  INPLACE_AND      
               86  ROT_TWO          
               88  STORE_ATTR               cmd_type
             90_0  COME_FROM            70  '70'

 L. 362        90  LOAD_FAST                'event_msg'
               92  LOAD_METHOD              pack
               94  CALL_METHOD_0         0  ''
               96  STORE_FAST               'data'

 L. 363        98  LOAD_FAST                'self'
              100  LOAD_METHOD              send
              102  LOAD_FAST                'data'
              104  LOAD_FAST                'target_address'
              106  CALL_METHOD_2         2  ''
              108  POP_TOP          
              110  POP_BLOCK        
              112  JUMP_FORWARD        176  'to 176'
            114_0  COME_FROM_FINALLY     0  '0'

 L. 364       114  DUP_TOP          
              116  LOAD_GLOBAL              Exception
              118  COMPARE_OP               exception-match
              120  POP_JUMP_IF_FALSE   174  'to 174'
              122  POP_TOP          
              124  STORE_FAST               'e'
              126  POP_TOP          
              128  SETUP_FINALLY       162  'to 162'

 L. 365       130  LOAD_GLOBAL              logger
              132  LOAD_METHOD              fatal
              134  LOAD_STR                 'Exception in send_msg, '
              136  LOAD_GLOBAL              traceback
              138  LOAD_METHOD              format_exc
              140  CALL_METHOD_0         0  ''
              142  BINARY_ADD       
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          

 L. 366       148  LOAD_GLOBAL              rm_define
              150  LOAD_ATTR                DUSS_ERR_FAILURE
              152  ROT_FOUR         
              154  POP_BLOCK        
              156  POP_EXCEPT       
              158  CALL_FINALLY        162  'to 162'
              160  RETURN_VALUE     
            162_0  COME_FROM           158  '158'
            162_1  COME_FROM_FINALLY   128  '128'
              162  LOAD_CONST               None
              164  STORE_FAST               'e'
              166  DELETE_FAST              'e'
              168  END_FINALLY      
              170  POP_EXCEPT       
              172  JUMP_FORWARD        176  'to 176'
            174_0  COME_FROM           120  '120'
              174  END_FINALLY      
            176_0  COME_FROM           172  '172'
            176_1  COME_FROM           112  '112'

 L. 367       176  LOAD_GLOBAL              rm_define
              178  LOAD_ATTR                DUSS_SUCCESS
              180  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 154

    def send_sync(self, event_msg, time_out=duml_cmdset.MSG_DEFAULT_TIMEOUT):
        duss_result = rm_define.DUSS_SUCCESS
        check_result, invalid_code = self.check_event_msg_invalid(event_msg)
        if check_result == True:
            logger.warn('RECEIVER %d, MODULE ID %d, OFFLINE OR ERROR %s' % (event_msg.receiver, event_msg.module_id, invalid_code))
            return (
             invalid_code, None)
            while event_msg.cmd_type & duml_cmdset.NEED_ACK_TYPE:
                identify = self.ack_register_identify(event_msg)
                j = 0
                for j in range(0, len(self.wait_ack_event_list)):
                    if not self.wait_ack_event_list[j].valid:
                        break

            self.wait_ack_event_list[j].valid = True
            self.wait_ack_event_list[j].identify = identify
            self.wait_ack_event_list[j].wait_ack_event.clear()
            self.send_msg(event_msg)
            self.wait_ack_event_list[j].wait_ack_event.wait(time_out)
            if not self.wait_ack_event_list[j].wait_ack_event.isSet():
                duss_result = rm_define.DUSS_ERR_TIMEOUT
                logger.warn('TIMEOUT: SENDER = ' + str(event_msg.sender) + ', RECEIVER = ' + str(event_msg.receiver) + ', CMDSET = ' + str(hex(event_msg.cmd_set)) + ', CMDID = ' + str(hex(event_msg.cmd_id)))
            self.wait_ack_event_list[j].valid = False
            resp = self.ack_unregister_identify(identify)
            return (
             duss_result, resp)
        self.send_msg(event_msg)
        return (
         duss_result, None)

    def send_task_async(self, event_msg, event_task, time_out=duml_cmdset.MSG_DEFAULT_TIMEOUT):
        duss_result, identify, resp = self.send_task_async_ret_resp(event_msg, event_task, time_out)
        return (
         duss_result, identify)

    def send_task_async_ret_resp(self, event_msg, event_task, time_out=duml_cmdset.MSG_DEFAULT_TIMEOUT):
        if event_task['cmd_id'] not in self.task_push_cmdid_list:
            self.task_push_cmdid_list.append(event_task['cmd_id'])
        identify = str(event_task['cmd_set']) + str(event_task['cmd_id']) + str(event_task['task_id'])
        duss_result, resp = self.send_sync(event_msg, time_out)
        if duss_result != rm_define.DUSS_SUCCESS:
            logger.error('EVENT: send task %s, error code = %d' % (identify, duss_result))
            return (
             duss_result, identify, resp)
        if resp['data'][0] == duml_cmdset.DUSS_MB_RET_OK:
            if resp['data'][1] == 0:
                logger.info('TASK ID = ' + str(event_task['task_id']) + ' ACCEPTED')
                duss_result = rm_define.DUSS_SUCCESS
            else:
                if resp['data'][1] == 1:
                    logger.info('TASK ID = ' + str(event_task['task_id']) + ' REJECTED')
                    duss_result = rm_define.DUSS_TASK_REJECTED
                else:
                    if resp['data'][1] == 2:
                        logger.info('TASK ID = ' + str(event_task['task_id']) + ' ALREADY FINISH.')
                        self.already_finish_task_identify_set.add(identify)
                        duss_result = rm_define.DUSS_TASK_FINISHED
                    else:
                        logger.warn('UNSUPPORT TASK RESULT')
                        duss_result = rm_define.DUSS_ERR_FAILURE
        else:
            logger.error('RETURN CODE ERROR')
            duss_result = rm_define.DUSS_ERR_FAILURE
        return (duss_result, identify, resp)

    def task_sync_process(self, identify, task_push_msg):
        task_push_msg['task_id'] = task_push_msg['data'][0]
        task_push_msg['result'] = task_push_msg['data'][2] & 3
        task_push_msg['fail_reason'] = task_push_msg['data'][2] >> 2 & 7
        task_push_msg['percent'] = task_push_msg['data'][1]
        self.script_state.set_block_running_percent(task_push_msg['percent'])
        self.script_state.set_block_running_fail_reason_code(task_push_msg['fail_reason'])
        logger.info('TASK ID = ' + str(task_push_msg['task_id']) + ', ' + str(task_push_msg['percent']) + '% STATE = ' + str(task_push_msg['result']) + ' FAIL_REASON = ' + str(task_push_msg['fail_reason']))
        self.event_watchdog_set(identify)
        if task_push_msg['result'] != 0:
            logger.info('TASK ID = ' + str(task_push_msg['task_id']) + ' FINISHED.')
            if identify in self.already_finish_task_identify_set:
                self.already_finish_task_identify_set.remove(identify)
            else:
                self.event_notify(identify)

    def send_task_stop(self, event_msg, time_out=duml_cmdset.MSG_DEFAULT_TIMEOUT):
        duss_result, resp = self.send_sync(event_msg, time_out)
        return duss_result

    def send_async(self):
        pass

    def resp_ok(self, msg):
        self.resp_retcode(msg, duml_cmdset.DUSS_MB_RET_OK)

    def resp_retcode(self, msg, retcode):
        event_msg = duss_event_msg.unpack2EventMsg(msg)
        event_msg.clear()
        event_msg.append('ret_code', 'uint8', retcode)
        event_msg.sender, event_msg.receiver = event_msg.receiver, event_msg.sender
        event_msg.cmd_type = duml_cmdset.ACK_PKG_TYPE
        self.send_msg(event_msg)

    def resp_event_msg(self, event_msg):
        event_msg.sender, event_msg.receiver = event_msg.receiver, event_msg.sender
        event_msg.cmd_type = duml_cmdset.ACK_PKG_TYPE
        self.send_msg(event_msg)

    def event_msg_invalid_check_callback_register(self, callback):
        self.check_event_msg_invalid_callback = callback

    def event_msg_invalid_check_callback_unregister(self):
        self.check_event_msg_invalid_callback = None

    def check_event_msg_invalid(self, event_msg):
        if callable(self.check_event_msg_invalid_callback):
            return self.check_event_msg_invalid_callback(event_msg)
        return (False, None)