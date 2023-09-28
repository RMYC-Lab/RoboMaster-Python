# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: .\src\test\duss_event_msg.py
# Compiled at: 2021-08-19 19:18:58
# Size of source mod 2**32: 7055 bytes
import tools, duml_crc, rm_define, duml_cmdset, random, operator, rm_log
logger = rm_log.dji_scratch_logger_get()
DUSS_MB_PACKAGE_V1_HEAD_SIZE = 11
DUSS_MB_PACKAGE_V1_CRC_SIZE = 2
DUSS_MB_PACKAGE_V1_CRCH_INIT = 119
DUSS_MB_PACKAGE_V1_CRC_INIT = 13970

def hostid2packid(host_id):
    host_id = int(host_id)
    host_id = int(host_id / 100) & 31 | host_id % 100 << 5 & 224
    return [
     host_id]


def _seqid2packid(seqid):
    seqid = tools.to_uint16(seqid)
    seqid_l = seqid & 255
    seqid_h = seqid >> 8 & 255
    return [
     seqid_l, seqid_h]


data_convert_func = {'int8':tools.int8_to_byte, 
 'uint8':tools.uint8_to_byte, 
 'int16':tools.int16_to_byte, 
 'uint16':tools.uint16_to_byte, 
 'int32':tools.int32_to_byte, 
 'uint32':tools.uint32_to_byte, 
 'float':tools.float_to_byte, 
 'double':tools.float_to_byte, 
 'string':tools.string_to_byte, 
 'bytes':tools.bytes_to_byte, 
 'bool':tools.bool_to_byte}

class EventMsg(object):

    def __init__(self, sender):
        self.default_cmdset = duml_cmdset.DUSS_MB_CMDSET_RM
        self.default_cmdtype = duml_cmdset.REQ_PKG_TYPE | duml_cmdset.NEED_ACK_TYPE
        self.default_receiver = 0
        self.default_moduleid = 0
        self.module_id = 0
        self.seq_num = random.randint(1000, 2000)
        self.cmd_type = 0
        self.cmd_set = 0
        self.cmd_id = 0
        self.sender = sender
        self.receiver = 0
        self.debug = False
        self.length = 0
        self.data_buff = []
        self.data = tools.create_order_dict()

    def set_default_cmdset(self, cmdset):
        self.default_cmdset = cmdset

    def set_default_cmdtype(self, type):
        self.default_cmdtype = type

    def set_default_receiver(self, receiver):
        self.default_receiver = receiver

    def set_default_moduleid(self, moduleid):
        self.default_moduleid = moduleid

    def init(self):
        self.module_id = self.default_moduleid
        self.cmd_set = self.default_cmdset
        self.cmd_type = self.default_cmdtype
        self.receiver = self.default_receiver
        self.seq_num = self.seq_num + 1
        self.data.clear()

    def clear(self):
        self.data.clear()
        self.data_buff = []

    def append(self, name, type, data):
        self.data[name] = {type: data}

    def get_value(self, name):
        if name in self.data.keys():
            return list(self.data[name].values())[0]

    def get_data(self):
        self.data_buff = []
        for name in self.data:
            type = list(self.data[name].keys())[0]
            try:
                self.data_buff.extend(data_convert_func[type](self.data[name][type]))
            except Exception as e:
                try:
                    logger.fatal('msg buff data parse error')
                    logger.fatal(e)
                finally:
                    e = None
                    del e

    def pack(self):
        self.data_buff = []
        self.get_data()
        self.length = len(self.data_buff)
        pack_size = self.length + DUSS_MB_PACKAGE_V1_HEAD_SIZE + DUSS_MB_PACKAGE_V1_CRC_SIZE
        verlen = [pack_size & 255] + [(1024 | pack_size) >> 8]
        crc_h_data = [85] + verlen
        crc_h_t = duml_crc.duss_util_crc8_append(crc_h_data, DUSS_MB_PACKAGE_V1_CRCH_INIT)
        crc_data = [
         85] + verlen + crc_h_t + hostid2packid(self.sender) + hostid2packid(self.receiver) + _seqid2packid(self.seq_num) + [
         self.cmd_type] + [
         self.cmd_set] + [
         self.cmd_id] + self.data_buff
        crc_t = duml_crc.duss_util_crc16_append(crc_data, DUSS_MB_PACKAGE_V1_CRC_INIT)
        package_combine = crc_data + crc_t
        if self.debug:
            logger.info(list(map(lambda x: hex(x)
, package_combine)))
        package_byte = tools.pack_to_byte(package_combine)
        return package_byte

    def set_data(self, data):
        self.data_buff = data

    def unpack(self):
        return unpack(self.recv_buff)


