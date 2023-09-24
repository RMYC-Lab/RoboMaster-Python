import event_client
import rm_ctrl
import rm_define
import math
import traceback
import rm_log
import multi_communication
import rm_socket
import math
import random

from widget import *

logger = rm_log.dji_scratch_logger_get()
event = event_client.EventClient()
# modulesStatus_ctrl = rm_ctrl.ModulesStatusCtrl(event)
gun_ctrl = rm_ctrl.GunCtrl(event)
armor_ctrl = rm_ctrl.ArmorCtrl(event)
vision_ctrl = rm_ctrl.VisionCtrl(event)
chassis_ctrl = rm_ctrl.ChassisCtrl(event)
gimbal_ctrl = rm_ctrl.GimbalCtrl(event)
robot_ctrl = rm_ctrl.RobotCtrl(event, chassis_ctrl, gimbal_ctrl)
log_ctrl = rm_ctrl.LogCtrl(event)
# scratch mode only
led_ctrl = rm_ctrl.LedCtrl(event)
media_ctrl = rm_ctrl.MediaCtrl(event)
# need replaced when app changed the method name
time = rm_ctrl.RobotTools(event)
tools = rm_ctrl.RobotTools(event)
debug_ctrl = rm_ctrl.DebugCtrl(event)
mobile_ctrl = rm_ctrl.MobileCtrl(event)
# multi_comm_ctrl = multi_communication.MultiCommunication(event, socket_ctrl)
ir_blaster_ctrl = rm_ctrl.GunCtrl(event, type='ir')

speech_recognizer_ctrl = rm_ctrl.SpeechRecognizerCtrl(event)
trackline_ctrl = rm_ctrl.TackLineCtrl(event)

if edu_enable:
    ir_distance_sensor_ctrl = rm_ctrl.IrDistanceSensorCtrl(event)
    sensor_adapter_ctrl = rm_ctrl.SensorAdapterCtrl(event)
    servo_ctrl = rm_ctrl.ServoCtrl(event)
    gripper_ctrl = rm_ctrl.RoboticGripperCtrl(event)
    robotic_arm_ctrl = rm_ctrl.RoboticArmCtrl(event)

    # reinit event_client to cur event, to recv cmd to control the current thread
    serial_ctrl.reinit_event_client(event)
    robot_ctrl = rm_ctrl.RobotCtrl(event, chassis_ctrl, gimbal_ctrl, servo_ctrl)

blaster_ctrl = gun_ctrl
AI_ctrl = vision_ctrl

show_msg = log_ctrl.show_msg
print_msg = log_ctrl.print_msg
info_msg = log_ctrl.info_msg
debug_msg = log_ctrl.debug_msg
error_msg = log_ctrl.error_msg
fatal_msg = log_ctrl.fatal_msg
print=print_msg

robot_mode = rm_define.robot_mode
chassis_status = rm_define.chassis_status
gimbal_status = rm_define.gimbal_status
detection_type = rm_define.detection_type
detection_func = rm_define.detection_func
led_effect = rm_define.led_effect
led_position = rm_define.led_position
pwm_port = rm_define.pwm_port
line_color = rm_define.line_color

update_widget_global_event_client(event)
update_widget_global_index(0)

stage = Stage()

PIDCtrl = rm_ctrl.PIDCtrl

del event_client
del rm_ctrl
del rm_log
del multi_communication
del rm_socket
del edu_enable

# to compatible old code ->rm_ctrl.PIDCtrl
class rm_ctrl(object):
    PIDCtrl = PIDCtrl

def robot_reset():
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    gimbal_ctrl.resume()
    gimbal_ctrl.recenter(90)

def robot_init():
    if 'speed_limit_mode' in globals():
        chassis_ctrl.enable_speed_limit_mode()

    robot_ctrl.init()
    #modulesStatus_ctrl.init()
    armor_ctrl.init()
    gimbal_ctrl.init()
    chassis_ctrl.init()
    led_ctrl.init()
    gun_ctrl.init()
    chassis_ctrl.init()
    mobile_ctrl.init()
    tools.init()
    socket_ctrl.init()
    # multi_comm_ctrl.init()
    vision_ctrl.init()

    speech_recognizer_ctrl.init()
    trackline_ctrl.init()
    try:
        ir_distance_sensor_ctrl.init()
        servo_ctrl.init()
    except:
        pass
    robot_reset()

def ready():
    robot_init()
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    chassis_ctrl.stop()
    gimbal_ctrl.stop()

    # enable check-module
    modules_status_ctrl.check_module_enable(event)

    tools.program_timer_start()

def register_event():
    armor_ctrl.register_event(globals())
    vision_ctrl.register_event(globals())
    media_ctrl.register_event(globals())
    chassis_ctrl.register_event(globals())
    try:
        sensor_adapter_ctrl.register_event(globals())
        ir_distance_sensor_ctrl.register_event(globals())
    except:
        pass

def start():
    pass

def stop():
    event.script_state.set_script_has_stopped()
    block_description_push(id="ABCDEFGHIJ4567890123", name="STOP", type="INFO_PUSH", curvar="")

def robot_exit():
    robot_reset()
    robot_ctrl.exit()
    gimbal_ctrl.exit()
    chassis_ctrl.exit()
    gun_ctrl.exit()
    mobile_ctrl.exit()
    armor_ctrl.exit()
    media_ctrl.exit()
    # multi_comm_ctrl.exit()
    speech_recognizer_ctrl.exit()
    trackline_ctrl.exit()
    try:
        sensor_adapter_ctrl.exit()
        ir_distance_sensor_ctrl.exit()
        servo_ctrl.exit()
        serial_ctrl.reset()
    except:
        pass

try:
    ready()

# replace your python code here
SCRATCH_PYTHON_CODE

    register_event()
    start()
    stop()
except:
    _error_msg = traceback.format_exc()
    logger.error('MAIN: script exit, message: ')
    logger.error('TRACEBACK:\n' + _error_msg)
finally:
    event.script_state.reset_stop_flag()
    stage.destory()
    gun_ctrl.stop()
    chassis_ctrl.stop()
    gimbal_ctrl.stop()
    media_ctrl.stop()
    vision_ctrl.stop()
    armor_ctrl.stop()
    led_ctrl.stop()
    try:
        sensor_adapter_ctrl.stop()
    except:
        pass
    robot_exit()
    event.stop()
    del event
