# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: .\src\test\rm_socket.py
# Compiled at: 2021-08-19 19:18:58
# Size of source mod 2**32: 22006 bytes
import socket, queue, select, threading, time, rm_log, subprocess, errno, traceback, tools
logger = rm_log.dji_scratch_logger_get()

class RmSocket(object):
    TCP_MODE = 'tcp'
    UDP_MODE = 'udp'

    def __init__(self):
        self.user_fd_to_socket_fd = {}
        self.socket_fileno_info = {}
        self.send_msg_queue = queue.Queue(128)
        self.user_fd = 0
        if not tools.is_windows_system():
            self.epoll_obj = select.kqueue()
        self.recv_thread_finish = True
        self.recv_thread = None

    def init(self):
        logger.info('SOCKET INIT')
        if not tools.is_windows_system():
            logger.info('Not Windows SOCKET INIT')
            self.recv_thread = threading.Thread(target=(self._RmSocket__epoll_task))
            self.recv_thread_finish = False

    def exit(self):
        logger.info('RM SOCKET EXIT')
        self.recv_thread_finish = True
        for socket_fileno in self.socket_fileno_info.keys():
            self.socket_fileno_info[socket_fileno]['socket'].close()
        else:
            self.socket_fileno_info = {}
            self.user_fd_to_socket_fd = {}
            self.recv_thread.join()

    def close(self, user_fd):
        logger.info('SHUWDOWN %d' % user_fd)
        if user_fd in self.user_fd_to_socket_fd.keys():
            self._RmSocket__remove_socket_fileno_info(self.user_fd_to_socket_fd[user_fd])

    def create(self, mode, ip_port, server=True, recv_msgq_size=16, send_msgq_size=16, **callback):
        if mode == RmSocket.TCP_MODE:
            if server:
                return (self._RmSocket__create_tcp_server)(ip_port, recv_msgq_size=recv_msgq_size, send_msgq_size=send_msgq_size, **callback)
            return (self._RmSocket__create_tcp_client)(ip_port, recv_msgq_size=recv_msgq_size, send_msgq_size=send_msgq_size, **callback)
        else:
            if mode == RmSocket.UDP_MODE:
                if server:
                    return (self._RmSocket__create_udp_server)(ip_port, recv_msgq_size=recv_msgq_size, send_msgq_size=send_msgq_size, **callback)
                return (self._RmSocket__create_udp_client)(ip_port, recv_msgq_size=recv_msgq_size, send_msgq_size=send_msgq_size, **callback)
            else:
                return

    def send--- This code section failed: ---

 L.  73         0  SETUP_FINALLY       216  'to 216'

 L.  74         2  LOAD_GLOBAL              str
                4  LOAD_FAST                'msg'
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'msg'

 L.  75        10  LOAD_FAST                'user_fd'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                user_fd_to_socket_fd
               16  LOAD_METHOD              keys
               18  CALL_METHOD_0         0  ''
               20  COMPARE_OP               in
               22  POP_JUMP_IF_FALSE   212  'to 212'

 L.  76        24  LOAD_FAST                'self'
               26  LOAD_ATTR                user_fd_to_socket_fd
               28  LOAD_FAST                'user_fd'
               30  BINARY_SUBSCR    
               32  STORE_FAST               'fileno'

 L.  77        34  LOAD_FAST                'self'
               36  LOAD_ATTR                socket_fileno_info
               38  LOAD_FAST                'fileno'
               40  BINARY_SUBSCR    
               42  STORE_FAST               'attr'

 L.  78        44  LOAD_FAST                'attr'
               46  LOAD_STR                 'type'
               48  BINARY_SUBSCR    
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                TCP_MODE
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_FALSE    92  'to 92'
               58  LOAD_FAST                'attr'
               60  LOAD_STR                 'server_flag'
               62  BINARY_SUBSCR    
               64  LOAD_CONST               True
               66  COMPARE_OP               !=
               68  POP_JUMP_IF_FALSE    92  'to 92'

 L.  79        70  LOAD_FAST                'attr'
               72  LOAD_STR                 'socket'
               74  BINARY_SUBSCR    
               76  LOAD_METHOD              send
               78  LOAD_FAST                'msg'
               80  LOAD_METHOD              encode
               82  LOAD_STR                 'utf-8'
               84  CALL_METHOD_1         1  ''
               86  CALL_METHOD_1         1  ''
               88  POP_BLOCK        
               90  RETURN_VALUE     
             92_0  COME_FROM            68  '68'
             92_1  COME_FROM            56  '56'

 L.  80        92  LOAD_FAST                'attr'
               94  LOAD_STR                 'type'
               96  BINARY_SUBSCR    
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                UDP_MODE
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   212  'to 212'

 L.  81       106  LOAD_FAST                'ip_port'
              108  POP_JUMP_IF_FALSE   134  'to 134'

 L.  82       110  LOAD_FAST                'attr'
              112  LOAD_STR                 'socket'
              114  BINARY_SUBSCR    
              116  LOAD_METHOD              sendto
              118  LOAD_FAST                'msg'
              120  LOAD_METHOD              encode
              122  LOAD_STR                 'utf-8'
              124  CALL_METHOD_1         1  ''
              126  LOAD_FAST                'ip_port'
              128  CALL_METHOD_2         2  ''
              130  POP_BLOCK        
              132  RETURN_VALUE     
            134_0  COME_FROM           108  '108'

 L.  83       134  LOAD_STR                 'default_target_addr'
              136  LOAD_FAST                'attr'
              138  LOAD_METHOD              keys
              140  CALL_METHOD_0         0  ''
              142  COMPARE_OP               in
              144  POP_JUMP_IF_FALSE   186  'to 186'
              146  LOAD_FAST                'attr'
              148  LOAD_STR                 'default_target_addr'
              150  BINARY_SUBSCR    
              152  POP_JUMP_IF_FALSE   186  'to 186'

 L.  84       154  LOAD_FAST                'attr'
              156  LOAD_STR                 'default_target_addr'
              158  BINARY_SUBSCR    
              160  STORE_FAST               'ip_port'

 L.  85       162  LOAD_FAST                'attr'
              164  LOAD_STR                 'socket'
              166  BINARY_SUBSCR    
              168  LOAD_METHOD              sendto
              170  LOAD_FAST                'msg'
              172  LOAD_METHOD              encode
              174  LOAD_STR                 'utf-8'
              176  CALL_METHOD_1         1  ''
              178  LOAD_FAST                'ip_port'
              180  CALL_METHOD_2         2  ''
              182  POP_BLOCK        
              184  RETURN_VALUE     
            186_0  COME_FROM           152  '152'
            186_1  COME_FROM           144  '144'

 L.  87       186  LOAD_GLOBAL              logger
              188  LOAD_METHOD              error
              190  LOAD_STR                 'no target ip and port, cur msg is %s'
              192  LOAD_FAST                'msg'
              194  LOAD_METHOD              encode
              196  LOAD_STR                 'utf-8'
              198  CALL_METHOD_1         1  ''
              200  BINARY_MODULO    
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          

 L.  88       206  POP_BLOCK        
              208  LOAD_CONST               None
              210  RETURN_VALUE     
            212_0  COME_FROM           104  '104'
            212_1  COME_FROM            22  '22'
              212  POP_BLOCK        
              214  JUMP_FORWARD        364  'to 364'
            216_0  COME_FROM_FINALLY     0  '0'

 L.  89       216  DUP_TOP          
              218  LOAD_GLOBAL              socket
              220  LOAD_ATTR                error
              222  COMPARE_OP               exception-match
          224_226  POP_JUMP_IF_FALSE   314  'to 314'
              228  POP_TOP          
              230  STORE_FAST               'e'
              232  POP_TOP          
              234  SETUP_FINALLY       302  'to 302'

 L.  90       236  LOAD_FAST                'e'
              238  LOAD_ATTR                errno
              240  LOAD_GLOBAL              errno
              242  LOAD_ATTR                EAGAIN
              244  COMPARE_OP               ==
          246_248  POP_JUMP_IF_FALSE   284  'to 284'

 L.  91       250  LOAD_FAST                'attr'
              252  LOAD_STR                 'send_msgq'
              254  BINARY_SUBSCR    
              256  LOAD_METHOD              full
              258  CALL_METHOD_0         0  ''
          260_262  POP_JUMP_IF_TRUE    298  'to 298'

 L.  92       264  LOAD_FAST                'attr'
              266  LOAD_STR                 'send_msgq'
              268  BINARY_SUBSCR    
              270  LOAD_METHOD              put
              272  LOAD_FAST                'msg'
              274  LOAD_FAST                'ip_port'
              276  BUILD_TUPLE_2         2 
              278  CALL_METHOD_1         1  ''
              280  POP_TOP          
              282  JUMP_FORWARD        298  'to 298'
            284_0  COME_FROM           246  '246'

 L.  94       284  LOAD_GLOBAL              logger
              286  LOAD_METHOD              fatal
              288  LOAD_GLOBAL              traceback
              290  LOAD_METHOD              format_exc
              292  CALL_METHOD_0         0  ''
              294  CALL_METHOD_1         1  ''
              296  POP_TOP          
            298_0  COME_FROM           282  '282'
            298_1  COME_FROM           260  '260'
              298  POP_BLOCK        
              300  BEGIN_FINALLY    
            302_0  COME_FROM_FINALLY   234  '234'
              302  LOAD_CONST               None
              304  STORE_FAST               'e'
              306  DELETE_FAST              'e'
              308  END_FINALLY      
              310  POP_EXCEPT       
              312  JUMP_FORWARD        364  'to 364'
            314_0  COME_FROM           224  '224'

 L.  95       314  DUP_TOP          
              316  LOAD_GLOBAL              Exception
              318  COMPARE_OP               exception-match
          320_322  POP_JUMP_IF_FALSE   362  'to 362'
              324  POP_TOP          
              326  STORE_FAST               'e'
              328  POP_TOP          
              330  SETUP_FINALLY       350  'to 350'

 L.  96       332  LOAD_GLOBAL              logger
              334  LOAD_METHOD              fatal
              336  LOAD_GLOBAL              traceback
              338  LOAD_METHOD              format_exc
              340  CALL_METHOD_0         0  ''
              342  CALL_METHOD_1         1  ''
              344  POP_TOP          
              346  POP_BLOCK        
              348  BEGIN_FINALLY    
            350_0  COME_FROM_FINALLY   330  '330'
              350  LOAD_CONST               None
              352  STORE_FAST               'e'
              354  DELETE_FAST              'e'
              356  END_FINALLY      
              358  POP_EXCEPT       
              360  JUMP_FORWARD        364  'to 364'
            362_0  COME_FROM           320  '320'
              362  END_FINALLY      
            364_0  COME_FROM           360  '360'
            364_1  COME_FROM           312  '312'
            364_2  COME_FROM           214  '214'

