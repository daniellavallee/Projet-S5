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
    ratio = 1 - abs((angle - 90) / 45)
    speed_of_bracked_wheel = int(speed * ratio)
    if (angle==90 or speed < 0): # Reculer ou droit
        left_speed = speed
        right_speed = speed
    elif (angle<90): # Gauche
        left_speed = speed
        right_speed = speed_of_bracked_wheel
    else:
        left_speed = speed_of_bracked_wheel
        right_speed = speed
        
    if (left_speed>0):
        bw.left_wheel.backward(abs(left_speed))
    elif (left_speed<0):
        bw.left_wheel.forward(abs(left_speed))
    else:
        bw.left_wheel.stop()
    
    if (right_speed>0):
        bw.right_wheel.backward(abs(right_speed))
    elif (right_speed<0):
        bw.right_wheel.forward(abs(right_speed))
    else:
        bw.right_wheel.stop()
    
def control(controls:ControllerResponse):
    wheel_angle = controls.wheel_angle
    bw_speed = controls.bw_speed
    control_front_wheels(wheel_angle)
    control_back_wheels(bw_speed, wheel_angle)