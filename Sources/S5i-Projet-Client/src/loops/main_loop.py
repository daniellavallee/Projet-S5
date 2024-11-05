from .base_loop import BaseLoop
from src.models import ControllerResponse, RaspberryPiResponse
from src.enums import Hosts, RunStates, Direction
from datetime import datetime
from src.constants import BACKWARD_DISTANCE, OBSTACLE_DETECTED_DISTANCE

class MainLoop(BaseLoop):
    def __init__(self, host: Hosts, *, is_verbose: bool = True) -> None:
        super().__init__(host, is_verbose=is_verbose)
        self.current_state : RunStates = RunStates.STARTING
    def control(self, rpi_response: RaspberryPiResponse):
        if self.current_state == RunStates.STARTING:
            self.current_state = RunStates.LINE_FOLLOWING
        elif self.current_state == RunStates.LINE_FOLLOWING:
            self.current_state = self.line_follower_module.run_follower(rpi_response)
        elif self.current_state == RunStates.FINDING_LINE:
            self.current_state = self.line_follower_module.run_finder(rpi_response)
        elif self.current_state == RunStates.OBSTACLE_AVOIDANCE:
            self.current_state = self.obstacle_manager.run(rpi_response)
            
        if self.current_state == RunStates.STOP:
            self.motors_module.set_speed(0)
            self.motors_module.set_angle(self.motors_cfg.centerAngle)
        elif rpi_response.sonar <= OBSTACLE_DETECTED_DISTANCE and rpi_response.sonar != -1:
            self.current_state = RunStates.OBSTACLE_AVOIDANCE