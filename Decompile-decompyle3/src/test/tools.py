# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: .\src\test\tools.py
# Compiled at: 2021-08-24 17:37:28
# Size of source mod 2**32: 15965 bytes
import struct, time, hashlib, json, logging, os
from threading import Timer
import inspect, ctypes, random, collections, binascii, rm_define, subprocess, platform

def to_uint8(data):
    data = int(round(data))
    return data & 255


def to_uint16(data):
    data = int(round(data))
    return data & 65535


def to_uint32(data):
    data = int(round(data))
    return data & 4294967295


def to_int8(data):
    data = int(round(data))
    if data >> 7 == 1:
        return -(256 - data)
    return data


def to_int16(data):
    data = int(round(data))
    if data >> 15 == 1:
        return -(65536 - data)
    return data


def to_int32(data):
    data = int(round(data))
    if data >> 31 == 1:
        return -(4294967296 - data)
    return data


def pack_to_byte(data):
    return (struct.pack)('>%dB' % len(data), *data)


def unpack_to_hex(data):
    return list(struct.unpack('%dB' % len(data), data))


def byte2hex(bins):
    return ''.join(['%02x' % x for x in bins]).strip()


def byte2HEX(bins):
    return ''.join(['%02X' % x for x in bins]).strip()


def list_hex2str(list_data):
    out = []
    for data_t in list_data:
        out.append(hex(data_t))
    else:
        return out


def dict_value2hex_list(dict_data, key_tuple):
    out = []
    for key in key_tuple:
        out = out + dict_data[key]
    else:
        return out


def dict_value2str_list(dict_data, key_tuple):
    out = []
    out = dict_value2str_list(dict_data, key_tuple)
    out = list_hex2str(out)
    return out


def bool_to_byte(data):
    if not data == False:
        if data == 0 or data == None:
            return [
             0]
        return [
         1]


def int8_to_byte(data):
    data = to_int8(data)
    return [
     data]


def int16_to_byte(data):
    data = to_int16(data)
    data_l = data & 255
    data_h = data >> 8 & 255
    return [
     data_l, data_h]


def int32_to_byte(data):
    data = to_int32(data)
    data_l0 = data & 255
    data_l1 = data >> 8 & 255
    data_h0 = data >> 16 & 255
    data_h1 = data >> 24 & 255
    return [
     data_l0, data_l1, data_h0, data_h1]


def uint8_to_byte(data):
    data = to_uint8(data)
    return [
     data]


def uint16_to_byte(data):
    data = to_uint16(data)
    data_l = data & 255
    data_h = data >> 8 & 255
    return [
     data_l, data_h]


def uint32_to_byte(data):
    data = to_uint32(data)
    data_l0 = data & 255
    data_l1 = data >> 8 & 255
    data_h0 = data >> 16 & 255
    data_h1 = data >> 24 & 255
    return [
     data_l0, data_l1, data_h0, data_h1]


def float_to_byte(data):
    data = float(data)
    out = []
    data = binascii.hexlify(struct.pack('>f', data)).decode('utf-8')
    for i in (6, 4, 2, 0):
        out.append(int(data[i:i + 2], 16))
    else:
        return out


def string_to_byte(data):
    out = []
    for i in range(len(data)):
        out.append(ord(data[i]))
    else:
        return out


def bytes_to_byte(data):
    return data


def byte_to_uint8(data):
    return data[0]


def byte_to_uint16(data):
    out = data[0] | data[1] << 8
    return out


def byte_to_uint32(data):
    out = data[0] | data[1] << 8 | data[2] << 16 | data[3] << 24
    return out


def byte_to_int8(data):
    out = to_int8(byte_to_uint8(data))
    return out


def byte_to_int16(data):
    out = to_int16(byte_to_uint16(data))
    return out


def byte_to_int32(data):
    out = to_int32(byte_to_uint32(data))
    return out


def byte_to_float(data):
    b0 = struct.pack('B', to_uint8(data[0]))
    b1 = struct.pack('B', to_uint8(data[1]))
    b2 = struct.pack('B', to_uint8(data[2]))
    b3 = struct.pack('B', to_uint8(data[3]))
    return struct.unpack('f', b0 + b1 + b2 + b3)[0]


def byte_to_string(data):
    out = ''
    for ch in data:
        out = out + chr(ch)
    else:
        return out


def data_limit(data, min_data, max_data):
    return max(min(max_data, data), min_data)


def string_limit(data, max_data):
    return data[0:max_data]


def wait(ms):
    time.sleep(ms / 1000.0)


def md5_check(string_hex_list, md5_hex_list):
    string = pack_to_byte(string_hex_list)
    md5_byte = pack_to_byte(md5_hex_list)
    md5_str = md5_byte.decode('utf-8')
    md5_obj = hashlib.md5()
    md5_obj.update(string)
    return md5_str == md5_obj.hexdigest()[8:-8]


