from .base_loop import BaseLoop
from src.models import ControllerResponse, RaspberryPiResponse
from src.enums import Hosts, RunStates, Direction

class MainLoop(BaseLoop):
    def __init__(self, host: Hosts, *, is_verbose: bool = True) -> None:
        super().__init__(host, is_verbose=is_verbose)
        self.current_state : RunStates = RunStates.STARTING
    def control(self, rpi_response: RaspberryPiResponse):
        if self.current_state == RunStates.STARTING:
            self.current_state = RunStates.OBSTACLE_AVOIDANCE
        if self.current_state == RunStates.LINE_FOLLOWING:
            self.current_state = self.line_follower_module.run_follower(rpi_response)
        if self.current_state == RunStates.FINDING_LINE:
            self.current_state = self.line_follower_module.run_finder(rpi_response)
        if self.current_state == RunStates.OBSTACLE_AVOIDANCE:
            if self.motors_module.turn_to_angle(Direction.LEFT_DIRECTION, 45, backward=False):
                self.current_state = RunStates.STOP
        elif self.current_state != RunStates.STOP:
            if self.obstacle_manager.is_obstacle_detected(rpi_response):
                self.current_state = RunStates.OBSTACLE_AVOIDANCE