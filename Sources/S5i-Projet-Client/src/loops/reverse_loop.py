from .base_loop import BaseLoop
from src.models import  RaspberryPiResponse
from src.enums import Hosts, RunStates

class ReverseLoop(BaseLoop):
    def __init__(self, host: Hosts, *, is_verbose: bool = True) -> None:
        super().__init__(host, is_verbose=is_verbose)
        self.current_state : RunStates = RunStates.STARTING
    def control(self, rpi_response: RaspberryPiResponse):
        if self.current_state == RunStates.STARTING:
            self.current_state = RunStates.BACKWARD
        if self.current_state == RunStates.BACKWARD:
            if self.motors_module.move(0.29, backward=True, is_decc=True):
                self.current_state = RunStates.STOP
        elif self.current_state == RunStates.STOP:
            self.current_state = RunStates.OBSTACLE_AVOIDANCE