Parse error at or near `LOAD_CONST' instruction at offset 208

    def recv(self, user_fd):
        if user_fd in self.user_fd_to_socket_fd.keys():
            fileno = self.user_fd_to_socket_fd[user_fd]
            msg_queue = self.socket_fileno_info[fileno]['recv_msgq']
            if not msg_queue.empty():
                msg = msg_queue.get()
                return msg
            return

    def get_status(self):
        pass

    def get_local_host_ip--- This code section failed: ---

 L. 114         0  LOAD_FAST                'user_fd'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                user_fd_to_socket_fd
                6  LOAD_METHOD              keys
                8  CALL_METHOD_0         0  ''
               10  COMPARE_OP               in
               12  POP_JUMP_IF_FALSE   106  'to 106'

 L. 115        14  LOAD_FAST                'self'
               16  LOAD_ATTR                socket_fileno_info
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                user_fd_to_socket_fd
               22  LOAD_FAST                'user_fd'
               24  BINARY_SUBSCR    
               26  BINARY_SUBSCR    
               28  LOAD_STR                 'socket'
               30  BINARY_SUBSCR    
               32  STORE_FAST               'socket'

 L. 116        34  SETUP_FINALLY        50  'to 50'

 L. 117        36  LOAD_FAST                'socket'
               38  LOAD_METHOD              getsockname
               40  CALL_METHOD_0         0  ''
               42  LOAD_CONST               0
               44  BINARY_SUBSCR    
               46  POP_BLOCK        
               48  RETURN_VALUE     
             50_0  COME_FROM_FINALLY    34  '34'

 L. 118        50  DUP_TOP          
               52  LOAD_GLOBAL              Exception
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE   102  'to 102'
               58  POP_TOP          
               60  STORE_FAST               'e'
               62  POP_TOP          
               64  SETUP_FINALLY        90  'to 90'

 L. 119        66  LOAD_GLOBAL              logger
               68  LOAD_METHOD              error
               70  LOAD_GLOBAL              traceback
               72  LOAD_METHOD              format_exc
               74  CALL_METHOD_0         0  ''
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L. 120        80  POP_BLOCK        
               82  POP_EXCEPT       
               84  CALL_FINALLY         90  'to 90'
               86  LOAD_CONST               None
               88  RETURN_VALUE     
             90_0  COME_FROM            84  '84'
             90_1  COME_FROM_FINALLY    64  '64'
               90  LOAD_CONST               None
               92  STORE_FAST               'e'
               94  DELETE_FAST              'e'
               96  END_FINALLY      
               98  POP_EXCEPT       
              100  JUMP_FORWARD        232  'to 232'
            102_0  COME_FROM            56  '56'
              102  END_FINALLY      
              104  JUMP_FORWARD        232  'to 232'
            106_0  COME_FROM            12  '12'

 L. 122       106  LOAD_GLOBAL              subprocess
              108  LOAD_ATTR                Popen
              110  LOAD_STR                 'busybox'
              112  LOAD_STR                 'ifconfig'
              114  LOAD_STR                 'wlan0'
              116  BUILD_LIST_3          3 

 L. 123       118  LOAD_GLOBAL              subprocess
              120  LOAD_ATTR                PIPE

 L. 124       122  LOAD_GLOBAL              subprocess
              124  LOAD_ATTR                PIPE

 L. 122       126  LOAD_CONST               ('stdout', 'stderr')
              128  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              130  STORE_FAST               'ifconfig_pipe'

 L. 126       132  LOAD_FAST                'ifconfig_pipe'
              134  LOAD_METHOD              communicate
              136  CALL_METHOD_0         0  ''
              138  UNPACK_SEQUENCE_2     2 
              140  STORE_FAST               'ifconfig_info'
              142  STORE_FAST               'error'

 L. 127       144  LOAD_FAST                'ifconfig_pipe'
              146  LOAD_METHOD              kill
              148  CALL_METHOD_0         0  ''
              150  POP_TOP          

 L. 129       152  LOAD_GLOBAL              len
              154  LOAD_FAST                'error'
              156  CALL_FUNCTION_1       1  ''
              158  LOAD_CONST               0
              160  COMPARE_OP               !=
              162  POP_JUMP_IF_FALSE   168  'to 168'

 L. 131       164  LOAD_CONST               None
              166  RETURN_VALUE     
            168_0  COME_FROM           162  '162'

 L. 133       168  LOAD_FAST                'ifconfig_info'
              170  LOAD_METHOD              decode
              172  LOAD_STR                 'utf-8'
              174  CALL_METHOD_1         1  ''
              176  STORE_FAST               'ifconfig_info'

 L. 135       178  LOAD_FAST                'ifconfig_info'
              180  LOAD_METHOD              split
              182  LOAD_STR                 '\n'
              184  CALL_METHOD_1         1  ''
              186  LOAD_CONST               1
              188  BINARY_SUBSCR    
              190  STORE_FAST               'inet_addr_str'

 L. 137       192  LOAD_CONST               None
              194  STORE_FAST               'local_host_ip'

 L. 138       196  LOAD_STR                 'inet addr'
              198  LOAD_FAST                'inet_addr_str'
              200  COMPARE_OP               in
              202  POP_JUMP_IF_FALSE   228  'to 228'

 L. 139       204  LOAD_FAST                'inet_addr_str'
              206  LOAD_METHOD              split
              208  LOAD_STR                 ':'
              210  CALL_METHOD_1         1  ''
              212  LOAD_CONST               1
              214  BINARY_SUBSCR    
              216  LOAD_METHOD              split
              218  LOAD_STR                 ' '
              220  CALL_METHOD_1         1  ''
              222  LOAD_CONST               0
              224  BINARY_SUBSCR    
              226  STORE_FAST               'local_host_ip'
            228_0  COME_FROM           202  '202'

 L. 141       228  LOAD_FAST                'local_host_ip'
              230  RETURN_VALUE     
            232_0  COME_FROM           104  '104'
            232_1  COME_FROM           100  '100'

Parse error at or near `POP_EXCEPT' instruction at offset 82

    def get_remote_host_ip--- This code section failed: ---

 L. 144         0  LOAD_FAST                'user_fd'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                user_fd_to_socket_fd
                6  LOAD_METHOD              keys
                8  CALL_METHOD_0         0  ''
               10  COMPARE_OP               in
               12  POP_JUMP_IF_FALSE   100  'to 100'

 L. 145        14  LOAD_FAST                'self'
               16  LOAD_ATTR                socket_fileno_info
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                user_fd_to_socket_fd
               22  LOAD_FAST                'user_fd'
               24  BINARY_SUBSCR    
               26  BINARY_SUBSCR    
               28  LOAD_STR                 'socket'
               30  BINARY_SUBSCR    
               32  STORE_FAST               'socket'

 L. 146        34  SETUP_FINALLY        50  'to 50'

 L. 147        36  LOAD_FAST                'socket'
               38  LOAD_METHOD              getpeername
               40  CALL_METHOD_0         0  ''
               42  LOAD_CONST               0
               44  BINARY_SUBSCR    
               46  POP_BLOCK        
               48  RETURN_VALUE     
             50_0  COME_FROM_FINALLY    34  '34'

 L. 148        50  DUP_TOP          
               52  LOAD_GLOBAL              Exception
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    96  'to 96'
               58  POP_TOP          
               60  STORE_FAST               'e'
               62  POP_TOP          
               64  SETUP_FINALLY        84  'to 84'

 L. 149        66  LOAD_GLOBAL              logger
               68  LOAD_METHOD              error
               70  LOAD_GLOBAL              traceback
               72  LOAD_METHOD              format_exc
               74  CALL_METHOD_0         0  ''
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
               80  POP_BLOCK        
               82  BEGIN_FINALLY    
             84_0  COME_FROM_FINALLY    64  '64'
               84  LOAD_CONST               None
               86  STORE_FAST               'e'
               88  DELETE_FAST              'e'
               90  END_FINALLY      
               92  POP_EXCEPT       
               94  JUMP_FORWARD        104  'to 104'
             96_0  COME_FROM            56  '56'
               96  END_FINALLY      
               98  JUMP_FORWARD        104  'to 104'
            100_0  COME_FROM            12  '12'

 L. 151       100  LOAD_CONST               None
              102  RETURN_VALUE     
            104_0  COME_FROM            98  '98'
            104_1  COME_FROM            94  '94'

