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
    def is_in_zero_range(self, speed:float) -> bool:
        return speed < self.config.maxZeroZone and speed > self.config.minZeroZone
    def add_to_current_value(self, current_value:float, wanted_value:int, offset:float) -> float:
        new_value = current_value + offset
        if current_value > wanted_value:
            if new_value < wanted_value:
                new_value = wanted_value
        elif current_value < wanted_value:
            if new_value > wanted_value:
                new_value = wanted_value
        return new_value
    def get_speed(self, *, in_meters_per_second : bool = False) -> int | float:
        if in_meters_per_second:
            get_speed_ratio = 0
            if self.speed > 0:
                get_speed_ratio = (self.speed - self.config.maxZeroZone) / (self.config.maxSpeed - self.config.maxZeroZone)
            return get_speed_ratio * self.config.speedInMeterPerSecondPerUnit
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
        
        # if the speed is in the zero zone, we need to set it to the limits of the zero zone
        if self.is_in_zero_range(self.speed):
            if wanted_speed > 0:
                self.speed = self.config.maxZeroZone + 0.01
            else:
                self.speed = self.config.minZeroZone - 0.01
        
        # if the new speed is greater than the current speed
        if wanted_speed > self.speed :
            self.speed = self.add_to_current_value(self.speed,wanted_speed,self.get_offset(self.config.maxAcceleration))
        else:
            self.speed = self.add_to_current_value(self.speed,wanted_speed,self.get_offset(-self.config.maxAcceleration))

        if (self.is_in_zero_range(self.speed)):
            self.speed = 0
        
        
            