def unpack_msg_header(msg_buff):
    pack = tools.unpack_to_hex(msg_buff)
    logger.info('MSG HEADER = ' + str(pack))
    if pack[0] != 85:
        logger.fatal('Fatal Error in duss_event_msg, header magic num failed!')
        return
    crc_h_data = pack[0:3]
    crc_h_t = duml_crc.duss_util_crc8_calc(crc_h_data, DUSS_MB_PACKAGE_V1_CRCH_INIT)
    if crc_h_t != pack[3]:
        logger.fatal('Fatal Error in duss_event_msg, crc header failed!')
        return
    msg_len = (pack[2] & 3) * 256 | pack[1]
    return msg_len


def unpack_msg_data(msg_buff):
    pack = tools.unpack_to_hex(msg_buff)
    msg = {}
    return msg


def unpack(recv_buff):
    if len(recv_buff) < 4:
        return
    pack = []
    pack = tools.unpack_to_hex(recv_buff)
    if pack[0] != 85:
        logger.fatal('Fatal Error in duss_event_msg, header magic num failed!')
        return
    crc_h_data = pack[0:3]
    crc_h_t = duml_crc.duss_util_crc8_calc(crc_h_data, DUSS_MB_PACKAGE_V1_CRCH_INIT)
    if crc_h_t != pack[3]:
        logger.fatal('Fatal Error in duss_event_msg, crc header failed!')
        return
    crc_data = pack[0:len(pack) - 2]
    crc_t = duml_crc.duss_util_crc16_append(crc_data, DUSS_MB_PACKAGE_V1_CRC_INIT)
    if True != operator.eq(crc_t, pack[len(pack) - 2:len(pack)]):
        logger.fatal('Fatal Error in duss_event_msg, crc message failed!')
        return
    msg = {}
    msg['len'] = (pack[2] & 3) * 256 | pack[1]
    if len(recv_buff) != msg['len']:
        logger.fatal('FATAL ERROR: NOT ENOUPH MSG BUFF TO UNPACK')
        return
    msg['sender'] = int(str(pack[4] & 31) + '0' + str(pack[4] >> 5 & 7))
    msg['receiver'] = int(str(pack[5] & 31) + '0' + str(pack[5] >> 5 & 7))
    msg['send_id'] = pack[4] & 31
    msg['send_module_id'] = pack[4] >> 5 & 7
    msg['recv_id'] = pack[5] & 31
    msg['recv_module_id'] = pack[5] >> 5 & 7
    msg['seq_num'] = pack[7] * 256 | pack[6]
    msg['cmd_type'] = pack[8] >> 5 & 3
    msg['cmd_set'] = pack[9]
    msg['cmd_id'] = pack[10]
    msg['data'] = pack[11:len(pack) - 2]
    if pack[8] & 128 == 0:
        msg['ack'] = False
    else:
        msg['ack'] = True
    return msg


def unpack2EventMsg(msg):
    event_msg = EventMsg(msg['sender'])
    event_msg.receiver = msg['receiver']
    event_msg.cmd_set = msg['cmd_set']
    event_msg.cmd_id = msg['cmd_id']
    event_msg.seq_num = msg['seq_num']
    event_msg.cmd_type = msg['cmd_type']
    event_msg.data_buff = msg['data']
    return event_msg