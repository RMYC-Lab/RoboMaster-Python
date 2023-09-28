# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: .\src\test\rm_log.py
# Compiled at: 2022-01-12 15:45:07
# Size of source mod 2**32: 3465 bytes
import logging, os, sys, rm_logger, rm_path
DEFAULT_LOG_DIR_PATH = '/Users/ares.li/Documents/SC/'
DEFAULT_DJI_SCRATCH_FILE_OUT_LEVEL = logging.ERROR
DEFAULT_DJI_SCRATCH_STREAM_OUT_LEVEL = logging.DEBUG
DEFAULT_DJI_SCRIPT_FILE_OUT_LEVEL = logging.ERROR
DEFAULT_DJI_SCRIPT_STREAM_OUT_LEVEL = logging.DEBUG
DEFAULT_LOGGER = logging
DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR
FATAL = logging.FATAL
dji_scratch_logger = logging.getLogger('dji_scratch_logger')
dji_script_logger = logging.getLogger('dji_script_logger')
logger = logging.getLogger('dji_scratch_logger')

def logger_get_path():
    dataPath = rm_path.get_data_path()
    return os.path.join(dataPath, 'SCLogs/')


def dji_scratch_logger_get():
    global dji_scratch_logger
    dji_scratch_logger = logging.getLogger('dji_scratch_logger')
    return dji_scratch_logger


def dji_script_logger_get():
    global dji_script_logger
    dji_script_logger = logging.getLogger('dji_script_logger')
    return dji_script_logger


def logger_file_out_path_generate(file_name):
    dir_path = logger_get_path()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_list = os.listdir(dir_path)
    num = 0
    for name in file_list:
        if file_name in name:
            num_str = name.replace(file_name + '_', '').replace('.log', '')
            if num_str.isdigit():
                num = max(num, int(num_str))
    else:
        if num > 100:
            for name in file_list:
                os.remove(dir_path + name)
            else:
                num = 0

        return dir_path + file_name + '_' + str(num + 1) + '.log'


def logger_init(logger, event_client, file_out_level=DEFAULT_DJI_SCRATCH_FILE_OUT_LEVEL, stream_out_level=DEFAULT_DJI_SCRATCH_STREAM_OUT_LEVEL):
    """
    Args:
        file_out: the logger output fil
        file_out_level: the lowest level to output to file_out
    """
    for handler in logger.handlers:
        logger.info('logger remove ------------------------------------')
        logger.removeHandler(handler)
        handler.close()
    else:
        logger.setLevel(logging.DEBUG)
        if stream_out_level != None:
            stream_out = logging.StreamHandler()
            stream_out.setLevel(stream_out_level)
            stream_out_formatter = logging.Formatter('[%(levelname)-5s]:[%(module)-15.15s]:[%(lineno)-4s]: %(message)s')
            stream_out.setFormatter(stream_out_formatter)
            logger.addHandler(stream_out)
        if file_out_level != None:
            file_out = logging.FileHandler((logger_file_out_path_generate('dji_scratch.log')), encoding='utf-8')
            file_out.setLevel(file_out_level)
            file_out_formatter = logging.Formatter('[%(asctime)s]:[%(levelname)-5s]:[%(module)-15s]:[%(lineno)-4s]:[%(funcName)-15s]:%(message)s')
            file_out.setFormatter(file_out_formatter)
            logger.addHandler(file_out)
        return logger


def logger_close():
    for handler in logger.handlers:
        logger.info('---logger close---')
        logger.removeHandler(handler)
        handler.close()