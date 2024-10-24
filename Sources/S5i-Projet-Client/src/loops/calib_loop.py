import sys

from .base_loop import BaseLoop
from src.models import ControllerResponse, RaspberryPiResponse
from src.enums import Hosts

class CalibLoop(BaseLoop):
    def __init__(self, host: Hosts = False) -> None:
        super().__init__(host, is_verbose=False)
    def get_controls(self, rpi_response: RaspberryPiResponse) -> ControllerResponse:
        sys.stdout.flush()
        print(rpi_response, end='\r')
        return ControllerResponse(0, 0)