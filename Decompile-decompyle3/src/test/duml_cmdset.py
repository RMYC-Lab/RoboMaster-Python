# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.7.4 (default, Aug  9 2019, 18:34:13) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: .\src\test\duml_cmdset.py
# Compiled at: 2022-01-12 15:45:07
# Size of source mod 2**32: 48911 bytes
REQ_PKG_TYPE = 0
ACK_PKG_TYPE = 128
NO_ACK_TYPE = 0
NEED_ACK_TYPE = 64
NEED_ACK_NO_FINISH_TYPE = 32
NO_ENC_TYPE = 0
AES_128_ENC_TYPE = 1
CUSTOM_ENC_TYPE = 2
XOR_ENC_TYPE = 3
DES_56_ENC_TYPE = 4
DES_112_ENC_TYPE = 5
AES_192_ENC_TYPE = 6
AES_256_ENC_TYPE = 7
MSG_TIMEOUT_FOREVER = 0
MSG_DEFAULT_TIMEOUT = 0.25
TASK_ID_MIN = 1
TASK_ID_MAX = 255
TASK_FREQ_10Hz = 2
TASK_FREQ_5Hz = 1
TASK_FREQ_1Hz = 0
TASK_CTRL_START = 0
TASK_CTRL_STOP = 1
DUSS_MB_CMDSET_COMMON = 0
DUSS_MB_CMDSET_SPECIAL = 1
DUSS_MB_CMDSET_CAMERA = 2
DUSS_MB_CMDSET_FC = 3
DUSS_MB_CMDSET_GIMBAL = 4
DUSS_MB_CMDSET_CENTER = 5
DUSS_MB_CMDSET_RC = 6
DUSS_MB_CMDSET_WIFI = 7
DUSS_MB_CMDSET_DM368 = 8
DUSS_MB_CMDSET_HDVT = 9
DUSS_MB_CMDSET_VISION = 10
DUSS_MB_CMDSET_SIM = 11
DUSS_MB_CMDSET_ESC = 12
DUSS_MB_CMDSET_SMART_BATTERY = 13
DUSS_MB_CMDSET_HDVT_1765_GND = 14
DUSS_MB_CMDSET_S_TO_P_AIR = 15
DUSS_MB_CMDSET_S_TO_P_GND = 16
DUSS_MB_CMDSET_ADSB = 17
DUSS_MB_CMDSET_BVISION = 18
DUSS_MB_CMDSET_FPGA_AIR = 19
DUSS_MB_CMDSET_FPGA_GND = 20
DUSS_MB_CMDSET_GLASS = 21
DUSS_MB_CMDSET_MAVLINK = 22
DUSS_MB_CMDSET_WATCH = 23
DUSS_MB_CMDSET_PERCEPTION = 36
DUSS_MB_CMDSET_ROBOTIC_ARM = 51
DUSS_MB_CMDSET_RM = 63
DUSS_MB_CMDSET_VIRTUAL_BUS = 72
DUSS_MB_CMDSET_EDU_PLATFORM = 93
DUSS_MB_CMDSET_MAX = 33
DUSS_MB_CMD_RM_HIT_EVENT = 2
DUSS_MB_CMD_RM_SPECIAL_CONTROL = 4
DUSS_MB_CMD_RM_WATER_GUN_PARM_SET = 5
DUSS_MB_CMD_RM_ARMOR_VOICE_PARAMS_SET = 7
DUSS_MB_CMD_RM_GAME_STATE_SYNC = 9
DUSS_MB_CMD_RM_GAMECTRL_CMD = 10
DUSS_MB_CMD_RM_GAME_GROUP_CONFIG = 11
DUSS_MB_CMD_RM_GAME_START_END_CONFIG = 12
DUSS_MB_CMD_RM_SKILL_SEND = 15
DUSS_MB_CMD_RM_IR_EVENT = 16
DUSS_MB_CMD_RM_BLOOD_LED_SET = 17
DUSS_MB_CMD_RM_MODULE_STATUS_PUSH = 18
DUSS_MB_CMD_RM_WORK_MODE_SET = 25
DUSS_MB_CMD_RM_PLAY_SOUND = 26
DUSS_MB_CMD_RM_SET_SPEAKER_VOLUME = 27
DUSS_MB_CMD_RM_GET_SPEAKER_VOLUME = 28
DUSS_MB_CMD_RM_AUDIO_TO_APP = 29
DUSS_MB_CMD_RM_SET_AUDIO_STATUS = 30
DUSS_MB_CMD_RM_WHEEL_SPEED_SET = 32
DUSS_MB_CMD_RM_SPEED_SET = 33
DUSS_MB_CMD_RM_FOLLOW_MODE_SET = 34
DUSS_MB_CMD_RM_FPV_MODE_SPEED_SET = 35
DUSS_MB_CMD_RM_GROUND_MODE_SET = 36
DUSS_MB_CMD_RM_POSITION_SET = 37
DUSS_MB_CMD_RM_WHEEL_STATUS_SET = 38
DUSS_MB_CMD_RM_WHEEL_STATUS_GET = 39
DUSS_MB_CMD_RM_SPEED_MODE_SET = 40
DUSS_MB_CMD_RM_CHASSIS_POSITION_TASK_PUSH = 42
DUSS_MB_CMD_RM_SET_CHASSIS_PWM_FREQ = 43
DUSS_MB_CMD_RM_GET_CHASSIS_PWM_FREQ = 45
DUSS_MB_CMD_RM_ARMOR_GET_STATE = 49
DUSS_MB_CMD_RM_ARMOR_LED_SET = 50
DUSS_MB_CMD_RM_LED_COLOR_SET = 51
DUSS_MB_CMD_RM_SET_CHASSIS_PWM_VALUE = 60
DUSS_MB_CMD_RM_GET_CHASSIS_PWM_VALUE = 61
DUSS_MB_CMD_RM_SET_TANK_WORK_MODE = 70
DUSS_MB_CMD_RM_GET_TANK_WORK_MODE = 71
DUSS_MB_CMD_RM_EXIT_LOW_POWER_MODE = 76
DUSS_MB_CMD_RM_SHOOT_EVENT = 80
DUSS_MB_CMD_RM_SHOOT_CMD = 81
DUSS_MB_CMD_RM_SHOOT_GET_STATE = 82
DUSS_MB_CMD_RM_SHOOT_MODE_SET = 83
DUSS_MB_CMD_RM_SHOOT_MODE_GET = 84
DUSS_MB_CMD_RM_GUN_LED_SET = 85
DUSS_MB_CMD_RM_FC_RMC = 96
DUSS_MB_CMD_RM_FC_GET_STATE = 97
DUSS_MB_CMD_RM_SCRIPT_DOWNLOAD_DATA = 161
DUSS_MB_CMD_RM_SCRIPT_DOWNLOAD_FINSH = 162
DUSS_MB_CMD_RM_SCRIPT_CTRL = 163
DUSS_MB_CMD_RM_SCRIPT_CUSTOM_INFO_PUSH = 164
DUSS_MB_CMD_RM_SCRIPT_BLOCK_STATUS_PUSH = 165
DUSS_MB_CMD_RM_SCRIPT_PARAMS_INFO_PUSH = 166
DUSS_MB_CMD_RM_SCRIPT_LOG_INFO = 167
DUSS_MB_CMD_RM_CUSTOM_SKILL_CONFIG_QUERY = 168
DUSS_MB_CMD_RM_SCRIPT_LOCAL_SUB_SERVICE = 169
DUSS_MB_CMD_RM_SUB_MOBILE_INFO = 171
DUSS_MB_CMD_RM_MOBILE_INFO_PUSH = 172
DUSS_MB_CMD_RM_SCRATCH_AUTO_TEST = 175
DUSS_MB_CMD_RM_GIMBAL_DEGREE_SET = 176
DUSS_MB_CMD_RM_GIMBAL_POSITION_TASK_PUSH = 177
DUSS_MB_CMD_RM_GIMBAL_RESET_POSITION_SET = 178
DUSS_MB_CMD_RM_PLAY_SOUND_TASK = 179
DUSS_MB_CMD_RM_PLAY_SOUND_TASK_PUSH = 180
DUSS_MB_CMD_RM_ROBOTIC_ARM_POSITION_TASK_SET = 181
DUSS_MB_CMD_RM_ROBOTIC_ARM_POSITION_TASK_PUSH = 182
DUSS_MB_CMD_RM_SERVO_ANGLE_TASK_SET = 183
DUSS_MB_CMD_RM_SERVO_ANGLE_TASK_PUSH = 184
DUSS_MB_CMD_RM_CUSTOM_UI_ATTRIBUTE_SET = 186
DUSS_MB_CMD_RM_CUSTOM_UI_ACTION_TRIGGER = 187
DUSS_MB_CMD_RM_CUSTOM_SOUND_CONVERT = 188
DUSS_MB_CMD_RM_LINK_STATE_PUSH = 208
DUSS_MB_CMD_RM_SDK_MODE_SET = 209
DUSS_MB_CMD_RM_STREAM_CTRL = 210
DUSS_MB_CMD_RM_UART_CONFIG = 192
DUSS_MB_CMD_RM_UART_MSG = 193
DUSS_MB_CMD_RM_UART_STATUS_PUSH = 194
DUSS_MB_CMD_RM_MEDIA_SOUND_RECOGNIZE_SET = 227
DUSS_MB_CMD_RM_MEDIA_SOUND_RECOGNIZE_PUSH = 228
DUSS_MB_CMD_RM_MEDIA_CAMERA_BRIGHTNESS_GET = 229
DUSS_MB_CMD_RM_GET_SENSOR_ADAPTER_DATA = 240
DUSS_MB_CMD_RM_SET_SENSOR_ADAPTER_PARAM = 241
DUSS_MB_CMD_RM_GET_SENSOR_ADAPTER_PARAM = 242
DUSS_MB_CMD_RM_PUSH_SENSOR_ADAPTER_IO_EVENT = 243
DUSS_MB_CMD_RM_PUSH_SENSOR_ADAPTER_ADC_VALUE = 244
DUSS_MB_CMD_RM_PRODUCT_ATTRIBUTE_GET = 254
DUSS_MB_RET_OK = 0
DUSS_MB_RET_ACK = 1
DUSS_MB_RET_FINSH = 208
DUSS_MB_RET_RESEND_REQUEST = 209
DUSS_MB_RET_MD5_CHECK_FAILUE = 210
DUSS_MB_RET_DOWNLOAD_FAILUE = 211
DUSS_MB_RET_NO_EXIST_DSP = 212
DUSS_MB_RET_NOT_IN_TRANSFER = 213
DUSS_MB_RET_SIZE_NOT_MATCH = 214
DUSS_MB_RET_SERVO_IN_ROBOTICARM_MODE = 218
DUSS_MB_RET_INVALID_CMD = 224
DUSS_MB_RET_TIMEOUT = 225
DUSS_MB_RET_OUT_OF_MEMORY = 226
DUSS_MB_RET_INVALID_PARAM = 227
DUSS_MB_RET_INVALID_STATE = 228
DUSS_MB_RET_TIME_NOT_SYNC = 229
DUSS_MB_RET_SET_PARAM_FAILED = 230
DUSS_MB_RET_GET_PARAM_FAILED = 231
DUSS_MB_RET_SDCARD_NOT_INSERTED = 232
DUSS_MB_RET_SDCARD_FULL = 233
DUSS_MB_RET_SDCARD_ERR = 234
DUSS_MB_RET_SENSOR_ERR = 235
DUSS_MB_RET_CRITICAL_ERR = 236
DUSS_MB_RET_PRARM_LEN_TOO_LONG = 237
DUSS_MB_RET_FW_SEQNUM_NOT_IN_ORDER = 240
DUSS_MB_RET_FW_EXCEED_FLASH = 241
DUSS_MB_RET_FW_CHECK_ERR = 242
DUSS_MB_RET_FW_FLASH_ERASE_ERR = 243
DUSS_MB_RET_FW_FLASH_PROGRAM_ERR = 244
DUSS_MB_RET_FW_UPDATE_STATE_ERR = 245
DUSS_MB_RET_FW_INVALID_TYPE = 246
DUSS_MB_RET_FW_UPDATE_WAIT_FINISH = 247
DUSS_MB_RET_FW_UPDATE_RC_DISCONNECT = 248
DUSS_MB_RET_FW_UPGRADE_MOTOR_RUNNING = 249
DUSS_MB_RET_HARDWARE_ERR = 250
DUSS_MB_RET_DEV_BAT_NOT_ENOUGH = 251
DUSS_MB_RET_DEV_UAV_DISCONNECT = 252
DUSS_MB_RET_FW_FLASH_ERASING = 253
DUSS_MB_RET_CHECK_CONNECTION_ERR = 254
DUSS_MB_RET_UNSPECIFIED = 255
DUSS_MB_CMD_INVALID = 0
DUSS_MB_CMD_PING = 0
DUSS_MB_CMD_GET_DEVICE_VERSION = 1
DUSS_MB_CMD_SET_PUSH_PARAM = 2
DUSS_MB_CMD_GET_PUSH_PARAM = 3
DUSS_MB_CMD_START_PUSH_PARAM = 4
DUSS_MB_CMD_SET_MULTIPLE_PRARAM = 5
DUSS_MB_CMD_GET_MULTIPLE_PRARAM = 6
DUSS_MB_CMD_FW_ENTRY = 7
DUSS_MB_CMD_FW_START = 8
DUSS_MB_CMD_FW_TRAMSMIT = 9
DUSS_MB_CMD_FW_FINISH = 10
DUSS_MB_CMD_DEVICE_REBOOT = 11
DUSS_MB_CMD_SET_DEVICE_VERSION = 13
DUSS_MB_CMD_COM_HEARTBEAT = 14
DUSS_MB_CMD_COMPATIBILE_UPGRADE = 15
DUSS_MB_CMD_FILE_SEND_REQUEST = 34
DUSS_MB_CMD_FILE_RECV_REQUEST = 35
DUSS_MB_CMD_FILE_SENDING = 36
DUSS_MB_CMD_FILE_SEGMENT_ERROR = 37
DUSS_MB_CMD_TRANSSRV_APP2CAM = 38
DUSS_MB_CMD_TRANSSRV_CAM2APP = 39
DUSS_MB_CMD_FILE_DELETE = 40
DUSS_MB_CMD_FILE_GENERAL_TRANS = 42
DUSS_MB_CMD_ENCRYPT_CONFIG = 48
DUSS_MB_CMD_ATIVATE_CONFIG = 50
DUSS_MB_CMD_MFI_AUTH = 51
DUSS_MB_CMD_SECURITY_COMM = 52
DUSS_MB_CMD_UPDATE_DESC_PUSH = 64
DUSS_MB_CMD_UPDATE_CONTROL = 65
DUSS_MB_CMD_UPDATE_STATUS = 66
DUSS_MB_CMD_UPDATE_FINISH = 67
DUSS_MB_CMD_SLEEP_CONTROL = 69
DUSS_MB_CMD_SHUTDOWN_NOTIFICATION = 70
DUSS_MB_CMD_POWER_STATE = 71
DUSS_MB_CMD_LED_CONTROL = 72
DUSS_MB_CMD_SET_DATE = 74
DUSS_MB_CMD_GET_DATE = 75
DUSS_MB_CMD_GET_MODULE_SYS_STATUS = 76
DUSS_MB_CMD_SET_RT = 77
DUSS_MB_CMD_GET_RT = 78
DUSS_MB_CMD_GET_CFG_FILE = 79
DUSS_MB_CMD_SET_SERIAL_NUMBER = 80
DUSS_MB_CMD_GET_SERIAL_NUMBER = 81
DUSS_MB_CMD_SET_GPS_PUSH_CONFIG = 82
DUSS_MB_CMD_PUSH_GPS_INFO = 83
DUSS_MB_CMD_GET_TEMPERATURE_INFO = 84
DUSS_MB_CMD_GET_ALIVE_TIME = 85
DUSS_MB_CMD_PUSH_TEMPERATURE_WARNING = 86
DUSS_MB_CMD_SEND_NETWORK_INFO = 87
DUSS_MB_CMD_TIME_SYNC = 88
DUSS_MB_CMD_TEST_MODE = 89
DUSS_MB_CMD_PLAY_SOUND = 90
DUSS_MB_CMD_UAV_FLY_INFO = 92
DUSS_MB_CMD_AUTO_TEST_INFO = 96
DUSS_MB_CMD_SET_PRODUCT_NEWEST_VER = 97
DUSS_MB_CMD_GET_PRODUCT_NEWEST_VER = 98
DUSS_MB_CMD_SEND_RESERVED_KEY = 239
DUSS_MB_CMD_LOG_PUSH = 240
DUSS_MB_CMD_SELF_TEST = 241
DUSS_MB_CMD_LOG_CONTROL_GLOBAL = 242
DUSS_MB_CMD_LOG_CONTROL_MODULE = 243
DUSS_MB_CMD_TEST_START = 244
DUSS_MB_CMD_TEST_STOP = 245
DUSS_MB_CMD_TEST_QUERY_RESULT = 246
DUSS_MB_CMD_PUSH_TEST_RESULT = 247
DUSS_MB_CMD_GET_METADATA = 248
DUSS_MB_CMD_LOG_CONTROL = 250
DUSS_MB_CMD_SELFTEST_STATE = 251
DUSS_MB_CMD_SELFTEST_STATE_COUNT = 252
DUSS_MB_CMD_DUMP_FRAME_BUFFER = 253
DUSS_MB_CMD_SELF_DEFINE = 254
DUSS_MB_CMD_QUERY_DEVICE_INFO = 255
DUSS_MB_CMD_SPECIAL_APP_CONTROL = 1
DUSS_MB_CMD_SPECIAL_REMOTE_CONTROL = 2
DUSS_MB_CMD_SPECIAL_NEW_CONTROL = 3
DUSS_MB_CMD_SPECIAL_RM_CONTROL = 4
DUSS_MB_CMD_SPECIAL_UAV_LOOPBACK = 255
DUSS_MB_CMD_CAPTURE = 1
DUSS_MB_CMD_RECORD = 2
DUSS_MB_CMD_HEARTBEAT = 3
DUSS_MB_CMD_USB_CONNECT = 4
DUSS_MB_CMD_VKEY = 5
DUSS_MB_CMD_SET_WORKMODE = 16
DUSS_MB_CMD_GET_WORKMODE = 17
DUSS_MB_CMD_SET_PHOTO_FORMAT = 18
DUSS_MB_CMD_GET_PHOTO_FORMAT = 19
DUSS_MB_CMD_SET_PHOTO_QUALITY = 20
DUSS_MB_CMD_GET_PHOTO_QUALITY = 21
DUSS_MB_CMD_SET_PHOTO_STORAGE_FMT = 22
DUSS_MB_CMD_GET_PHOTO_STORAGE_FMT = 23
DUSS_MB_CMD_SET_VIDEO_FORMAT = 24
DUSS_MB_CMD_GET_VIDEO_FORMAT = 25
DUSS_MB_CMD_SET_VIDEO_QUALITY = 26
DUSS_MB_CMD_GET_VIDEO_QUALITY = 27
DUSS_MB_CMD_SET_VIDEO_STORAGE_FMT = 28
DUSS_MB_CMD_GET_VIDEO_STORAGE_FMT = 29
DUSS_MB_CMD_SET_EXPO_MODE = 30
DUSS_MB_CMD_GET_EXPO_MODE = 31
DUSS_MB_CMD_SET_SCENE_MODE = 32
DUSS_MB_CMD_GET_SCENE_MODE = 33
DUSS_MB_CMD_SET_AE_METER = 34
DUSS_MB_CMD_GET_AE_METER = 35
DUSS_MB_CMD_SET_FOCUS_MODE = 36
DUSS_MB_CMD_GET_FOCUS_MODE = 37
DUSS_MB_CMD_SET_APERTURE_SIZE = 38
DUSS_MB_CMD_GET_APERTURE_SIZE = 39
DUSS_MB_CMD_SET_SHUTTER_SPEED = 40
DUSS_MB_CMD_GET_SHUTTER_SPEED = 41
DUSS_MB_CMD_SET_ISO = 42
DUSS_MB_CMD_GET_ISO = 43
DUSS_MB_CMD_SET_WB = 44
DUSS_MB_CMD_GET_WB = 45
DUSS_MB_CMD_SET_EV_BIAS = 46
DUSS_MB_CMD_GET_EV_BIAS = 47
DUSS_MB_CMD_SET_FOCUS_REGION = 48
DUSS_MB_CMD_GET_FOCUS_REGION = 49
DUSS_MB_CMD_SET_AE_METER_REGION = 50
DUSS_MB_CMD_GET_AE_METER_REGION = 51
DUSS_MB_CMD_SET_ZOOM_PARAM = 52
DUSS_MB_CMD_GET_ZOOM_PARAM = 53
DUSS_MB_CMD_SET_FLASH_MODE = 54
DUSS_MB_CMD_GET_FLASH_MODE = 55
DUSS_MB_CMD_SET_SHARPNESS = 56
DUSS_MB_CMD_GET_SHARPNESS = 57
DUSS_MB_CMD_SET_CONTRAST = 58
DUSS_MB_CMD_GET_CONTRAST = 59
DUSS_MB_CMD_SET_SATURATION = 60
DUSS_MB_CMD_GET_SATURATION = 61
DUSS_MB_CMD_SET_HUE = 62
DUSS_MB_CMD_GET_HUE = 63
DUSS_MB_CMD_SET_FACE_DETECT = 64
DUSS_MB_CMD_GET_FACE_DETECT = 65
DUSS_MB_CMD_SET_DIGITAL_EFFECT = 66
DUSS_MB_CMD_GET_DIGITAL_EFFECT = 67
DUSS_MB_CMD_SET_DIGITAL_DENOISE = 68
DUSS_MB_CMD_GET_DIGITAL_DENOISE = 69
DUSS_MB_CMD_SET_ANTI_FLICKER = 70
DUSS_MB_CMD_GET_ANTI_FLICKER = 71
DUSS_MB_CMD_SET_MULTICAP_PARAM = 72
DUSS_MB_CMD_GET_MULTICAP_PARAM = 73
DUSS_MB_CMD_SET_CONTICAP_PARAM = 74
DUSS_MB_CMD_GET_CONTICAP_PARAM = 75
DUSS_MB_CMD_SET_HDMI_OUTPUT = 76
DUSS_MB_CMD_GET_HDMI_OUTPUT = 77
DUSS_MB_CMD_SET_QUICKVIEW_PARAM = 78
DUSS_MB_CMD_GET_QUICKVIEW_PARAM = 79
DUSS_MB_CMD_SET_OSD_PARAM = 80
DUSS_MB_CMD_GET_OSD_PARAM = 81
DUSS_MB_CMD_SET_PREVIEW_OSD_PARAM = 82
DUSS_MB_CMD_GET_PREVIEW_OSD_PARAM = 83
DUSS_MB_CMD_SET_CAMERA_TIME = 84
DUSS_MB_CMD_GET_CAMERA_TIME = 85
DUSS_MB_CMD_SET_LANGUAGE_PARAM = 86
DUSS_MB_CMD_GET_LANGUAGE_PARAM = 87
DUSS_MB_CMD_SET_CAMERA_GPS = 88
DUSS_MB_CMD_GET_CAMERA_GPS = 89
DUSS_MB_CMD_SET_DISCON_STATE = 90
DUSS_MB_CMD_GET_DISCON_STATE = 91
DUSS_MB_CMD_SET_FILE_INDEX_MODE = 92
DUSS_MB_CMD_GET_FILE_INDEX_MODE = 93
DUSS_MB_CMD_SET_AEB_PARAM = 94
DUSS_MB_CMD_GET_AEB_PARAM = 95
DUSS_MB_CMD_SET_HISTOGRAM = 96
DUSS_MB_CMD_GET_HISTOGRAM = 97
DUSS_MB_CMD_SET_V_SUBTITLES = 98
DUSS_MB_CMD_GET_V_SUBTITLES = 99
DUSS_MB_CMD_SET_V_SUBTITLES_LOG = 100
DUSS_MB_CMD_SET_MGEAR_SHUTTERSPEED_LIMIT = 101
DUSS_MB_CMD_SET_VIDEO_STANDARD = 102
DUSS_MB_CMD_GET_VIDEO_STANDARD = 103
DUSS_MB_CMD_SET_AE_LOCK_STATUS = 104
DUSS_MB_CMD_GET_AE_LOCK_STATUS = 105
DUSS_MB_CMD_SET_CAPTURE_MODE = 106
DUSS_MB_CMD_GET_CAPTURE_MODE = 107
DUSS_MB_CMD_SET_RECORD_MODE = 108
DUSS_MB_CMD_GET_RECORD_MODE = 109
DUSS_MB_CMD_SET_PANO_MODE = 110
DUSS_MB_CMD_GET_PANO_MODE = 111
DUSS_MB_CMD_GET_SYSTEM_STATE = 112
DUSS_MB_CMD_GET_SDCARD_INFO = 113
DUSS_MB_CMD_FORMAT_SDCARD = 114
DUSS_MB_CMD_GET_SDCARD_FORMAT_PROGRESS = 115
DUSS_MB_CMD_GET_FW_UPGRADE_PROGRESS = 116
DUSS_MB_CMD_GET_PHOTO_SYNC_PROGRESS = 117
DUSS_MB_CMD_GET_CAMERA_POWER_INFO = 118
DUSS_MB_CMD_SAVE_PREF = 119
DUSS_MB_CMD_LOAD_PREF = 120
DUSS_MB_CMD_PICTURE_DELETE = 121
DUSS_MB_CMD_VIDEO_CTRL = 122
DUSS_MB_CMD_SINGLE_PLAY_CTRL = 123
DUSS_MB_CMD_TELECTRL_ACTION = 124
DUSS_MB_CMD_PB_ZOOM_CTRL = 125
DUSS_MB_CMD_PB_PIC_DRAG_CTRL = 126
DUSS_MB_CMD_CAMERA_STATUS_PUSH = 128
DUSS_MB_CMD_CAP_PARA_PUSH = 129
DUSS_MB_CMD_PB_PARA_PUSH = 130
DUSS_MB_CMD_HISTOGRAM_PUSH = 131
DUSS_MB_CMD_VIDEO_NAME_PUSH = 132
DUSS_MB_CMD_RAW_CAMERA_STATUS_PUSH = 133
DUSS_MB_CMD_PANORAMA_STATUS_PUSH = 134
DUSS_MB_CMD_LENS_INFO_PUSH = 135
DUSS_MB_CMD_TIME_LAPSE_INFO_PUSH = 136
DUSS_MB_CMD_CAMERA_TRACKING_PARA_PUSH = 137
DUSS_MB_CMD_FOV_PARA_PUSH = 138
DUSS_MB_CMD_SET_RACING_LIVEVIEW_FORMAT = 139
DUSS_MB_CMD_GET_RACING_LIVEVIEW_FORMAT = 140
DUSS_MB_CMD_CALIBRATE = 144
DUSS_MB_CMD_CAL_COMPLETE = 145
DUSS_MB_CMD_GET_VCM_RANGE = 148
DUSS_MB_CMD_SET_VCM_POS = 149
DUSS_MB_CMD_GET_VCM_POS = 150
DUSS_MB_CMD_SET_V_ADT_GAMMA = 155
DUSS_MB_CMD_GET_V_ADT_GAMMA = 156
DUSS_MB_CMD_SET_FOREARM_LAMP_CONFIG = 182
DUSS_MB_CMD_GET_FOREARM_LAMP_CONFIG = 183
DUSS_MB_CMD_SET_IMAGE_ROTATION = 185
DUSS_MB_CMD_GET_IMAGE_ROTATION = 186
DUSS_MB_CMD_SET_GIMBAL_LOCK_CONFIG = 187
DUSS_MB_CMD_GET_GIMBAL_LOCK_CONFIG = 188
DUSS_MB_CMD_SET_CAM_LCD_FORMAT = 189
DUSS_MB_CMD_GET_CAM_LCD_FORMAT = 190
DUSS_MB_CMD_SET_FILE_STAR_FLAG = 191
DUSS_MB_CMD_CAM_DCF_ABSTRACT_PUSH = 209
DUSS_MB_CMD_CAPTURE_SOUND = 224
DUSS_MB_CMD_SET_CAPTURE_CONFIG = 225
DUSS_MB_CMD_GET_CAPTURE_CONFIG = 226
DUSS_MB_CMD_FC_TEST = 0
DUSS_MB_CMD_FC_GET_STATUS = 1
DUSS_MB_CMD_FC_GET_FC_PARAM = 2
DUSS_MB_CMD_FC_SET_ORIGIN_GPS = 3
DUSS_MB_CMD_FC_GET_ORIGIN_GPS = 4
DUSS_MB_CMD_FC_GET_GPS_COORDINATE = 5
DUSS_MB_CMD_FC_SET_LIMITED_PARAM = 6
DUSS_MB_CMD_FC_GET_LIMITED_PARAM = 7
DUSS_MB_CMD_FC_SET_FORBIDDEN_AREA = 8
DUSS_MB_CMD_FC_GET_FORBIDDEN_STATUS = 9
DUSS_MB_CMD_FC_GET_NVT_BATTARY_STATUS = 10
DUSS_MB_CMD_FC_SET_MOTOR_WORK_STATUS = 11
DUSS_MB_CMD_FC_GET_MOTOR_WORK_STATUS = 12
DUSS_MB_CMD_FC_SET_GPS_FOLLOW_MODE = 16
DUSS_MB_CMD_FC_GET_GPS_FOLLOW_MODE = 17
DUSS_MB_CMD_FC_GET_GPS_FOLLOW_COORDINATE = 18
DUSS_MB_CMD_FC_SUB_SERVICE_REQ = 20
DUSS_MB_CMD_FC_SUB_RESET_SERVICE_REQ = 21
DUSS_MB_CMD_FC_SUB_REMOVE_SERVICE_REQ = 22
DUSS_MB_CMD_FC_SET_GROUNDSTATION_ON = 32
DUSS_MB_CMD_FC_GET_UAV_STATUS = 33
DUSS_MB_CMD_FC_UPLOAD_AIR_ROUTE = 34
DUSS_MB_CMD_FC_DOWNLOAD_AIR_ROUTE = 35
DUSS_MB_CMD_FC_UPLOAD_WAYPOINT = 36
DUSS_MB_CMD_FC_DOWNLOAD_WAYPOINT = 37
DUSS_MB_CMD_FC_ENABLE_WAYPOINT = 38
DUSS_MB_CMD_FC_SUSPEND_RESUME_WAYPOINT = 39
DUSS_MB_CMD_FC_ONE_KEY_BACK = 40
DUSS_MB_CMD_FC_JOYSTICK = 41
DUSS_MB_CMD_FC_FUNCTION_CONTROL = 42
DUSS_MB_CMD_FC_SET_IOC_MODE_TYPE = 43
DUSS_MB_CMD_FC_GET_IOC_MODE_TYPE = 44
DUSS_MB_CMD_FC_SET_LIMIT_PARAM = 45
DUSS_MB_CMD_FC_GET_LIMIT_PARAM = 46
DUSS_MB_CMD_FC_SET_VOLTAGE_ALARM_PARAM = 47
DUSS_MB_CMD_FC_GET_VOLTAGE_ALARM_PARAM = 48
DUSS_MB_CMD_FC_SET_UAV_HOME = 49
DUSS_MB_CMD_FC_PUSH_FOOT_STOOL_STATUS = 50
DUSS_MB_CMD_FC_GET_UAV_NAME = 51
DUSS_MB_CMD_FC_SET_UAV_NAME = 52
DUSS_MB_CMD_FC_CHANGE_PARAM_PING = 53
DUSS_MB_CMD_FC_REQUEST_SN = 54
DUSS_MB_CMD_FC_GET_DEVICE_INFO = 55
DUSS_MB_CMD_FC_SET_DEVICE_INFO = 56
DUSS_MB_CMD_FC_READ_SD_DATA = 57
DUSS_MB_CMD_FC_SET_TIME_ZONE = 61
DUSS_MB_CMD_FC_PUSH_UAV_POSTURE = 66
DUSS_MB_CMD_FC_PUSH_OSD = 67
DUSS_MB_CMD_FC_PUSH_OSD_HOME = 68
DUSS_MB_CMD_FC_PUSH_GPS_SNR = 69
DUSS_MB_CMD_FC_ENABLE_GPS_SNR = 70
DUSS_MB_CMD_FC_PUSH_ENCRYPTED_PACKAGE = 73
DUSS_MB_CMD_FC_PUSH_ATT_IMU_INFO = 74
DUSS_MB_CMD_FC_PUSH_RC_STICK_VALUE = 75
DUSS_MB_CMD_FC_PUSH_FUSSED_POS_SPEED_DATA = 76
DUSS_MB_CMD_FC_PUSH_NVT_BATTARY_STATUS = 81
DUSS_MB_CMD_FC_LOW_BAT_DEPARTURE_CNF_CANECL = 82
DUSS_MB_CMD_FC_PUSH_VISUAL_AVOIDANCE_INFO = 83
DUSS_MB_CMD_FC_PUSH_GPS_INFO = 87
DUSS_MB_CMD_FC_PUSH_ATT_STICK_SPEED_POS_DATA = 88
DUSS_MB_CMD_FC_PUSH_SDK_DATA = 89
DUSS_MB_CMD_FC_PUSH_FC_DATA = 90
DUSS_MB_CMD_FC_MOTIVE_POWER_INFO = 103
DUSS_MB_CMD_FC_SET_NAVIGATION = 128
DUSS_MB_CMD_FC_START_STOP_WAYPOINT = 134
DUSS_MB_CMD_FC_PAUSE_RESUME_WAYPOINT = 135
DUSS_MB_CMD_FC_PUSH_NVT_TASK_INFO = 136
DUSS_MB_CMD_FC_PUSH_NVT_EVENT_INFO = 137
DUSS_MB_CMD_FC_START_HOTPOINT = 138
DUSS_MB_CMD_FC_CANCEL_HOTPOINT = 139
DUSS_MB_CMD_FC_PAUSE_RESUME_HOTPOINT = 140
DUSS_MB_CMD_FC_PUSH_JOYSTICK = 142
DUSS_MB_CMD_FC_START_FOLLOWME = 144
DUSS_MB_CMD_FC_CANCEL_FOLLOWME = 145
DUSS_MB_CMD_FC_PAUSE_RESUME_FOLLOWME = 146
DUSS_MB_CMD_FC_SET_GPS_FOLLOW = 147
DUSS_MB_CMD_FC_START_NEO_MISSION = 148
DUSS_MB_CMD_FC_STOP_NEO_MISSION = 149
DUSS_MB_CMD_FC_START_IOC = 151
DUSS_MB_CMD_FC_CANCEL_IOC = 152
DUSS_MB_CMD_FC_SET_DEFAULT_SPEED_DIRECTION = 153
DUSS_MB_CMD_FC_RESUME_HEADER = 155
DUSS_MB_CMD_FC_RACE_DRONE_OSD_PUSH = 162
DUSS_MB_CMD_FC_SBUS_PACKET = 170
DUSS_MB_CMD_FC_FDI_INPUT = 181
DUSS_MB_CMD_FC_CHANGE_DEV_COLOUR = 182
DUSS_MB_CMD_SET_FOREARM_LAMP = 186
DUSS_MB_CMD_FC_SUB_SERVICE_RSP = 193
DUSS_MB_CMD_GET_MOTO_SPEED = 212
DUSS_MB_CMD_RECORD_LOG = 215
DUSS_MB_CMD_REGISTER_MOTOR_ERROR_ACTION = 234
DUSS_MB_CMD_LOGOUT_MOTOR_ERROR_ACTION = 235
DUSS_MB_CMD_SET_MOTOR_ERROR_ACTION_STATUS = 236
DUSS_MB_CMD_FC_UPDATE_PARAM = 240
DUSS_MB_CMD_FC_QUERY_PARAM = 241
DUSS_MB_CMD_FC_WRITE_PARAM = 242
DUSS_MB_CMD_FC_RESTORE_DEFAULT_PARAM = 243
DUSS_MB_CMD_FC_PUSH_PARAM = 244
DUSS_MB_CMD_FC_PUSH_PARAM_PC_LOG = 246
DUSS_MB_CMD_FC_GET_PARAM_INFO_PER_HASH = 247
DUSS_MB_CMD_FC_READ_PARAM_PER_HASH = 248
DUSS_MB_CMD_FC_WRITE_PARAM_PER_HASH = 249
DUSS_MB_CMD_FC_RESET_PARAM_PER_HASH = 250
DUSS_MB_CMD_FC_PUSH_PARAM_PER_HASH = 251
DUSS_MB_CMD_FC_REQUEST_PUSH_DATA_BY_HASH_VALUE = 252
DUSS_MB_CMD_FC_REQUEST_DRONE_TYPE = 253
DUSS_MB_CMD_GIMBAL_RESERVED = 0
DUSS_MB_CMD_GIMBAL_CONTROL = 1
DUSS_MB_CMD_GIMBAL_GET_POSITION = 2
DUSS_MB_CMD_GIMBAL_SET_PARAM = 3
DUSS_MB_CMD_GIMBAL_GET_PARAM = 4
DUSS_MB_CMD_GIMBAL_PUSH_POSITION = 5
DUSS_MB_CMD_GIMBAL_PUSH_AETR = 6
DUSS_MB_CMD_GIMBAL_ADJUST_ROLL = 7
DUSS_MB_CMD_GIMBAL_CALIBRATION = 8
DUSS_MB_CMD_GIMBAL_RESERVED2 = 9
DUSS_MB_CMD_GIMBAL_EXT_CTRL_DEGREE = 10
DUSS_MB_CMD_GIMBAL_GET_EXT_CTRL_STATUS = 11
DUSS_MB_CMD_GIMBAL_EXT_CTRL_ACCEL = 12
DUSS_MB_CMD_GIMBAL_SUSPEND_RESUME = 13
DUSS_MB_CMD_GIMBAL_THIRDP_MAGN = 14
DUSS_MB_CMD_GIMBAL_SET_USER_PARAM = 15
DUSS_MB_CMD_GIMBAL_GET_USER_PARAM = 16
DUSS_MB_CMD_GIMBAL_SAVE_USER_PARAM = 17
DUSS_MB_CMD_GIMBAL_RESUME_DEFAULT_PARAM = 19
DUSS_MB_CMD_GIMBAL_PUSH_TYPE = 28
DUSS_MB_CMD_GIMBAL_DEGREE_INFO_SUBSCRIPTION = 30
DUSS_MB_CMD_GIMBAL_LOCK = 57
DUSS_MB_CMD_GIMBAL_ROTATE_CAMERA_X_AXIS = 58
DUSS_MB_CMD_GIMBAL_GET_TEMP = 69
DUSS_MB_CMD_GIMBAL_SET_MODE = 76
DUSS_MB_CMD_GIMBAL_ROTATE_EXP_CMD = 104
DUSS_MB_CMD_CENTER_RESERVED = 0
DUSS_MB_CMD_CENTER_REQ_BATT_INFO_CONFIRM = 1
DUSS_MB_CMD_CENTER_PUSH_BATT_DYNAMIC_INFO = 2
DUSS_MB_CMD_CENTER_CONTROL_UAV_STATUS_LED = 3
DUSS_MB_CMD_CENTER_TRANSFORM_CONTROL = 4
DUSS_MB_CMD_CENTER_REQ_PUSH_BAT_NORMAL_DATA = 5
DUSS_MB_CMD_CENTER_PUSH_BAT_NORMAL_DATA = 6
DUSS_MB_CMD_CENTER_QUERY_BAT_STATUS = 7
DUSS_MB_CMD_CENTER_QUERY_BAT_HISOTY_STATUS = 8
DUSS_MB_CMD_CENTER_BAT_SELFDISCHARGE_DAYS = 9
DUSS_MB_CMD_CENTER_BAT_STORAGE_INFO = 10
DUSS_MB_CMD_CENTER_REQ_BAT_STATIC_DATA = 33
DUSS_MB_CMD_CENTER_REQ_BAT_DYNAMIC_DATA = 34
DUSS_MB_CMD_CENTER_REQ_BAT_AUTH_DATA = 35
DUSS_MB_CMD_CENTER_REQ_BAT_AUTH_RESULT = 36
DUSS_MB_CMD_CENTER_REQ_BAT_SELFDISCHARGE_TIME = 49
DUSS_MB_CMD_CENTER_SET_BAT_SELFDISCHARGE_TIME = 50
DUSS_MB_CMD_CENTER_REQ_BAT_BARCODE = 51
DUSS_MB_CMD_RC_GET_LOGIC_CHANNEL_PARAMETER = 1
DUSS_MB_CMD_RC_SET_LOGIC_CHANNEL_MAPPING = 2
DUSS_MB_CMD_RC_SET_CALIBIRATION = 3
DUSS_MB_CMD_RC_GET_PHYSICAL_CHANNEL_PARAMETER = 4
DUSS_MB_CMD_RC_PUSH_RC_PARAMETER = 5
DUSS_MB_CMD_RC_SET_MASTER_SLAVE_MODE = 6
DUSS_MB_CMD_RC_GET_MASTER_SLAVE_MODE = 7
DUSS_MB_CMD_RC_SET_NAME = 8
DUSS_MB_CMD_RC_GET_NAME = 9
DUSS_MB_CMD_RC_SET_PASSWORD = 10
DUSS_MB_CMD_RC_GET_PASSWORD = 11
DUSS_MB_CMD_RC_SET_CONNECTED_MASTER_ID = 12
DUSS_MB_CMD_RC_GET_CONNECTED_MASTER_ID = 13
DUSS_MB_CMD_RC_GET_AVAILABLE_MASTER_ID = 14
DUSS_MB_CMD_RC_SET_SEARCH_MODE = 15
DUSS_MB_CMD_RC_GET_SEARCH_MODE = 16
DUSS_MB_CMD_RC_SET_MASTER_SLAVE_SWITCH = 17
DUSS_MB_CMD_RC_GET_MASTER_SLAVE_SWITCH_CONF = 18
DUSS_MB_CMD_RC_REQUEST_JOIN_BY_SLAVE = 19
DUSS_MB_CMD_RC_LIST_REQUEST_JOIN_SLAVE = 20
DUSS_MB_CMD_RC_DELETE_SLAVE = 21
DUSS_MB_CMD_RC_DELETE_MASTER = 22
DUSS_MB_CMD_RC_SET_SLAVE_CONTROL_RIGHT = 23
DUSS_MB_CMD_RC_GET_SLAVE_CONTROL_RIGHT = 24
DUSS_MB_CMD_RC_SET_CONTROL_MODE = 25
DUSS_MB_CMD_RC_GET_CONTROL_MODE = 26
DUSS_MB_CMD_RC_PUSH_GPS_INFO = 27
DUSS_MB_CMD_RC_PUSH_RTC_INFO = 28
DUSS_MB_CMD_RC_PUSH_TEMPERATURE_INFO = 29
DUSS_MB_CMD_RC_PUSH_BATTERY_INFO = 30
DUSS_MB_CMD_RC_PUSH_MASTER_SLAVE_CONN_INFO = 31
DUSS_MB_CMD_RC_SET_CE_FCC_MODE = 32
DUSS_MB_CMD_RC_GET_CE_FCC_MODE = 33
DUSS_MB_CMD_RC_GET_GIMBAL_CONTROL = 34
DUSS_MB_CMD_RC_REQUEST_GIMBAL_CONTROL = 35
DUSS_MB_CMD_RC_SET_SIMULATE_FLIGHT_MODE = 36
DUSS_MB_CMD_RC_GET_SIMULATE_FLIGHT_MODE = 37
DUSS_MB_CMD_RC_PUSH_AETR_VALUE = 38
DUSS_MB_CMD_RC_GET_DETECTION_INFO = 39
DUSS_MB_CMD_RC_GET_GIMBAL_CONTROL_ACCESS_RIGHT = 40
DUSS_MB_CMD_RC_SET_SLAVE_CONTROL_MODE = 41
DUSS_MB_CMD_RC_GET_SLAVE_CONTROL_MODE = 42
DUSS_MB_CMD_RC_SET_GIMBAL_CONTROL_SPEED = 43
DUSS_MB_CMD_RC_GET_GIMBAL_CONTROL_SPEED = 44
DUSS_MB_CMD_RC_SET_SELF_DEFINED_KEY_FUNC = 45
DUSS_MB_CMD_RC_GET_SELF_DEFINED_KEY_FUNC = 46
DUSS_MB_CMD_RC_PAIRING = 47
DUSS_MB_CMD_RC_TEST_GPS = 48
DUSS_MB_CMD_RC_SET_RTC_CLOCK = 49
DUSS_MB_CMD_RC_GET_RTC_CLOCK = 50
DUSS_MB_CMD_RC_SET_GIMBAL_CONTROL_SENSITIVITY = 51
DUSS_MB_CMD_RC_GET_GIMBAL_CONTROL_SENSITIVITY = 52
DUSS_MB_CMD_RC_SET_GIMBAL_CONTROL_MODE = 53
DUSS_MB_CMD_RC_GET_GIMBAL_CONTROL_MODE = 54
DUSS_MB_CMD_RC_REQUEST_ENTER_APP_MODE = 55
DUSS_MB_CMD_RC_GET_CALIBRATION_VALUE = 56
DUSS_MB_CMD_RC_PUSH_MASTER_SLAVE_CONNECT_STATUS = 57
DUSS_MB_CMD_RC_SET_2014_USB_MODE = 58
DUSS_MB_CMD_RC_SET_RC_ID = 59
DUSS_MB_CMD_RC_PUSH_RMC_KEY_INFO = 80
DUSS_MB_CMD_RC_PUSH_TO_GLASS = 81
DUSS_MB_CMD_RC_PUSH_LCD_TO_MCU = 82
DUSS_MB_CMD_RC_GET_UNIT_LANGUAGE = 83
DUSS_MB_CMD_RC_SET_UNIT_LANGUAGE = 84
DUSS_MB_CMD_RC_SET_TEST_MODE = 85
DUSS_MB_CMD_RC_QUIRY_ROLE = 86
DUSS_MB_CMD_RC_QUIRY_MS_LINK_STATUS = 87
DUSS_MB_CMD_RC_SET_WORK_FUNCTION = 88
DUSS_MB_CMD_RC_GET_WORK_FUNCTION = 89
DUSS_MB_CMD_RC_SET_RF_CERT_CONFIG = 240
DUSS_MB_CMD_RC_TEST_STICK_VALUE = 245
DUSS_MB_CMD_RC_FACTORY_GET_BOARD_ID = 246
DUSS_MB_CMD_RC_PUSH_BUZZER_TO_MCU = 247
DUSS_MB_CMD_RC_GET_STICK_VERIFICATION_DATA = 248
DUSS_MB_CMD_RC_SET_POST_CALIBIRATION = 249
DUSS_MB_CMD_RC_GET_STICK_MIDDLE_VALUE = 250
DUSS_MB_CMD_WIFI_RESERVED = 0
DUSS_MB_CMD_WIFI_AP_PUSH_SCAN_RESULTS = 1
DUSS_MB_CMD_WIFI_AP_GET_CHAN_SNR = 2
DUSS_MB_CMD_WIFI_AP_SET_CHAN = 3
DUSS_MB_CMD_WIFI_AP_GET_CHAN = 4
DUSS_MB_CMD_WIFI_AP_SET_TX_PWR = 5
DUSS_MB_CMD_WIFI_AP_GET_TX_PWR = 6
DUSS_MB_CMD_WIFI_AP_GET_SSID = 7
DUSS_MB_CMD_WIFI_AP_SET_SSID = 8
DUSS_MB_CMD_WIFI_AP_PUSH_RSSI = 9
DUSS_MB_CMD_WIFI_AP_GET_ANT_RSSI = 10
DUSS_MB_CMD_WIFI_AP_SET_MAC_ADDR = 11
DUSS_MB_CMD_WIFI_AP_GET_MAC_ADDR = 12
DUSS_MB_CMD_WIFI_AP_SET_PASSPHRASE = 13
DUSS_MB_CMD_WIFI_AP_GET_PASSPHRASE = 14
DUSS_MB_CMD_WIFI_AP_FACTORY_RESET = 15
DUSS_MB_CMD_WIFI_AP_SET_BAND = 16
DUSS_MB_CMD_WIFI_AP_PUSH_STA_MAC = 17
DUSS_MB_CMD_WIFI_AP_GET_PHY_PARAM = 18
DUSS_MB_CMD_WIFI_AP_SET_PWR_MODE = 19
DUSS_MB_CMD_WIFI_AP_CALIBRATE = 20
DUSS_MB_CMD_WIFI_AP_RESTART = 21
DUSS_MB_CMD_WIFI_AP_UNDEFINED1 = 22
DUSS_MB_CMD_WIFI_AP_UNDEFINED2 = 23
DUSS_MB_CMD_WIFI_AP_UNDEFINED3 = 24
DUSS_MB_CMD_WIFI_AP_UNDEFINED4 = 25
DUSS_MB_CMD_WIFI_AP_UNDEFINED5 = 26
DUSS_MB_CMD_WIFI_AP_UNDEFINED6 = 27
DUSS_MB_CMD_WIFI_AP_UNDEFINED7 = 28
DUSS_MB_CMD_WIFI_AP_UNDEFINED8 = 29
DUSS_MB_CMD_WIFI_AP_UNDEFINED9 = 30
DUSS_MB_CMD_WIFI_AP_UNDEFINEDA = 31
DUSS_MB_CMD_WIFI_AP_GET_FREQ = 32
DUSS_MB_CMD_WIFI_AP_SET_BW = 33
DUSS_MB_CMD_WIFI_AP_UNDEFINEDC = 34
DUSS_MB_CMD_WIFI_AP_UNDEFINEDD = 35
DUSS_MB_CMD_WIFI_AP_UNDEFINEDE = 36
DUSS_MB_CMD_WIFI_AP_UNDEFINEDF = 37
DUSS_MB_CMD_WIFI_AP_REALTIME_ACS = 38
DUSS_MB_CMD_WIFI_AP_MANUAL_SWITCH_SDR = 39
DUSS_MB_CMD_WIFI_AP_PUSH_CHAN_LIST = 40
DUSS_MB_CMD_WIFI_AP_REQ_CHAN_NOISE = 41
DUSS_MB_CMD_WIFI_AP_PUSH_CHAN_NOISE = 42
DUSS_MB_CMD_WIFI_AP_SET_HW_MODE = 43
DUSS_MB_CMD_WIFI_AP_SET_USR_PREF = 46
DUSS_MB_CMD_WIFI_AP_GET_USR_PREF = 47
DUSS_MB_CMD_WIFI_AP_SET_COUNTRY_CODE = 48
DUSS_MB_CMD_WIFI_AP_RESET_FREQ = 49
DUSS_MB_CMD_WIFI_AP_DEL_COUNTRY_CODE = 50
DUSS_MB_CMD_WIFI_AP_VERIFY_CC = 51
DUSS_MB_CMD_WIFI_GET_WORK_MODE = 57
DUSS_MB_CMD_WIFI_SET_WORK_MODE = 58
DUSS_MB_CMD_WIFI_CONFIG_BY_QRCODE = 59
DUSS_MB_CMD_WIFI_PUSH_MAC_STAT = 128
DUSS_MB_CMD_WIFI_SET_RC_INFO = 145
DUSS_MB_CMD_WIFI_UPDATE_SW_STATE = 146
DUSS_MB_CMD_DM368_RESERVED = 0
DUSS_MB_CMD_DM368_SEND_GND_CTRL_INFO = 1
DUSS_MB_CMD_DM368_RECV_GND_CTRL_INFO = 2
DUSS_MB_CMD_DM368_SEND_UAV_CTRL_INFO = 3
DUSS_MB_CMD_DM368_RECV_UAV_CTRL_INFO = 4
DUSS_MB_CMD_DM368_SEND_GND_STAT_INFO = 5
DUSS_MB_CMD_DM368_SEND_UAV_STAT_INFO = 6
DUSS_MB_CMD_DM368_GET_APP_CONNECT_STAT = 14
DUSS_MB_CMD_DM368_RECYCLE_VISION_FRAME_INFO = 15
DUSS_MB_CMD_DM368_SET_BITRATE = 32
DUSS_MB_CMD_DM368_GET_BITRATE = 33
DUSS_MB_CMD_DM368_PUSH_STATUS = 48
DUSS_MB_CMD_DM368_SEND_VMEM_FD_TO_VISION = 49
DUSS_MB_CMD_SET_CAM_FORMAT_MODE = 64
DUSS_MB_CMD_HDVT_RESERVED = 0
DUSS_MB_CMD_HDVT_PUSH_OSD_DATA = 1
DUSS_MB_CMD_HDVT_PUSH_HOME_POINT = 2
DUSS_MB_CMD_HDVT_PUSH_BB_STATUS = 3
DUSS_MB_CMD_HDVT_WRITE_FPGA = 4
DUSS_MB_CMD_HDVT_READ_FPGA = 5
DUSS_MB_CMD_HDVT_WRITE_9363 = 6
DUSS_MB_CMD_HDVT_READ_9363 = 7
DUSS_MB_CMD_HDVT_PUSH_VT_SIGNAL_QUALITY = 8
DUSS_MB_CMD_HDVT_REQ_FREQ_ENERGY = 9
DUSS_MB_CMD_HDVT_PUSH_FREQ_ENERGY = 10
DUSS_MB_CMD_HDVT_PUSH_DEVICE_STATUS = 11
DUSS_MB_CMD_HDVT_GET_VT_CONFIG_INFO = 12
DUSS_MB_CMD_HDVT_SET_VT_CONFIG_INFO = 13
DUSS_MB_CMD_HDVT_CHANGE_USB_IF = 14
DUSS_MB_CMD_HDVT_RESET_68013 = 15
DUSS_MB_CMD_HDVT_UPGRADE = 16
DUSS_MB_CMD_HDVT_PUSH_WL_ENV_QUALITY = 17
DUSS_MB_CMD_HDVT_SET_FACTORY_TEST = 18
DUSS_MB_CMD_HDVT_GET_FACTORY_TEST = 19
DUSS_MB_CMD_HDVT_SET_MAX_VIDEO_BANDWIDTH = 20
DUSS_MB_CMD_HDVT_PUSH_MAX_VIDEO_BANDWIDTH = 21
DUSS_MB_CMD_HDVT_PUSH_DEBUG_INFO = 22
DUSS_MB_CMD_HDVT_PUSH_SDR_DL_FREQ_ENERGY = 32
DUSS_MB_CMD_HDVT_GET_SDR_VT_CONFIG_INFO = 33
DUSS_MB_CMD_HDVT_PUSH_SDR_DL_AUTO_VT_INFO = 34
DUSS_MB_CMD_HDVT_REQ_SDR_RT_STATUS = 35
DUSS_MB_CMD_HDVT_PUSH_SDR_UAV_RT_STATUS = 36
DUSS_MB_CMD_HDVT_PUSH_SDR_GND_RT_STATUS = 37
DUSS_MB_CMD_HDVT_SDR_DEBUG_READ = 38
DUSS_MB_CMD_HDVT_SDR_DEBUG_WRITE = 39
DUSS_MB_CMD_HDVT_REQ_SDR_LOG = 40
DUSS_MB_CMD_HDVT_PUSH_SDR_UL_FREQ_ENERGY = 41
DUSS_MB_CMD_HDVT_PUSH_SDR_UL_AUTO_VT_INFO = 42
DUSS_MB_CMD_HDVT_SDR_REVERT_ROLE = 43
DUSS_MB_CMD_HDVT_SDR_AMT_PROCESS = 44
DUSS_MB_CMD_HDVT_SDR_GET_LBT_STATUS = 45
DUSS_MB_CMD_HDVT_SDR_SET_LBT_STATUS = 46
DUSS_MB_CMD_HDVT_SDR_LINK_TEST = 47
DUSS_MB_CMD_HDVT_SDR_WIRELESS_ENV = 48
DUSS_MB_CMD_HDVT_SDR_SCAN_FREQ_CFG = 49
DUSS_MB_CMD_HDVT_SDR_FACTORY_MODE_SET = 50
DUSS_MB_CMD_HDVT_TRACKING_STATE_IND = 51
DUSS_MB_CMD_HDVT_SDR_LIVEVIEW_MODE_SET = 52
DUSS_MB_CMD_HDVT_SDR_LIVEVIEW_MODE_GET = 53
DUSS_MB_CMD_HDVT_SDR_LIVEVIEW_RATE_IND = 54
DUSS_MB_CMD_HDVT_ABNORMAL_EVENT_IND = 55
DUSS_MB_CMD_HDVT_SDR_SET_RATE = 56
DUSS_MB_CMD_HDVT_SET_LIVEVIEW_CONFIG = 57
DUSS_MB_CMD_HDVT_PUSH_DL_FREQ_ENERGY = 58
DUSS_MB_CMD_HDVT_TIP_INTERFERENCE = 59
DUSS_MB_CMD_HDVT_SDR_UPGRADE_RF_POWER = 60
DUSS_MB_CMD_HDVT_PUSH_SLAVE_RT_STATUS = 62
DUSS_MB_CMD_HDVT_PUSH_RC_CONN_STATUS = 63
DUSS_MB_CMD_HDVT_SET_ROBOMASTER_CNFG = 81
DUSS_MB_CMD_HDVT_GET_ROBOMASTER_INFO = 82
DUSS_MB_CMD_HDVT_GET_SDR_CP_STATUS = 83
DUSS_MB_CMD_HDVT_RACING_SET_MODEM_INFO = 65
DUSS_MB_CMD_HDVT_RACING_GET_MODEM_INFO = 66
DUSS_MB_CMD_VISION_RESERVED = 0
DUSS_MB_CMD_VISION_BINO_INFO = 1
DUSS_MB_CMD_VISION_MONO_INFO = 2
DUSS_MB_CMD_VISION_ULTRASONIC_INFO = 3
DUSS_MB_CMD_VISION_OA_INFO = 4
DUSS_MB_CMD_VISION_RELITIVE_POS = 5
DUSS_MB_CMD_VISION_AVOIDANCE_WARN = 6
DUSS_MB_CMD_VISION_OBSTACLE_INFO = 7
DUSS_MB_CMD_VISION_TAPGO_OA_INFO = 8
DUSS_MB_CMD_VISION_PUSH_VISION_DEBUG_INFO = 10
DUSS_MB_CMD_VISION_PUSH_CONTROL_DEBUG_INFO = 11
DUSS_MB_CMD_VISION_PUSH_SDK_CONTROL_CMD = 15
DUSS_MB_CMD_VISION_ENABLE_TRACKING_TAPTOGO = 16
DUSS_MB_CMD_VISION_PUSH_TARGET_SPEED_POS_INFO = 17
DUSS_MB_CMD_VISION_PUSH_TARGET_POS_INFO = 18
DUSS_MB_CMD_VISION_PUSH_TRAJECTORY = 19
DUSS_MB_CMD_VISION_PUSH_EXPECTED_SPEED_ANGLE = 20
DUSS_MB_CMD_VISION_RECEIVE_FRAME_INFO = 21
DUSS_MB_CMD_VISION_FIXED_WING_CTRL = 29
DUSS_MB_CMD_VISION_FIXED_WING_STATUS_PUSH = 30
DUSS_MB_CMD_VISION_FLAT_CHECK = 25
DUSS_MB_CMD_VISION_MARQUEE_PUSH = 32
DUSS_MB_CMD_VISION_TRACKING_CNF_CANCEL = 33
DUSS_MB_CMD_VISION_MOVE_MARQUEE_PUSH = 34
DUSS_MB_CMD_VISION_TRACKING_STATUS_PUSH = 35
DUSS_MB_CMD_VISION_POSITION_PUSH = 36
DUSS_MB_CMD_VISION_FLY_CTL_PUSH = 37
DUSS_MB_CMD_VISION_TAPGO_STATUS_PUSH = 38
DUSS_MB_CMD_VISION_COMMON_CTL_CMD = 39
DUSS_MB_CMD_VISION_GET_PARA_CMD = 40
DUSS_MB_CMD_VISION_SET_PARA_CMD = 41
DUSS_MB_CMD_VISION_COM_STATUS_UPDATE = 42
DUSS_MB_CMD_VISION_TA_LOCK_UPDATE = 44
DUSS_MB_CMD_VISION_SMART_LANDING = 45
DUSS_MB_CMD_VISION_FUNC_LIST_PUSH = 46
DUSS_MB_CMD_VISION_SENSOR_STATUS_PUSH = 47
DUSS_MB_CMD_VISION_SELF_CALI = 48
DUSS_MB_CMD_VISION_SELF_CALI_STATE = 50
DUSS_MB_CMD_VISION_QRCODE_MODE = 55
DUSS_MB_CMD_VISION_RC_PACKET = 70
DUSS_MB_CMD_VISION_SET_BUFFER_CONFIG = 71
DUSS_MB_CMD_VISION_GET_BUFFER_CONFIG = 72
DUSS_MB_CMD_VISION_ENABLE_SDK_FUNC = 163
DUSS_MB_CMD_VISION_DETECTION_MSG_PUSH = 164
DUSS_MB_CMD_VISION_GET_SDK_FUNC = 165
DUSS_MB_CMD_VISION_CTRL_PARAM_SET = 168
DUSS_MB_CMD_VISION_CHASSIS_CTRL_PARAM_SET = 169
DUSS_MB_CMD_VISION_GIMBAL_CTRL_PARAM_SET = 170
DUSS_MB_CMD_VISION_LINE_DETECTION_ATTR_SET = 171
DUSS_MB_CMD_BATTERY_GET_DYNAMIC_INFO = 2
DUSS_MB_CMD_BATTERY_GET_SINGLE_CORE_VOLT = 3
DUSS_MB_CMD_BATTERY_PUSH_COMMON_INFO = 6
DUSS_MB_CMD_SIM_RESERVED = 0
DUSS_MB_CMD_SIM_SET_SIM_VISION_MODE = 26
DUSS_MB_CMD_SIM_GET_SIM_VISION_MODE = 27
DUSS_MB_CMD_GLASS_LINK_STATE_IND = 1
DUSS_MB_CMD_GLASS_IMU_STATUS_PUSH = 2
DUSS_MB_CMD_GLASS_SDR_STATUS_PUSH = 3
DUSS_MB_CMD_GLASS_GET_HEADBELT_SN = 4
DUSS_MB_CMD_RM_HIT_EVENT = 2
DUSS_MB_CMD_RM_WATER_GUN_PARM_SET = 5
DUSS_MB_CMD_RM_GAME_STATE_SYNC = 9
DUSS_MB_CMD_RM_GAMECTRL_CMD = 10
DUSS_MB_CMD_RM_GAME_GROUP_CONFIG = 11
DUSS_MB_CMD_RM_GAME_START_END_CONFIG = 12
DUSS_MB_CMD_RM_SKILL_SEND = 15
DUSS_MB_CMD_RM_IR_EVENT = 16
DUSS_MB_CMD_RM_BLOOD_LED_SET = 17
DUSS_MB_CMD_RM_PLAY_SOUND = 26
DUSS_MB_CMD_RM_SET_SPEAKER_VOLUME = 27
DUSS_MB_CMD_RM_GET_SPEAKER_VOLUME = 28
DUSS_MB_CMD_RM_AUDIO_TO_APP = 29
DUSS_MB_CMD_RM_SET_AUDIO_STATUS = 30
DUSS_MB_CMD_RM_CONFIG_STATE = 34
DUSS_MB_CMD_RM_ATTITUDE_EVENT = 41
DUSS_MB_CMD_RM_ARMOR_GET_STATE = 49
DUSS_MB_CMD_RM_ARMOR_LED_SET = 50
DUSS_MB_CMD_RM_SYSTEM_LED_SET = 51
DUSS_MB_CMD_RM_SHOOT_EVENT = 80
DUSS_MB_CMD_RM_SHOOT_CMD = 81
DUSS_MB_CMD_RM_SHOOT_GET_STATE = 82
DUSS_MB_CMD_RM_SHOOT_MODE_SET = 83
DUSS_MB_CMD_RM_SHOOT_MODE_GET = 84
DUSS_MB_CMD_RM_GUN_LED_SET = 85
DUSS_MB_CMD_RM_SET_SIGHT_BEAD_POSITION = 86
DUSS_MB_CMD_RM_GET_SIGHT_BEAD_POSITION = 87
DUSS_MB_CMD_RM_FC_RMC = 96
DUSS_MB_CMD_RM_FC_GET_STATE = 97
DUSS_MB_CMD_RM_1860_ACTIVE_STATE_GET = 117
DUSS_MB_CMD_VBUS_ADD_NODE = 1
DUSS_MB_CMD_VBUS_NODE_RESET = 2
DUSS_MB_CMD_VBUS_ADD_MSG = 3
DUSS_MB_CMD_VBUS_DEL_MSG = 4
DUSS_MB_CMD_VBUS_QUERY_CONF = 5
DUSS_MB_CMD_VBUS_SET_PUSH_FREQ = 6
DUSS_MB_CMD_VBUS_PUSH_CTRL = 7
DUSS_MB_CMD_VBUS_DATA_ANALYSIS = 8
DUSS_MB_CMD_PER_TOF_DATA_SET = 32
DUSS_MB_CMD_PER_TOF_DATA_PUSH = 33
DUSS_MB_CMD_ROBOTIC_GRIPPER_CTRL_SET = 17
DUSS_MB_CMD_ROBOTIC_GRIPPER_STATUS_GET = 18
DUSS_MB_CMD_ROBOTIC_ARM_MOVE_CTRL = 19
DUSS_MB_CMD_ROBOTIC_ARM_POSITION_GET = 20
DUSS_MB_CMD_ROBOTIC_SERVO_ANGLE_GET = 21
DUSS_MB_CMD_ROBOTIC_SERVO_MODE_SET = 22
DUSS_MB_CMD_ROBOTIC_SERVO_DATA_SET = 23
DUSS_MB_CMD_ROBOTIC_ARM_MOVE_STOP = 24
DUSS_MB_CMD_EDUPLATFORM_SPEECH_DATA_SET = 16
DUSS_MB_CMD_EDUPLATFORM_SPEECH_DATA_PUSH = 17
DUSS_MB_CMD_EDUPLATFORM_TEXT_TO_SPEECH_TASK = 18
DUSS_MB_CMD_EDUPLATFORM_TEXT_TO_SPEECH_TASK_PUSH = 19
DUSS_MB_CMD_EDUPLATFORM_TRACKLINE_SET_ENABLE = 32