def load_route_table(json_file, service_name, client_name):

    def read_route_file(json_file):
        file_fd = open(json_file, 'r')
        json_str = file_fd.read()
        route_table = json.loads(json_str)
        return route_table

    def get_host_device(route_table):
        host_name = route_table['host']
        host_index = route_table['index']
        route_table.pop('host')
        route_table.pop('index')
        return (
         route_table, host_name, host_index)

    def get_local_V1_route(route_table):
        client_name = {'camera':rm_define.camera_id, 
         'mvision':rm_define.vision_id, 
         'vt_air':rm_define.hdvt_uav_id, 
         've_air':rm_define.system_scratch_id}
        n_route_table = {}
        for device_index in route_table.keys():
            target = route_table[device_index]['target']
            status = route_table[device_index]['status']
            channel = route_table[device_index]['channel']
            protocol = route_table[device_index]['protocol']
            if status == 1:
                if channel == 'local':
                    if protocol == 'v1':
                        if target in client_name.keys():
                            direct_route = route_table[device_index]['local']
                            target_host = direct_route['direct_host']
                            target_index = direct_route['index']
                            if target_host in client_name.keys():
                                target_address = '\x00/duss/mb/' + senderid2hostid(client_name[target_host])
                                n_route_table[client_name[target]] = {'target_address':target_address,  'channel':channel,  'protocol':protocol}
        else:
            return n_route_table

    route_table = read_route_file(json_file)
    route_table = route_table[service_name]['mb_route_table'][client_name]
    route_table, host_name, host_index = get_host_device(route_table)
    target_table = get_local_V1_route(route_table)
    return (
     target_table, host_name, host_index)


global_timer_obj = None

def get_timer(freq, func, *arg, **kw):
    global global_timer_obj
    if global_timer_obj == None:
        global_timer_obj = UnitTimer()
    t = ScratchTimer(freq, func, *arg, **kw)
    global_timer_obj.add_timer(t)
    return t


def close_timer():
    if global_timer_obj != None:
        global_timer_obj.close()


def set_tools_msg_callback(callback):
    global global_timer_obj
    if global_timer_obj == None:
        global_timer_obj = UnitTimer()
    global_timer_obj.set_msg_callback(callback)


class UnitTimer(object):

    def __init__(self):
        self.unit_timer_dict = {}
        self.unit_timer_t = 0.01
        self.count_t = 0
        self.timer_obj = None
        self.msg_callback = None

    def set_msg_callback(self, callback):
        self.msg_callback = callback

    def add_timer(self, timer_obj):
        if timer_obj not in self.unit_timer_dict.keys():
            self.unit_timer_dict[timer_obj] = int(timer_obj.get_freq() / self.unit_timer_t)
        if self.timer_obj == None:
            if len(self.unit_timer_dict) != 0:
                self.timer_obj = Timer(self.unit_timer_t, self.process_timer, ())
                self.timer_obj.start()

    def delete_timer(self, timer_obj):
        if timer_obj in self.unit_timer_dict.keys():
            self.unit_timer_dict.pop(timer_obj)
        if len(self.unit_timer_dict) == 0:
            self.timer_obj = None

    def process_timer(self):
        start_time = time.time()
        self.count_t += 1
        unit_timer_dict = dict(self.unit_timer_dict)
        for timer_obj, t in unit_timer_dict.items():
            if timer_obj.is_alive():
                while self.count_t % t == 0:
                    timer_obj._call()

                self.delete_timer(timer_obj)
        else:
            if len(self.unit_timer_dict) == 0:
                self.timer_obj = None
                return
            if self.count_t >= 6000:
                self.count_t = 0
            diff_time = time.time() - start_time
            timer_t = self.unit_timer_t - diff_time
            if timer_t < 0:
                timer_t = 0
            self.timer_obj = Timer(timer_t, self.process_timer, ())
            self.timer_obj.start()

    def close(self):
        self.unit_timer_dict = {}


class ScratchTimer(object):

    def __init__(self, freq, func, *arg, **kw):
        self.freq = freq
        self.func = func
        self.arg = arg
        self.kw = kw
        self.start_flag = False
        self.alive_flag = True
        self.join_flag = True

    def start(self):
        if self.alive_flag:
            self.start_flag = True

    def stop(self):
        self.start_flag = False

    def join(self):
        while True:
            if not self.join_flag:
                time.sleep(0.01)

    def destory(self):
        self.alive_flag = False

    def _call(self):
        if self.alive_flag:
            if self.start_flag:
                self.join_flag = False
                (self.func)(*self.arg, **self.kw)
                self.join_flag = True

    def is_alive(self):
        return self.alive_flag

    def is_start(self):
        return self.start_flag

    def get_freq(self):
        return self.freq


def mutex():
    return threading.Lock()


def cur_time():
    print('time_stamp:', time.time())
    print(time.asctime(time.localtime(time.time())))


def check_and_retry(func, condi, times):
    i = times
    while i != 0:
        while func != condi:
            i = i - 1

    if i == 0:
        return False
    return True


def async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError('invalid thread id')
    else:
        if res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)


