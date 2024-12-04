from src.models import MotorsConfig
import numpy as np
from .time import Time
from src.enums import MoveForwardState, TurnState, Direction

class Motors():
    """
    This class is responsible for handling the motors of the car
    """
    def __init__(self, config:MotorsConfig,time_module:Time, verbose:bool=False):
        self.config = config
        self.verbose = verbose
        self.speed : float  = 0.0
        self.angle : float = self.config.centerAngle
        self.time_module = time_module
        self.distance_parcourue = 0.0
        self.distance_acceleration = 0.0
        self.move_forward_state: MoveForwardState = MoveForwardState.STARTING
        self.turn_to_angle_state: TurnState = TurnState.STARTING
        self.longueur_arc = 0.0
        self.rayon_courbure = self.config.rayon_courbure
        self.block_wheel = False
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
    def get_speed(self, *, in_meters_per_second : bool = False) -> float:
        if in_meters_per_second:
            get_speed_ratio = 0
            speed = np.abs(self.speed)
            if speed >= self.config.maxZeroZone:
                get_speed_ratio = (speed - self.config.maxZeroZone) / (100 - self.config.maxZeroZone)
            return get_speed_ratio * self.config.maxSpeedInMeterPerSecond
        return int(self.speed)
    def get_decc_distance(self) -> float:
        acc_in_meters_per_second = self.config.maxAcceleration / 100 * self.config.maxSpeedInMeterPerSecond / 2.2
        return self.get_speed(in_meters_per_second=True) ** 2 / (2 * acc_in_meters_per_second)
    def get_curvature(self, angle_in_degrees:float) -> float:
        angle = angle_in_degrees - self.config.centerAngle
        angle_rad : float = np.deg2rad(np.abs(angle))
        if (angle_rad == 0):
            return 0
        rayon_roue_exterieur = self.config.wheelDistance / np.tan(angle_rad)
        rayon_roue_interieur = self.config.wheelDistance / np.tan(angle_rad)
        rayon_centre = (rayon_roue_exterieur + rayon_roue_interieur) / 2
        
        return rayon_centre
    
    
    def get_centrifugal_acceleration(self) -> float:
        speed = self.get_speed(in_meters_per_second=True) / self.config.maxSpeedInMeterPerSecond
        acc = speed ** 2 * self.get_curvature(self.get_angle())
        return acc
    def get_angle(self) -> int:
        return int(self.angle)
    def get_offset(self, per_seconds_value:int) -> float:
        return per_seconds_value * self.time_module.get_dt_in_seconds()
    def get_available_acceleration(self) -> float:
        value = self.config.maxAcceleration**2 - self.get_centrifugal_acceleration()**2
        # if the value is negative, it means that the car is in a curve and the acceleration is limited by the centrifugal acceleration
        # so we return -1 to indicate that the acceleration is limited
        if value < 0:
            return 0
        available_acceleration = np.sqrt(value)
        return available_acceleration
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
        current_max_acceleration = self.get_available_acceleration()
        
        if self.speed == wanted_speed:
            return
        
        #Clip the speed to the borders speed
        if wanted_speed < -self.config.maxSpeed:
            wanted_speed = -self.config.maxSpeed
        if wanted_speed > self.config.maxSpeed:
            wanted_speed = self.config.maxSpeed
        
        # if the speed is in the zero zone, we need to set it to the limits of the zero zone
        if self.is_in_zero_range(self.speed):
            if wanted_speed > 0:
                self.speed = self.config.maxZeroZone + 0.01
            else:
                self.speed = self.config.minZeroZone - 0.01
        # if the new speed is greater than the current speed
        if wanted_speed > self.speed:
            self.speed = self.add_to_current_value(self.speed,wanted_speed,self.get_offset(current_max_acceleration))
        else:
            self.speed = self.add_to_current_value(self.speed,wanted_speed,self.get_offset(-current_max_acceleration))

        if (self.is_in_zero_range(self.speed)):
            self.speed = 0
        
    
    def move(self, distance:float, backward:bool=False, is_decc:bool=True) -> bool:
        """
        Description:      Move the car forward of x meters.
        Parameters:
            distance:     distance in meters to move forward to.
        Return:           bool when finished.
        """
        new_distance = self.get_speed(in_meters_per_second=True) * self.time_module.get_dt_in_seconds()
        self.distance_parcourue += new_distance
        if backward:
            m = -1
        else:
            m = 1

        if self.move_forward_state == MoveForwardState.STARTING:
            self.move_forward_state = MoveForwardState.MOVING_ACC
            self.distance_parcourue = 0.0
            self.distance_acceleration = 0.0

        new_speed = m*self.config.maxSpeed
        
        # État d'accélération
        if self.move_forward_state == MoveForwardState.MOVING_ACC:
            self.distance_acceleration += new_distance
            if self.get_speed() == new_speed:
                self.move_forward_state = MoveForwardState.MOVING_FORWARD
            elif is_decc and self.distance_acceleration * 2 >= distance:
                self.move_forward_state = MoveForwardState.MOVING_DECC
        # État de mouvement
        if self.move_forward_state == MoveForwardState.MOVING_FORWARD:
            if not is_decc and self.distance_parcourue >= distance:
                self.move_forward_state = MoveForwardState.STOP
            elif is_decc and self.distance_parcourue + self.distance_acceleration >= distance:
                new_speed = 0
                self.move_forward_state = MoveForwardState.MOVING_DECC

        # État de décélération
        if self.move_forward_state == MoveForwardState.MOVING_DECC:
            new_speed = 0
            if self.get_speed() == 0:
                self.move_forward_state = MoveForwardState.STOP
            else:
                self.move_forward_state = MoveForwardState.MOVING_DECC

        # État d'arrêt
        if self.move_forward_state == MoveForwardState.STOP:
            self.distance_parcourue = 0.0
            self.distance_acceleration = 0.0
            self.move_forward_state = MoveForwardState.STARTING
            return True
        
        self.set_speed(new_speed)
        return False
    def is_wheel_centered(self) -> bool:
        return self.get_angle() == self.config.centerAngle
    
    def turn_to_angle(self, direction:Direction, angle:int=0, backward:bool=False, is_decc:bool=True) -> bool:
        """
        Description:
         Parameters:
            direction:    (int) 0 for left, 1 for right.
            angle:        (int) Angle en degré.
        Return: void.
        """
        print(self.turn_to_angle_state)
        self.longueur_arc = np.deg2rad(angle) * self.get_curvature(self.get_angle())
        # État initial
        if self.turn_to_angle_state == TurnState.STARTING:
            self.turn_to_angle_state = TurnState.TURNING_WHEEL
        
        # État de rotation
        elif self.turn_to_angle_state == TurnState.TURNING_WHEEL:
            if direction == Direction.LEFT_DIRECTION:
                if self.get_angle() == self.config.maxLeftAngle:
                    self.turn_to_angle_state = TurnState.MOVING_FORWARD
                else:
                    self.set_angle(self.config.maxLeftAngle)
            elif direction == Direction.RIGHT_DIRECTION:
                if self.get_angle() == self.config.maxRightAngle:
                    self.turn_to_angle_state = TurnState.MOVING_FORWARD
                else:
                    self.set_angle(self.config.maxRightAngle)
        
        # État de mouvement
        elif self.turn_to_angle_state == TurnState.MOVING_FORWARD:
            if self.move(self.longueur_arc, backward, is_decc=is_decc):
                self.turn_to_angle_state = TurnState.RETOUR_ANGLE
        
        # État retour angle
        elif self.turn_to_angle_state == TurnState.RETOUR_ANGLE:
            if self.get_angle() == self.config.centerAngle:
                self.turn_to_angle_state = TurnState.STOP
            else:
                self.set_angle(self.config.centerAngle)

        # État d'arrêt
        elif self.turn_to_angle_state == TurnState.STOP:
            self.turn_to_angle_state = TurnState.STARTING
            return True
        
        return False

        
