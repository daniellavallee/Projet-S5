from src.models import LineFollowerConfig, RaspberryPiResponse, ControllerResponse
from src.enums import RunStates
from .motors import Motors
import numpy as np

class LineFollower():
    lastValue = [0, 0, 0, 0, 0]
    """
    Class responsible for handling the line follower sensor
    """

    def __init__(self, config: LineFollowerConfig, motors_module: Motors, verbose: bool = False):
        self.config = config
        self.verbose = verbose
        self.motors_module = motors_module
        self.turning_angle = self.motors_module.config.centerAngle
        self.sampleBuffer = []
        self.maxSamples = 50
        self.is_in_straight_line = False

    def read(self, rpi_response:RaspberryPiResponse) -> list[bool]:
        digital_values = [value < self.config.min_white for value in rpi_response.line_follower]
        if self.verbose:
            print("Line follower | Analog values : ", digital_values)
            print("Line follower | Digital values : ", digital_values)
            print("==============================")
        return digital_values

    def get_speed(self, values: list[bool]) -> float:
        current_value = self.get_current_value(values)
        if len(self.sampleBuffer) >= self.maxSamples:
            self.sampleBuffer.pop(0)
        self.sampleBuffer.append(4*current_value)
        # Calculate the standard deviation of the sample buffer
        factor_decc = np.std(self.sampleBuffer)
        
        diff = self.config.cruising_speed - self.config.finders_speed
        return self.config.cruising_speed - factor_decc * diff
    
    def get_current_value(self, values: list[bool]) -> float:
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
        
        a_step = 10
        b_step = 15
        c_step = 30
        d_step = 35
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
        elif values == [1, 1, 1, 1, 1] and self.is_in_straight_line:
            return RunStates.STOP
        # turn right
        elif values in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
            self.turning_angle = int(self.motors_module.config.centerAngle - step)
        # turn left
        elif values in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
            self.turning_angle = int(self.motors_module.config.centerAngle + step)
        elif values == [0, 0, 0, 0, 0]:
            return RunStates.FINDING_LINE

        self.motors_module.set_angle(self.turning_angle)
        self.motors_module.set_speed(self.get_speed(values))
        self.lastValue = values
        return RunStates.LINE_FOLLOWING

    def found_line(self, values: list[bool]) -> RunStates:
        if any(values):
            return RunStates.LINE_FOLLOWING
        return RunStates.FINDING_LINE

    def run_finder(self, rpi_response: RaspberryPiResponse) -> RunStates:
        values = self.read(rpi_response)
        step = 45 

        if self.lastValue == [0, 0, 0, 1, 0] or self.lastValue == [0, 0, 0, 0, 1]: 
            self.turning_angle = int(self.motors_module.config.centerAngle + step) 
        if self.lastValue == [0, 1, 0, 0, 0] or self.lastValue == [1, 0, 0, 0, 0]: 
            self.turning_angle = int(self.motors_module.config.centerAngle - step) 
        self.motors_module.set_angle(self.turning_angle) 
        self.motors_module.set_speed(self.config.finders_speed)
        
        return self.found_line(values)

    def run_stop(self) -> RunStates:
        self.motors_module.set_speed(0)
        self.motors_module.set_angle(90)
        return RunStates.STOP
