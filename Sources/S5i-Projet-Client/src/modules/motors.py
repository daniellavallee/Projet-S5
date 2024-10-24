from src.models import MotorsConfig
from .time import Time

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
        
        
            