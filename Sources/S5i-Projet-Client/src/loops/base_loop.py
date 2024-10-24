from abc import ABC, abstractmethod
from src.constants import RPI_HOST, GODOT_HOST, PORT
from src.enums import Hosts
from src.models import ControllerResponse, RaspberryPiResponse
from src.ws.client import WebSocketClient
from src.json import read_raspberry_pi_response, write_controller_response, read_configs
from src.modules import Motors, LineFollower, Time
class BaseLoop(ABC):
    def __init__(self, host: Hosts, *, is_verbose:bool = True) -> None:
        if (host.value == Hosts.RaspberryPi.value):
            self.host = RPI_HOST
        else:
            self.host = GODOT_HOST
        self.is_verbose = is_verbose
        self.read_configs()
        self.time_module = Time()
        self.motors_module = Motors(self.motors_cfg, self.time_module, verbose=self.is_verbose)
        self.line_follower_module = LineFollower(self.line_follower_cfg, self.motors_module, verbose=self.is_verbose)
    @abstractmethod
    def get_controls(self, rpi_response:RaspberryPiResponse) -> ControllerResponse:
        pass
    def read_configs(self):
        self.line_follower_cfg, self.sonar_cfg, self.motors_cfg = read_configs()
    def run(self):
        ws = WebSocketClient(self.host, PORT)
        response = ControllerResponse(0, 0)
        while True:
            message = write_controller_response(response)
            print("Sending '%s'" % response)
            ws.send(message)
            result = ws.recv()
            rpr = read_raspberry_pi_response(result)
            controls = self.get_controls(rpr)
            response = ControllerResponse(*controls)
            if self.is_verbose:
                print("Received '%s'" % rpr)