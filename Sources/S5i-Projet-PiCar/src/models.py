from dataclasses import dataclass
from typing import List
@dataclass
class RaspberryPiResponse:
    line_follower:List[int]
    sonar:int
    time:str

@dataclass
class ControllerResponse:
    wheel_angle:int
    bw_speed:int