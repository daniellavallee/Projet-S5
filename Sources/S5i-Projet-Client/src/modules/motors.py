from src.models import MotorsConfig
from .time import Time
from src.enums import MoveForwardState

class Motors():
    """
    This class is responsible for handling the motors of the car
    """
    def __init__(self, config:MotorsConfig,time_module:Time, verbose:bool=False):
        self.config = config
        self.verbose = verbose
        self.speed : float  = 0.0
        self.angle : float = 90.0
        self.time_module = time_module
        self.distance_parcourue = 0.0
        self.distance_acceleration = 0.0
        self.move_forward_state: MoveForwardState = MoveForwardState.STOP
    def add_to_current_value(self, current_value:float, wanted_value:int, offset:float) -> float:
        new_value = current_value + offset
        if current_value > wanted_value:
            if new_value < wanted_value:
                new_value = wanted_value
        elif current_value < wanted_value:
            if new_value > wanted_value:
                new_value = wanted_value
        return new_value
    def get_speed(self) -> int:
        return int(self.speed)
    def get_angle(self) -> int:
        return int(self.angle)
    def get_offset(self, per_seconds_value:int) -> float:
        return per_seconds_value * self.time_module.get_dt_in_seconds()
    def set_angle(self, wanted_angle:int):
        """
        Set the angle of the wheels (handling angular acceleration/deceleration)
        """
        if self.angle == wanted_angle:
            return
        # Clip the angle to the maximum left and right angles
        if wanted_angle < self.config.maxLeftAngle:
            wanted_angle = self.config.maxLeftAngle
        if wanted_angle > self.config.maxRightAngle:
            wanted_angle = self.config.maxRightAngle
            
        # if the wanted angle is greater than the current angle
        if wanted_angle > self.angle:
            self.angle = self.add_to_current_value(self.angle,wanted_angle,self.get_offset(self.config.maxAngularAcc))
        else:
            self.angle = self.add_to_current_value(self.angle,wanted_angle,self.get_offset(-self.config.maxAngularAcc))
    def set_speed(self, wanted_speed:int):
        """
        Set the speed of the motors (handling acceleration/deceleration)
        """
        if self.speed == wanted_speed:
            return
        
        #Clip the speed to the borders speed
        if wanted_speed < self.config.minSpeed:
            wanted_speed = self.config.minSpeed
        if wanted_speed > self.config.maxSpeed:
            wanted_speed = self.config.maxSpeed
        
        # if the new speed is greater than the current speed
        if wanted_speed > self.speed :
            self.speed = self.add_to_current_value(self.speed,wanted_speed,self.get_offset(self.config.maxAcceleration))
        else:
            self.speed = self.add_to_current_value(self.speed,wanted_speed,self.get_offset(-self.config.maxAcceleration))
        
    
    def move_forward(self, distance:float) -> bool:
        """
        Description:      Move the car forward of x meters.
        Parameters:
            distance:     distance in meters to move forward to.
        Return:           void.
        """

        # État initiale
        if self.move_forward_state == MoveForwardState.STARTING:
            self.move_forward_state = MoveForwardState.MOVING_ACC
            self.distance_parcourue = 0.0
            self.distance_acceleration = 0.0
            self.set_speed(self.config.maxSpeed)

            print("État initial")

        # État d'accélération
        elif self.move_forward_state == MoveForwardState.MOVING_ACC:
            if self.get_speed() == self.config.maxSpeed:
                self.distance_acceleration += self.get_speed() * self.time_module.get_dt_in_seconds()
                self.set_speed(self.config.maxSpeed)
                self.move_forward_state = MoveForwardState.MOVING_FORWARD
            elif self.distance_acceleration * 2 >= distance:
                self.move_forward_state = MoveForwardState.MOVING_DECC
            
            print("État d'accélération")

        # État de mouvement
        elif self.move_forward_state == MoveForwardState.MOVING_FORWARD:
            if self.distance_parcourue + self.distance_acceleration < distance:
                self.distance_parcourue += self.get_speed() * self.time_module.get_dt_in_seconds()
                self.set_speed(self.config.maxSpeed)
            else:
                Motors.set_speed(0)
                self.move_forward_state = MoveForwardState.MOVING_DECC
        
            print("État de mouvement")

        # État de décélération
        elif self.move_forward_state == MoveForwardState.MOVING_DECC:
            if self.get_speed() == 0:
                self.move_forward_state = MoveForwardState.STOP
            else:
                self.set_speed(0)
                self.move_forward_state = MoveForwardState.MOVING_DECC
            self.move_forward_state = MoveForwardState.STOP
            
            print("État de décélération")

        # État d'arrêt
        elif self.move_forward_state == MoveForwardState.STOP:
            self.distance_parcourue = 0.0
            self.distance_accelerationo = 0.0
            return True

        return False

    def turn_to_angle(self, direction:int, angle:int=0):
        """
        Description:
         Parameters:
            direction:    (int) 0 for left, 1 for right.
            angle:        (int)
        Return: void.
        """


         
        
        

        