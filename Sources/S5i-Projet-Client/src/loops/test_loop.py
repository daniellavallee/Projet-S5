import keyboard
import sys

from .base_loop import BaseLoop
from src.models import ControllerResponse, RaspberryPiResponse
from src.enums import Hosts

class TestLoop(BaseLoop):
    def __init__(self, host: Hosts = False) -> None:
        super().__init__(host, is_verbose=True)
    def control(self, rpi_response: RaspberryPiResponse) -> ControllerResponse:
        sys.stdout.flush()
        if keyboard.is_pressed('up'):
            self.motors_module.set_speed(self.motors_cfg.maxSpeed)
        elif keyboard.is_pressed('down'):
            self.motors_module.set_speed(self.motors_cfg.minSpeed)
        else:
            self.motors_module.set_speed(0)
        
        if keyboard.is_pressed('left'):
            self.motors_module.set_angle(self.motors_cfg.maxLeftAngle)
        elif keyboard.is_pressed('right'):
            self.motors_module.set_angle(self.motors_cfg.maxRightAngle)
        else:
            self.motors_module.set_angle(90)