def hostid2senderid(host_id):
    return int(hex(host_id)[0:3], 16) * 100 + int(hex(host_id)[3:5])


hostid2receiverid = hostid2senderid

def senderid2hostid(sender_id):
    host = int(sender_id / 100)
    index = sender_id % 100
    return hex((host << 8) + (index & 255))


receiverid2hostid = senderid2hostid

def task_id_generate():
    random.seed(time.time())
    task_id = random.randint(0, 255)
    return task_id


def create_order_dict():
    return collections.OrderedDict()


def get_fatal_code(fatal_msg):
    if 'division' in fatal_msg:
        if 'zero' in fatal_msg:
            return rm_define.FAT_DIV_ZERO
    if 'index out of range' in fatal_msg:
        return rm_define.FAT_LIST_OUT_OF_RANGE
    if 'has no attribute' in fatal_msg or 'is not defined' in fatal_msg:
        return rm_define.FAT_DEVICE_NOT_SUPPORT
    if 'not in list' in fatal_msg or 'from empty list' in fatal_msg:
        return rm_define.FAT_LIST_FIND_FAILUE
    if 'maximun recursion depth exceeded' in fatal_msg:
        return rm_define.FAT_STACK_OVERFLOW
    if 'Variable value type error' in fatal_msg:
        return rm_define.BLOCK_ERR_VALUE_TYPE
    if 'Variable value range error' in fatal_msg:
        return rm_define.BLOCK_ERR_VALUE_RANGE
    if 'Exit' in fatal_msg:
        return rm_define.BLOCK_RUN_SUCCESS
    return rm_define.FAT_OTHER


err_code_dict = {rm_define.camera_id: {228:rm_define.BLOCK_ERR_STORAGE_SDCARD, 
                       232:rm_define.BLOCK_ERR_NO_SDCARD, 
                       233:rm_define.BLOCK_ERR_FULL_SDCARD}, 
 
 rm_define.chassis_id: {}, 
 rm_define.mobile_id: {}, 
 rm_define.gun_id: {}, 
 rm_define.vision_id: {}, 
 rm_define.gimbal_id: {}}

def get_block_err_code(module_id, err_code):
    if module_id in err_code_dict.keys():
        if err_code in err_code_dict[module_id].keys():
            return err_code_dict[module_id][err_code]
    return err_code


def check_value_type(value, *type_args):
    for t in type_args:
        if isinstance(value, t):
            return None
    else:
        raise Exception('Variable value type error. TargetTypeTuple: %s, CurType: %s' % (type_args, type(value)))


def check_value_range(value, min_value, max_value):
    if value <= max_value:
        if value >= min_value:
            return
    raise Exception('Variable value range error. TargetRange: %s ~ %s, CurValue: %s' % (min_value, max_value, value))


def check_value_in_enum_list(value, **value_enum_dict):
    value_enum_list = value_enum_dict.values()
    if value in value_enum_list:
        return
    raise Exception('Variable value enum error. TargetEnum: %s, CurValue: %s' % (tuple(value_enum_dict.keys()), value))


def check_value_range_and_type(value, min_value, max_value, *type_args):
    check_value_type(value, *type_args)
    check_value_range(value, min_value, max_value)


def get_ip_by_dev_name(dev_name):
    ifconfig_pipe = subprocess.Popen(['busybox', 'ifconfig', dev_name], stdout=(subprocess.PIPE),
      stderr=(subprocess.PIPE))
    ifconfig_info, error = ifconfig_pipe.communicate()
    ifconfig_pipe.kill()
    if len(error) != 0:
        return
    ifconfig_info = ifconfig_info.decode('utf-8')
    inet_addr_str = ifconfig_info.split('\n')[1]
    if 'inet addr' in inet_addr_str:
        return inet_addr_str.split(':')[1].split(' ')[0]
    return


def is_station_mode():
    ps_pipe = subprocess.Popen(['ps', 'wpa'], stdout=(subprocess.PIPE),
      stderr=(subprocess.PIPE))
    ps_info, error = ps_pipe.communicate()
    ps_pipe.kill()
    if len(error) != 0:
        return
    ps_info = ps_info.decode('utf-8')
    if 'wpa_supplicant' in ps_info:
        return True
    return False


def is_ap_mode():
    return not is_station_mode()


def number_mapping(input, min_ori, max_ori, min_tar, max_tar):
    check_value_range(input, min_ori, max_ori)
    if max_ori != min_ori:
        if min_tar != max_tar:
            output = (input - min_ori) / (max_ori - min_ori) * (max_tar - min_tar) + min_tar
            return output
    if min_ori == max_ori:
        if min_tar == max_tar:
            return min_tar
    raise Exception('InputError, min_value equal max_value')


def duss_result_check(duss_result, resp, ret_code):
    if duss_result == rm_define.DUSS_SUCCESS:
        if resp['data'][0] == ret_code:
            return rm_define.SUCCESS
        return rm_define.FAILURE
    else:
        return rm_define.FAILURE


def is_windows_system():
    return 'Windows' in platform.system()