Parse error at or near `JUMP_FORWARD' instruction at offset 98

    def set_udp_default_target_addr(self, user_fd, ip_port):
        if user_fd in self.user_fd_to_socket_fd.keys():
            fileno = self.user_fd_to_socket_fd[user_fd]
            if ip_port[0] == '<broadcast>':
                self.socket_fileno_info[fileno]['socket'].setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                self.socket_fileno_info[fileno]['socket'].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_fileno_info[fileno]['default_target_addr'] = ip_port

    def update_socket_info(self, user_fd, recv_msgq_size=None, send_msgq_size=None, connected_callback=None, disconnected_callback=None, recv_callback=None, send_callback=None):
        if user_fd in self.user_fd_to_socket_fd.keys():
            fileno = self.user_fd_to_socket_fd[user_fd]
            if recv_msgq_size:
                self.socket_fileno_info[fileno]['recv_msgq'] = queue.Queue(recv_msgq_size)
            if send_msgq_size:
                self.socket_fileno_info[fileno]['send_msgq'] = queue.Queue(send_msgq_size)
            if connected_callback:
                if callable(connecti_calback):
                    self.socket_fileno_info[fileno]['callback']['connected_callback'] = connected_callback
            if disconnected_callback:
                if callable(disconnected_calback):
                    self.socket_fileno_info[fileno]['callback']['disconnected_callback'] = disconnected_callback
            if recv_callback:
                if callable(recv_callback):
                    self.socket_fileno_info[fileno]['callback']['recv_callback'] = recv_callback
            if send_callback:
                if callable(send_callback):
                    self.socket_fileno_info[fileno]['callback']['send_callback'] = send_callback

    def __add_socket_fileno_info(self, fd, type, server=False, recv_msgq_size=1, send_msgq_size=1, **callback):
        self.user_fd += 1
        fd_t = self.user_fd
        self.user_fd_to_socket_fd[self.user_fd] = fd.fileno()
        fd.setblocking(False)
        self.socket_fileno_info[fd.fileno()] = {'socket':fd, 
         'user_fd':self.user_fd, 
         'type':type, 
         'server_flag':server, 
         'callback':None, 
         'recv_msgq':queue.Queue(recv_msgq_size), 
         'send_msgq':queue.Queue(send_msgq_size)}
        callback_dict = {}
        if 'connected_callback' in callback.keys():
            if callable(callback['connected_callback']):
                callback_dict['connected_callback'] = callback['connected_callback']
        if 'disconnected_callback' in callback.keys():
            if callable(callback['disconnected_callback']):
                callback_dict['disconnected_callback'] = callback['disconnected_callback']
        if 'recv_callback' in callback.keys():
            if callable(callback['recv_callback']):
                callback_dict['recv_callback'] = callback['recv_callback']
        if 'send_callback' in callback.keys():
            if callable(callback['send_callback']):
                callback_dict['send_callback'] = callback['send_callback']
        self.socket_fileno_info[fd.fileno()]['callback'] = callback_dict
        logger.info('NEW SOCKET %s' % fd)
        return fd_t

    def __remove_socket_fileno_info(self, fileno):
        if fileno in self.socket_fileno_info.keys():
            socket = self.socket_fileno_info[fileno]['socket']
            socket.close()
            if self.socket_fileno_info[fileno]['user_fd'] in self.user_fd_to_socket_fd.keys():
                self.user_fd_to_socket_fd.pop(self.socket_fileno_info[fileno]['user_fd'])
            self.socket_fileno_info.pop(fileno)

    def __create_tcp_server--- This code section failed: ---

 L. 225         0  SETUP_FINALLY        72  'to 72'

 L. 226         2  LOAD_GLOBAL              socket
                4  LOAD_METHOD              socket
                6  LOAD_GLOBAL              socket
                8  LOAD_ATTR                AF_INET
               10  LOAD_GLOBAL              socket
               12  LOAD_ATTR                SOCK_STREAM
               14  CALL_METHOD_2         2  ''
               16  STORE_FAST               'fd'

 L. 227        18  LOAD_FAST                'fd'
               20  LOAD_METHOD              bind
               22  LOAD_FAST                'ip_port'
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          

 L. 229        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _RmSocket__add_socket_fileno_info
               32  LOAD_FAST                'fd'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                TCP_MODE
               38  BUILD_TUPLE_2         2 
               40  LOAD_CONST               True
               42  LOAD_FAST                'recv_msgq_size'
               44  LOAD_FAST                'send_msgq_size'
               46  LOAD_CONST               ('server', 'recv_msgq_size', 'send_msgq_size')
               48  BUILD_CONST_KEY_MAP_3     3 
               50  LOAD_FAST                'callback'
               52  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               54  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               56  STORE_FAST               'fd_t'

 L. 231        58  LOAD_FAST                'fd'
               60  LOAD_METHOD              listen
               62  CALL_METHOD_0         0  ''
               64  POP_TOP          

 L. 233        66  LOAD_FAST                'fd_t'
               68  POP_BLOCK        
               70  RETURN_VALUE     
             72_0  COME_FROM_FINALLY     0  '0'

 L. 234        72  DUP_TOP          
               74  LOAD_GLOBAL              Exception
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   124  'to 124'
               80  POP_TOP          
               82  STORE_FAST               'e'
               84  POP_TOP          
               86  SETUP_FINALLY       112  'to 112'

 L. 235        88  LOAD_GLOBAL              logger
               90  LOAD_METHOD              fatal
               92  LOAD_GLOBAL              traceback
               94  LOAD_METHOD              format_exc
               96  CALL_METHOD_0         0  ''
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          

 L. 236       102  POP_BLOCK        
              104  POP_EXCEPT       
              106  CALL_FINALLY        112  'to 112'
              108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM           106  '106'
            112_1  COME_FROM_FINALLY    86  '86'
              112  LOAD_CONST               None
              114  STORE_FAST               'e'
              116  DELETE_FAST              'e'
              118  END_FINALLY      
              120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
            124_0  COME_FROM            78  '78'
              124  END_FINALLY      
            126_0  COME_FROM           122  '122'

Parse error at or near `POP_EXCEPT' instruction at offset 104

    def __create_tcp_client--- This code section failed: ---

 L. 239         0  SETUP_FINALLY        72  'to 72'

 L. 240         2  LOAD_GLOBAL              socket
                4  LOAD_METHOD              socket
                6  LOAD_GLOBAL              socket
                8  LOAD_ATTR                AF_INET
               10  LOAD_GLOBAL              socket
               12  LOAD_ATTR                SOCK_STREAM
               14  CALL_METHOD_2         2  ''
               16  STORE_FAST               'fd'

 L. 241        18  LOAD_FAST                'fd'
               20  LOAD_METHOD              bind
               22  LOAD_FAST                'ip_port'
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          

 L. 243        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _RmSocket__add_socket_fileno_info
               32  LOAD_FAST                'fd'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                TCP_MODE
               38  BUILD_TUPLE_2         2 
               40  LOAD_CONST               False
               42  LOAD_FAST                'recv_msgq_size'
               44  LOAD_FAST                'send_msgq_size'
               46  LOAD_CONST               ('server', 'recv_msgq_size', 'send_msgq_size')
               48  BUILD_CONST_KEY_MAP_3     3 
               50  LOAD_FAST                'callback'
               52  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               54  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               56  STORE_FAST               'fd_t'

 L. 245        58  LOAD_FAST                'fd'
               60  LOAD_METHOD              connect
               62  CALL_METHOD_0         0  ''
               64  POP_TOP          

 L. 246        66  LOAD_FAST                'fd_t'
               68  POP_BLOCK        
               70  RETURN_VALUE     
             72_0  COME_FROM_FINALLY     0  '0'

 L. 248        72  DUP_TOP          
               74  LOAD_GLOBAL              Exception
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   124  'to 124'
               80  POP_TOP          
               82  STORE_FAST               'e'
               84  POP_TOP          
               86  SETUP_FINALLY       112  'to 112'

 L. 249        88  LOAD_GLOBAL              logger
               90  LOAD_METHOD              fatal
               92  LOAD_GLOBAL              traceback
               94  LOAD_METHOD              format_exc
               96  CALL_METHOD_0         0  ''
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          

 L. 250       102  POP_BLOCK        
              104  POP_EXCEPT       
              106  CALL_FINALLY        112  'to 112'
              108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM           106  '106'
            112_1  COME_FROM_FINALLY    86  '86'
              112  LOAD_CONST               None
              114  STORE_FAST               'e'
              116  DELETE_FAST              'e'
              118  END_FINALLY      
              120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
            124_0  COME_FROM            78  '78'
              124  END_FINALLY      
            126_0  COME_FROM           122  '122'

