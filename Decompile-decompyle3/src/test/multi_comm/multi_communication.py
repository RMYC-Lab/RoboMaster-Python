# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: .\src\test\multi_comm\multi_communication.py
# Compiled at: 2021-08-19 19:18:58
# Size of source mod 2**32: 4316 bytes
import queue, threading, rm_log
logger = rm_log.dji_scratch_logger_get()

class MultiCommunication(object):
    PORT = 40930

    def __init__(self, event_client, socket):
        self.event_client = event_client
        self.socket = socket
        self.user_fd = -1
        self.send_group = 0
        self.recv_group = ()
        self.recv_callback = None
        self.recv_msg_queue = queue.Queue(16)
        self._MultiCommunication__recv_callback_process_thread = None
        self._MultiCommunication__recv_callback_process_finish = True

    def init(self):
        logger.info('MULTI_COMM INIT')
        self.user_fd = self.socket.create((self.socket.UDP_MODE),
          (
         '', self.PORT),
          server=True,
          recv_callback=(self._MultiCommunication__recv_msg_from_socket))
        if self.user_fd == -1:
            logger.info('create socket error')
        self.socket.set_udp_default_target_addr(self.user_fd, ('<broadcast>', self.PORT))

    def set_mode(self, mode):
        pass

    def set_group(self, send_group, recv_group=()):
        self.send_group = send_group
        if recv_group == ():
            self.recv_group = (
             send_group,)
        else:
            if type(recv_group) == tuple or type(recv_group) == list:
                self.recv_group = tuple(recv_group)
            else:
                if type(recv_group) == int:
                    self.recv_group = (
                     recv_group,)
                else:
                    logger.error('SET GROUP ERROR, value is %s' % str(self.recv_group))

    def send_msg(self, msg, group=None):
        if group == None:
            group = self.send_group
        msg = 'SENDER_GROUP:%s MSG:%s' % (str(group), str(msg))
        self.socket.send(self.user_fd, msg)

    def recv_msg--- This code section failed: ---

 L.  60         0  LOAD_CONST               0.2
                2  STORE_FAST               'timeout_t'

 L.  61         4  LOAD_FAST                'timeout'
                6  LOAD_CONST               None
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_TRUE     20  'to 20'
               12  LOAD_FAST                'timeout'
               14  LOAD_CONST               0
               16  COMPARE_OP               <=
               18  POP_JUMP_IF_FALSE    24  'to 24'
             20_0  COME_FROM            10  '10'

 L.  62        20  LOAD_CONST               7200
               22  STORE_FAST               'timeout'
             24_0  COME_FROM            18  '18'

 L.  63        24  LOAD_FAST                'timeout'
               26  LOAD_CONST               0.2
               28  BINARY_TRUE_DIVIDE
               30  STORE_FAST               'count_t'

 L.  64        32  LOAD_FAST                'self'
               34  LOAD_ATTR                recv_callback
               36  LOAD_CONST               None
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE   130  'to 130'
             42_0  COME_FROM           118  '118'
             42_1  COME_FROM           114  '114'
             42_2  COME_FROM           110  '110'

 L.  65        42  LOAD_FAST                'count_t'
               44  LOAD_CONST               0
               46  COMPARE_OP               >=
               48  POP_JUMP_IF_FALSE   120  'to 120'
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                event_client
               54  LOAD_ATTR                script_state
               56  LOAD_METHOD              check_stop
               58  CALL_METHOD_0         0  ''
               60  POP_JUMP_IF_TRUE    120  'to 120'

 L.  66        62  SETUP_FINALLY        84  'to 84'

 L.  67        64  LOAD_FAST                'self'
               66  LOAD_ATTR                recv_msg_queue
               68  LOAD_ATTR                get
               70  LOAD_FAST                'timeout_t'
               72  LOAD_CONST               ('timeout',)
               74  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               76  STORE_FAST               'msg'

 L.  68        78  LOAD_FAST                'msg'
               80  POP_BLOCK        
               82  RETURN_VALUE     
             84_0  COME_FROM_FINALLY    62  '62'

 L.  69        84  DUP_TOP          
               86  LOAD_GLOBAL              queue
               88  LOAD_ATTR                Empty
               90  COMPARE_OP               exception-match
               92  POP_JUMP_IF_FALSE   116  'to 116'
               94  POP_TOP          
               96  POP_TOP          
               98  POP_TOP          

 L.  70       100  LOAD_FAST                'count_t'
              102  LOAD_CONST               1
              104  INPLACE_SUBTRACT 
              106  STORE_FAST               'count_t'

 L.  71       108  POP_EXCEPT       
              110  JUMP_LOOP            42  'to 42'
              112  POP_EXCEPT       
              114  JUMP_LOOP            42  'to 42'
            116_0  COME_FROM            92  '92'
              116  END_FINALLY      
              118  JUMP_LOOP            42  'to 42'
            120_0  COME_FROM            60  '60'
            120_1  COME_FROM            48  '48'

 L.  72       120  LOAD_GLOBAL              logger
              122  LOAD_METHOD              info
              124  LOAD_STR                 'timeout'
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          
            130_0  COME_FROM            40  '40'

Parse error at or near `END_FINALLY' instruction at offset 116

    def register_recv_callback(self, callback):
        if callable(callback):
            self.recv_callback = callback
            if self._MultiCommunication__recv_callback_process_thread == None:
                self._MultiCommunication__recv_callback_process_finish = False
                self._MultiCommunication__recv_callback_process_thread = threading.Thread(target=(self._MultiCommunication__recv_callback_process))
                self._MultiCommunication__recv_callback_process_thread.start()

    def exit(self):
        logger.info('MULTI_COMM EXIT')
        if not self._MultiCommunication__recv_callback_process_finish:
            self._MultiCommunication__recv_callback_process_finish = True
            self.recv_msg_queue.put('eixt')
            self.recv_msg_queue.put('eixt')
            self._MultiCommunication__recv_callback_process_thread.join()
        self.socket.close(self.user_fd)

    def __recv_callback_process(self):
        while True:
            if not (self._MultiCommunication__recv_callback_process_finish or self.event_client.script_state.check_stop()):
                try:
                    msg = self.recv_msg_queue.get()
                    if self._MultiCommunication__recv_callback_process_finish or self.event_client.script_state.check_stop():
                        break
                    if self.recv_callback:
                        self.recv_callback(msg)
                except queue.Empty:
                    continue

    def __recv_msg_from_socket(self, recv_addr, user_id, msg):
        if msg.find('SENDER_GROUP:') != -1:
            if msg.find(' ') != -1:
                group = msg[msg.find('SENDER_GROUP:') + len('SENDER_GROUP:'):msg.find(' ')]
                msg = msg[msg.find('MSG:') + len('MSG:'):]
                if not group.isdigit():
                    return
                group = int(group)
                if group not in self.recv_group:
                    return
                if self.recv_msg_queue.full():
                    self.recv_msg_queue.get()
                self.recv_msg_queue.put((group, msg))