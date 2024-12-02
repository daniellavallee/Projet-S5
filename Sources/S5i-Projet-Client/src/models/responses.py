from dataclasses import dataclass
import datetime
from typing import List
@dataclass
class RaspberryPiResponse:
    line_follower:List[int]
    sonar:int
    time:str
    def get_datetime(self):
        return datetime.datetime.fromisoformat(self.time)

@dataclass
class ControllerResponse:
    wheel_angle:int
    bw_speed:int
    block_wheel:bool