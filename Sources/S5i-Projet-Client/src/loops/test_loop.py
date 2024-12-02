import keyboard
import sys

from .base_loop import BaseLoop
from src.models import ControllerResponse, RaspberryPiResponse
from src.enums import Hosts
from time import sleep
class TestLoop(BaseLoop):
    def __init__(self, host: Hosts = False, *, is_verbose: bool) -> None:
        super().__init__(host, is_verbose=is_verbose)
    def control(self, rpi_response: RaspberryPiResponse) -> ControllerResponse:
        sys.stdout.flush()
        self.obstacle_manager.is_obstacle_detected(rpi_response)
        if keyboard.is_pressed('up'):
            self.motors_module.set_speed(self.motors_cfg.maxSpeed)
        elif keyboard.is_pressed('down'):
            self.motors_module.set_speed(-self.motors_cfg.maxSpeed)
        else:
            self.motors_module.set_speed(0)
        
        if keyboard.is_pressed('left'):
            self.motors_module.set_angle(self.motors_cfg.maxLeftAngle)
        elif keyboard.is_pressed('right'):
            self.motors_module.set_angle(self.motors_cfg.maxRightAngle)
        else:
            self.motors_module.set_angle(self.motors_cfg.centerAngle)