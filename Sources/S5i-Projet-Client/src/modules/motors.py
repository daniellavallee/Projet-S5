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
            speed = np.abs(self.speed)
            if speed >= self.config.maxZeroZone:
                get_speed_ratio = (speed - self.config.maxZeroZone) / (self.config.maxSpeed - self.config.maxZeroZone)
            return get_speed_ratio * self.config.maxSpeedInMeterPerSecond
        return int(self.speed)
    def get_curvature(self, angle_in_degrees:float) -> float:
        angle = angle_in_degrees - self.config.centerAngle
        angle_rad : float = np.deg2rad(np.abs(angle))

        print(self.config.wheelDistance) 
        return self.config.wheelDistance / np.tan(angle_rad)
    
    
    def get_centrifugal_acceleration(self) -> float:
        return self.get_speed(in_meters_per_second=True) ** 2 * self.get_curvature(self.get_angle())
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
        
    
    def move(self, distance:float, backward:bool=False) -> bool:
        """
        Description:      Move the car forward of x meters.
        Parameters:
            distance:     distance in meters to move forward to.
        Return:           void.
        """
        new_distance = self.get_speed(in_meters_per_second=True) * self.time_module.get_dt_in_seconds()

        if backward:
            m = -1
        else:
            m = 1
        # État initiale
        if self.move_forward_state == MoveForwardState.STARTING:
            self.move_forward_state = MoveForwardState.MOVING_ACC
            self.distance_parcourue = 0.0
            self.distance_acceleration = 0.0

            print("État initial")

        # État d'accélération
        elif self.move_forward_state == MoveForwardState.MOVING_ACC:
            self.set_speed(m*self.config.maxSpeed)
            if self.get_speed() == m*self.config.maxSpeed:
                self.distance_parcourue += new_distance
                self.distance_acceleration += new_distance
                self.move_forward_state = MoveForwardState.MOVING_FORWARD
            elif self.distance_acceleration * 2 >= distance:
                self.move_forward_state = MoveForwardState.MOVING_DECC
                
            print("État d'accélération")
            

        # État de mouvement
        elif self.move_forward_state == MoveForwardState.MOVING_FORWARD:
            if self.distance_parcourue + self.distance_acceleration < distance:
                self.distance_parcourue += new_distance
                print("Distance parcourue: ", self.distance_parcourue)
                self.set_speed(m*self.config.maxSpeed)
            else:
                self.set_speed(0)
                self.move_forward_state = MoveForwardState.MOVING_DECC
        
            print("État de mouvement")

        # État de décélération
        elif self.move_forward_state == MoveForwardState.MOVING_DECC:
            if self.get_speed() == 0:
                self.move_forward_state = MoveForwardState.STOP
            else:
                self.set_speed(0)
                self.move_forward_state = MoveForwardState.MOVING_DECC
            
            print("État de décélération")

        # État d'arrêt
        elif self.move_forward_state == MoveForwardState.STOP:
            self.distance_parcourue = 0.0
            self.distance_accelerationo = 0.0
            self.move_forward_state = MoveForwardState.STARTING
            return True

        return False

    def turn_to_angle(self, direction:Direction, angle:int=0, backward:bool=False):
        """
        Description:
         Parameters:
            direction:    (int) 0 for left, 1 for right.
            angle:        (int) Angle en degré.
        Return: void.
        """
        
        self.longueur_arc = np.deg2rad(angle) * self.get_curvature(self.get_angle())
        print("rayon: ", self.get_curvature(self.get_angle()))
        # État initial
        if self.turn_to_angle_state == TurnState.STARTING:
            self.turn_to_angle_state = TurnState.TURNING_WHEEL
            
            print("État initial")
        
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
            print("État de rotation")
        
        # État de mouvement
        elif self.turn_to_angle_state == TurnState.MOVING_FORWARD:
            print("Longueur arc: ", self.longueur_arc)
            if self.move(self.longueur_arc, backward):
                self.turn_to_angle_state = TurnState.RETOUR_ANGLE
            # print("État de mouvement")
        
        # État retour angle
        elif self.turn_to_angle_state == TurnState.RETOUR_ANGLE:
            if self.get_angle() == 90:
                self.turn_to_angle_state = TurnState.STOP
            else:
                self.set_angle(90)
            print("État retour angle")

        # État d'arrêt
        elif self.turn_to_angle_state == TurnState.STOP:
            self.turn_to_angle_state = TurnState.STARTING
            print("État d'arrêt")
            return True

         
        
        

        