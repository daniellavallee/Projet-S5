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

def control_back_wheels(speed:int, angle:int):
    bw.speed = abs(speed)
    ratio = abs((angle - 90) / 45)
    speed_of_bracked_wheel = speed * ratio
    if (angle<=90): # Gauche
        left_speed = speed_of_bracked_wheel
        right_speed = speed
    else:
        left_speed = speed
        right_speed = speed_of_bracked_wheel
        
    if (speed>0):
        bw.left_wheel.backward(left_speed)
        bw.right_wheel.backward(right_speed)
    elif (speed<0):
        bw.left_wheel.forward(left_speed)
        bw.right_wheel.forward(right_speed)
    else:
        bw.stop()
    
def control(controls:ControllerResponse):
    wheel_angle = controls.wheel_angle
    bw_speed = controls.bw_speed
    control_front_wheels(wheel_angle)
    control_back_wheels(bw_speed, wheel_angle)