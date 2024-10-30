from src.models import LineFollowerConfig, RaspberryPiResponse, ControllerResponse
from src.enums import RunStates
from .motors import Motors


class LineFollower():
    lastValue = [0, 0, 0, 0, 0]
    """
    Class responsible for handling the line follower sensor
    """

    def __init__(self, config: LineFollowerConfig, motors_module: Motors, verbose: bool = False):
        self.config = config
        self.verbose = verbose
        self.off_track_count = 0
        self.turning_angle = 90
        self.motors_module = motors_module

    def read(self, rpi_response:RaspberryPiResponse) -> list[bool]:
        digital_values = [value < self.config.min_white for value in rpi_response.line_follower]
        if self.verbose:
            print("Line follower | Analog values : ", digital_values)
            print("Line follower | Digital values : ", digital_values)
            print("==============================")
        return digital_values

    def run_follower(self, rpi_response: RaspberryPiResponse) -> RunStates:
        values = self.read(rpi_response)
        a_step = 3
        b_step = 10
        c_step = 30
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
        # Direction calculate
        if values == [0, 0, 1, 0, 0]:
            self.off_track_count = 0
            self.turning_angle = 90
        # turn right
        elif values in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
            self.off_track_count = 0
            self.turning_angle = int(90 - step)
        # turn left
        elif values in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
            self.off_track_count = 0
            self.turning_angle = int(90 + step)
        elif values == [0, 0, 0, 0, 0]:
            self.off_track_count += 1
            if self.off_track_count > 10:
                return RunStates.FINDING_LINE
        else:
            self.off_track_count = 0

        self.motors_module.set_angle(self.turning_angle)
        self.motors_module.set_speed(self.config.cruising_speed)
        self.lastValue = values
        return RunStates.LINE_FOLLOWING

    def found_line(self, values: list[bool]) -> RunStates:
        if values == [0, 0, 0, 0, 0]:
            return RunStates.FINDING_LINE
        return RunStates.LINE_FOLLOWING

    def run_finder(self, rpi_response: RaspberryPiResponse) -> RunStates:

        values = self.read(rpi_response)
        
        self.off_track_count += 1
        center_angle = self.motors_module.config.maxRightAngle - self.motors_module.config.maxLeftAngle
        #if self.off_track_count > self.config.max_off_track_count or True:
        #    self.motors_module.set_angle(45)
        #    self.motors_module.set_speed(100)
        #else:
        #    self.motors_module.set_angle(center_angle)
        #    self.motors_module.set_speed(0)
        print("Finder | Off track count : ",self.off_track_count)
        self.motors_module.set_angle(center_angle)
        self.motors_module.set_speed(0)
        return self.found_line(values)