Parse error at or near `POP_EXCEPT' instruction at offset 104

    def __create_udp_server--- This code section failed: ---

 L. 253         0  SETUP_FINALLY        64  'to 64'

 L. 254         2  LOAD_GLOBAL              socket
                4  LOAD_METHOD              socket
                6  LOAD_GLOBAL              socket
                8  LOAD_ATTR                AF_INET
               10  LOAD_GLOBAL              socket
               12  LOAD_ATTR                SOCK_DGRAM
               14  CALL_METHOD_2         2  ''
               16  STORE_FAST               'fd'

 L. 256        18  LOAD_FAST                'fd'
               20  LOAD_METHOD              bind
               22  LOAD_FAST                'ip_port'
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          

 L. 258        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _RmSocket__add_socket_fileno_info
               32  LOAD_FAST                'fd'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                UDP_MODE
               38  BUILD_TUPLE_2         2 
               40  LOAD_CONST               True
               42  LOAD_FAST                'recv_msgq_size'
               44  LOAD_FAST                'send_msgq_size'
               46  LOAD_CONST               ('server', 'recv_msgq_size', 'send_msgq_size')
               48  BUILD_CONST_KEY_MAP_3     3 
               50  LOAD_FAST                'callback'
               52  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               54  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               56  STORE_FAST               'fd_t'

 L. 260        58  LOAD_FAST                'fd_t'
               60  POP_BLOCK        
               62  RETURN_VALUE     
             64_0  COME_FROM_FINALLY     0  '0'

 L. 261        64  DUP_TOP          
               66  LOAD_GLOBAL              Exception
               68  COMPARE_OP               exception-match
               70  POP_JUMP_IF_FALSE   118  'to 118'
               72  POP_TOP          
               74  STORE_FAST               'e'
               76  POP_TOP          
               78  SETUP_FINALLY       106  'to 106'

 L. 262        80  LOAD_GLOBAL              logger
               82  LOAD_METHOD              fatal
               84  LOAD_GLOBAL              traceback
               86  LOAD_METHOD              format_exc
               88  CALL_METHOD_0         0  ''
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          

 L. 263        94  LOAD_FAST                'fd'
               96  ROT_FOUR         
               98  POP_BLOCK        
              100  POP_EXCEPT       
              102  CALL_FINALLY        106  'to 106'
              104  RETURN_VALUE     
            106_0  COME_FROM           102  '102'
            106_1  COME_FROM_FINALLY    78  '78'
              106  LOAD_CONST               None
              108  STORE_FAST               'e'
              110  DELETE_FAST              'e'
              112  END_FINALLY      
              114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM            70  '70'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'

Parse error at or near `POP_BLOCK' instruction at offset 98

    def __create_udp_client--- This code section failed: ---

 L. 266         0  SETUP_FINALLY        54  'to 54'

 L. 267         2  LOAD_GLOBAL              socket
                4  LOAD_METHOD              socket
                6  LOAD_GLOBAL              socket
                8  LOAD_ATTR                AF_INET
               10  LOAD_GLOBAL              socket
               12  LOAD_ATTR                SOCK_DGRAM
               14  CALL_METHOD_2         2  ''
               16  STORE_FAST               'fd'

 L. 268        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _RmSocket__add_socket_fileno_info
               22  LOAD_FAST                'fd'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                UDP_MODE
               28  BUILD_TUPLE_2         2 
               30  LOAD_CONST               False
               32  LOAD_FAST                'recv_msgq_size'
               34  LOAD_FAST                'send_msgq_size'
               36  LOAD_CONST               ('server', 'recv_msgq_size', 'send_msgq_size')
               38  BUILD_CONST_KEY_MAP_3     3 
               40  LOAD_FAST                'callback'
               42  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               44  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               46  STORE_FAST               'fd_t'

 L. 270        48  LOAD_FAST                'fd_t'
               50  POP_BLOCK        
               52  RETURN_VALUE     
             54_0  COME_FROM_FINALLY     0  '0'

 L. 271        54  DUP_TOP          
               56  LOAD_GLOBAL              Exception
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE   108  'to 108'
               62  POP_TOP          
               64  STORE_FAST               'e'
               66  POP_TOP          
               68  SETUP_FINALLY        96  'to 96'

 L. 272        70  LOAD_GLOBAL              logger
               72  LOAD_METHOD              fatal
               74  LOAD_GLOBAL              traceback
               76  LOAD_METHOD              format_exc
               78  CALL_METHOD_0         0  ''
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          

 L. 273        84  LOAD_FAST                'fd'
               86  ROT_FOUR         
               88  POP_BLOCK        
               90  POP_EXCEPT       
               92  CALL_FINALLY         96  'to 96'
               94  RETURN_VALUE     
             96_0  COME_FROM            92  '92'
             96_1  COME_FROM_FINALLY    68  '68'
               96  LOAD_CONST               None
               98  STORE_FAST               'e'
              100  DELETE_FAST              'e'
              102  END_FINALLY      
              104  POP_EXCEPT       
              106  JUMP_FORWARD        110  'to 110'
            108_0  COME_FROM            60  '60'
              108  END_FINALLY      
            110_0  COME_FROM           106  '106'

