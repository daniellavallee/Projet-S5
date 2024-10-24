from .base_loop import BaseLoop
from src.models import ControllerResponse, RaspberryPiResponse
from src.enums import Hosts, RunStates

class MainLoop(BaseLoop):
    def __init__(self, host: Hosts, *, is_verbose: bool = True) -> None:
        super().__init__(host, is_verbose=is_verbose)
        self.current_state : RunStates = RunStates.STARTING
    def get_controls(self, rpi_response: RaspberryPiResponse) -> ControllerResponse:
        self.time_module.update_time(rpi_response)
        if self.current_state == RunStates.STARTING:
            self.current_state = RunStates.LINE_FOLLOWING
        if self.current_state == RunStates.LINE_FOLLOWING:
            self.current_state = self.line_follower_module.run_follower(rpi_response)
        if self.current_state == RunStates.FINDING_LINE:
            self.motors_module.angle = self.line_follower_module.run_finder(rpi_response)
        return ControllerResponse(self.motors_module.angle, self.motors_module.speed)