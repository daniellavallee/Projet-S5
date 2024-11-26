from src.models import LineFollowerConfig, RaspberryPiResponse, ControllerResponse
from src.enums import RunStates
from .motors import Motors, Time
import numpy as np
import time
class LineFollower():
    lastValue = [0, 0, 0, 0, 0]
    """
    Class responsible for handling the line follower sensor
    """

    def __init__(self, config: LineFollowerConfig, motors_module: Motors, time_module:Time, verbose: bool = False):
        self.config = config
        self.verbose = verbose
        self.motors_module = motors_module
        self.time_module = time_module
        self.turning_angle = self.motors_module.config.centerAngle
        self.sampleBuffer = []
        self.maxSamples = 20
        self.is_in_straight_line = False
        self.missings_line_counter = 0
        self.was_turning = True

    def read(self, rpi_response:RaspberryPiResponse):
        digital_values = [value < self.config.min_white for value in rpi_response.line_follower]
        return digital_values

    def get_speed(self, values) -> float:
        current_value = self.get_current_value(values)
        if len(self.sampleBuffer) >= self.maxSamples:
            self.sampleBuffer.pop(0)
        self.sampleBuffer.append(current_value)
        # Calculate the standard deviation of the sample buffer
        factor_decc = np.std(self.sampleBuffer)
        
        diff = self.config.cruising_speed - self.config.finders_speed
        return self.config.cruising_speed - factor_decc * diff
    
    def get_current_value(self, values) -> float:
        indexes  = []
        for i,value in enumerate(values):
            if value:
                indexes.append(i)
        if len(indexes) == 0:
            if self.lastValue == [0, 0, 0, 1, 0] or self.lastValue == [0, 0, 0, 0, 1]:
                return 1
            if self.lastValue == [0, 1, 0, 0, 0] or self.lastValue == [1, 0, 0, 0, 0]:
                return -1
            return 0
        center_index = sum(indexes) / len(indexes) / 4
        center_index = -(center_index * 2 - 1)
    
        return center_index
    
    def run_follower(self, rpi_response: RaspberryPiResponse) -> RunStates:
        values = self.read(rpi_response)
        
        a_step = 5
        b_step = 10
        c_step = 17
        d_step = 45
        # Angle calculate
        if values == [0, 0, 1, 0, 0]:
            step = 0
        elif values == [0, 1, 1, 0, 0] or values == [0, 0, 1, 1, 0]:
            step = a_step
        elif values == [0, 1, 0, 0, 0] or values == [0, 0, 0, 1, 0]:
            step = b_step
        elif values == [1, 1, 0, 0, 0] or values == [0, 0, 0, 1, 1]:
            step = c_step
        elif values == [1, 0, 0, 0, 0] or values == [0, 0, 0, 0, 1]:
            step = d_step
        
        # If the center sensor is activated, the robot is in a straight line
        self.is_in_straight_line = values[3]
        
        # Direction calculate
        if values == [0, 0, 1, 0, 0]:
            self.turning_angle = self.motors_module.config.centerAngle
            self.was_turning = False
            self.missings_line_counter = 0
        elif values == [1, 1, 1, 1, 1] and self.is_in_straight_line:
            return RunStates.STOP
        # turn right
        elif values in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
            self.turning_angle = int(self.motors_module.config.centerAngle - step)
            self.was_turning = True
            self.missings_line_counter = 0
        # turn left
        elif values in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
            self.was_turning = True
            self.turning_angle = int(self.motors_module.config.centerAngle + step)
            self.missings_line_counter = 0
        elif values == [0, 0, 0, 0, 0]:
            if self.was_turning:
                self.missings_line_counter += self.time_module.get_dt_in_seconds()
                if self.missings_line_counter > 1.5:
                    self.missings_line_counter = 0
                    return RunStates.FINDING_LINE
                else:
                    return RunStates.LINE_FOLLOWING
            else:
                return RunStates.FINDING_LINE

        self.motors_module.set_angle(self.turning_angle)
        self.motors_module.set_speed(self.get_speed(values))
        self.lastValue = values
        return RunStates.LINE_FOLLOWING

    def found_line(self, response: RaspberryPiResponse) -> bool:
        return any(self.read(response))

    def run_finder(self, rpi_response: RaspberryPiResponse) -> RunStates:
        values = self.read(rpi_response)
        step = 45 

        if self.lastValue == [0, 0, 0, 1, 0] or self.lastValue == [0, 0, 0, 0, 1]: 
            self.turning_angle = int(self.motors_module.config.centerAngle - step) 
        else: 
            self.turning_angle = int(self.motors_module.config.centerAngle + step)
        
        if any(values):
            self.motors_module.set_angle(self.motors_module.config.centerAngle) 
            self.motors_module.set_speed(0) 
            if self.motors_module.is_wheel_centered():
                time.sleep(1)
                return RunStates.LINE_FOLLOWING
        else:   
            self.motors_module.set_angle(self.turning_angle) 
            self.motors_module.set_speed(-self.config.finders_speed)
        
        return RunStates.FINDING_LINE
