from .models import ControllerResponse
from .picar import front_wheels, back_wheels, setup

setup()

fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')

def control_front_wheels(angle:int):
    if angle == 90:
        fw.turn_straight()
    else:
        fw.turn(angle)

def control_back_wheels(speed:int):
    bw.speed = speed
    if (speed>0):
        bw.forward()
    elif (speed<0):
        bw.backward()
    else:
        bw.stop()
    
def control(controls:ControllerResponse):
    wheel_angle = controls.wheel_angle
    bw_speed = controls.bw_speed
    control_front_wheels(wheel_angle)
    control_back_wheels(bw_speed)