Parse error at or near `POP_BLOCK' instruction at offset 88

    def __register_connected_cb(self):
        pass

    def __register_disconnected_cb(self):
        pass

    def __register_recv_cb(self):
        pass

    def __register_send_cb(self):
        pass

    def __epoll_task(self):
        timeout = -1
        while True:
            while not self.recv_thread_finish:
                events = self.epoll_obj.poll(timeout)
                if not events:
                    pass
                else:
                    for fd_fileno, event in events:
                        cur_socket_info = self.socket_fileno_info[fd_fileno]
                        if cur_socket_info['type'] == self.TCP_MODE:
                            if cur_socket_info['server_flag'] == True:
                                while True:
                                    try:
                                        conn, addr = cur_socket_info['socket'].accept()
                                        fd_t = (self._RmSocket__add_socket_fileno_info)(conn, self.TCP_MODE, server=False, **self.socket_fileno_info[fd_fileno]['callback'])
                                        if 'connected_callback' in self.socket_fileno_info[fd_fileno]['callback'].keys():
                                            self.socket_fileno_info[fd_fileno]['callback']['connected_callback'](self.socket_fileno_info[fd_fileno]['user_fd'], fd_t)
                                        logger.info('NEW CONNECTION %s %s' % (conn, addr))
                                    except socket.error as e:
                                        try:
                                            if e.errno == errno.EAGAIN:
                                                logger.info('NO NEW CONNECTION ALSO')
                                            else:
                                                logger.fatal(traceback.format_exc())
                                        finally:
                                            e = None
                                            del e
                                        break
                                    except Exception as e:
                                        try:
                                            logger.fatal(traceback.format_exc())
                                        finally:
                                            e = None
                                            del e
                                        break

                            else:
                                if event & select.EPOLLHUP:
                                    if 'disconnected_callback' in self.socket_fileno_info[fd_fileno]['callback'].keys():
                                        self.socket_fileno_info[fd_fileno]['callback']['disconnected_callback'](self.socket_fileno_info[fd_fileno]['user_fd'])
                                    self._RmSocket__remove_socket_fileno_info(fd_fileno)
                                    self.epoll_obj.unregister(fd_fileno)
                                else:
                                    if event & select.EPOLLIN:
                                        buff = b''
                                        while True:
                                            try:
                                                recv_buff = cur_socket_info['socket'].recv(2048)
                                                buff += recv_buff
                                                if not recv_buff:
                                                    logger.info('connection disconnected')
                                                    if 'disconnected_callback' in self.socket_fileno_info[fd_fileno]['callback'].keys():
                                                        self.socket_fileno_info[fd_fileno]['callback']['disconnected_callback'](self.socket_fileno_info[fd_fileno]['user_fd'])
                                                    self._RmSocket__remove_socket_fileno_info(fd_fileno)
                                                    self.epoll_obj.unregister(fd_fileno)
                                                break
                                            except socket.error as e:
                                                try:
                                                    if e.errno == errno.EAGAIN:
                                                        logger.info('READ DATA EAGAIN ERROR')
                                                    else:
                                                        logger.fatal(traceback.format_exc())
                                                finally:
                                                    e = None
                                                    del e
                                                break
                                            except Exception as e:
                                                try:
                                                    logger.fatal(traceback.format_exc())
                                                finally:
                                                    e = None
                                                    del e
                                                break

                                        if recv_buff:
                                            if 'recv_callback' in cur_socket_info['callback'].keys():
                                                cur_socket_info['callback']['recv_callback'](cur_socket_info['user_fd'], recv_buff.decode('utf-8'))
                                            else:
                                                if cur_socket_info['recv_msgq'].full():
                                                    cur_socket_info['recv_msgq'].get()
                                                cur_socket_info['recv_msgq'].put((addr, recv_buff.decode('utf-8')))
                                    else:
                                        if event & select.EPOLLOUT:
                                            send_info = None
                                            while True:
                                                if self.socket_fileno_info[fd_fileno]['send_msgq'].qsize() > 0:
                                                    send_info = self.socket_fileno_info[fd_fileno]['send_msgq'].get()
                                                    while send_info == None:
                                                        pass

                                                    if 'send_callback' in cur_socket_info['callback'].keys():
                                                        cur_socket_info['callback']['send_callback'](cur_socket_info['user_fd'], send_info[0])
                                                    try:
                                                        cur_socket_info['socket'].send(send_info[0].encode('utf-8'))
                                                    except Exception as e:
                                                        try:
                                                            logger.fatal(traceback.format_exc())
                                                            if not self.socket_fileno_info[fd_fileno]['send_msgq'].full():
                                                                self.socket_fileno_info[fd_fileno]['send_msgq'].put(send_info)
                                                        finally:
                                                            e = None
                                                            del e
                                                        break

                                            self.epoll_obj.modify(fd_fileno, select.EPOLLIN)
                                        else:
                                            self.epoll_obj.modify(fd_fileno, 0)
                        else:
                            if cur_socket_info['type'] == self.UDP_MODE:
                                if event & select.EPOLLOUT:
                                    send_info = None
                                    while True:
                                        if self.socket_fileno_info[fd_fileno]['send_msgq'].qsize() > 0:
                                            send_info = self.socket_fileno_info[fd_fileno]['send_msgq'].get()
                                            while send_info == None:
                                                pass

                                            ip_port = send_info[1]
                                            if ip_port == None:
                                                if 'default_target_addr' in cur_socket_info.keys():
                                                    ip_port = cur_socket_info['default_target_addr']
                                            if 'send_callback' in cur_socket_info['callback'].keys():
                                                cur_socket_info['callback']['send_callback'](cur_socket_info['user_id'], send_info[0])
                                            try:
                                                cur_socket_info['socket'].sendto(send_info[0].encode('utf-8'), ip_port)
                                            except Exception as e:
                                                try:
                                                    if e.errno == errno.EAGAIN:
                                                        logger.info('WRITE DATA EAGAIN ERROR')
                                                    else:
                                                        logger.fatal(traceback.format_exc())
                                                    if not self.socket_fileno_info[fd_fileno]['send_msgq'].full():
                                                        self.socket_fileno_info[fd_fileno]['send_msgq'].put(send_info)
                                                finally:
                                                    e = None
                                                    del e
                                                break

                                    self.epoll_obj.modify(fd_fileno, select.EPOLLIN)
                                else:
                                    if event & select.EPOLLIN:
                                        buff = b''
                                        while True:
                                            try:
                                                recv_buff, addr = cur_socket_info['socket'].recvfrom(2048)
                                                buff += recv_buff
                                            except socket.error as e:
                                                try:
                                                    if e.errno == errno.EAGAIN:
                                                        logger.info('RECV DATA EAGAIN ERROR')
                                                    else:
                                                        logger.fatal(traceback.format_exc())
                                                finally:
                                                    e = None
                                                    del e
                                                break
                                            except Exception as e:
                                                try:
                                                    logger.fatal(traceback.format_exc())
                                                finally:
                                                    e = None
                                                    del e
                                                break

                                        if buff:
                                            if 'recv_callback' in cur_socket_info['callback'].keys():
                                                cur_socket_info['callback']['recv_callback'](addr, cur_socket_info['user_fd'], buff.decode('utf-8'))
                                            else:
                                                if cur_socket_info['recv_msgq'].full():
                                                    cur_socket_info['recv_msgq'].get()
                                                cur_socket_info['recv_msgq'].put((addr, recv_buff.decode('utf-8')))
                                    else:
                                        self.epoll_obj.modify(fd_fileno, 0)
                            else:
                                logger.info('KNOW SOCKET %s' % cur_socket_info)

        logger.info('exit')