import json
from .json_encoder import EnhancedJSONEncoder
from src.models import (
    ControllerResponse,
    RaspberryPiResponse,
    LineFollowerConfig,
    SonarConfig,
    MotorsConfig,
    ObstacleAvoidanceConfig
    )
from src.constants import LINE_FOLLOWER_CONFIG, SONAR_CONFIG, MOTOR_CONFIG, OBSTACLE_AVOIDANCE_CONFIG

def read_raspberry_pi_response(input:str) -> RaspberryPiResponse:
    data = json.loads(input)
    return RaspberryPiResponse(**data)

def write_controller_response(response:ControllerResponse) -> str:
    return json.dumps(response, cls=EnhancedJSONEncoder)

def read_configs()-> tuple[LineFollowerConfig, SonarConfig, MotorsConfig, ObstacleAvoidanceConfig]:
    with LINE_FOLLOWER_CONFIG.open("r") as f:
        data = json.load(f)
        line_follower = LineFollowerConfig(**data)
    with SONAR_CONFIG.open("r") as f:
        data = json.load(f)
        sonar = SonarConfig(**data)
    with MOTOR_CONFIG.open("r") as f:
        data = json.load(f)
        motors = MotorsConfig(**data)
    with OBSTACLE_AVOIDANCE_CONFIG.open("r") as f:
        data = json.load(f)
        obstacle_avoidance = ObstacleAvoidanceConfig(**data)
    return line_follower, sonar, motors, obstacle_avoidance