from dataclasses import dataclass
@dataclass
class LineFollowerConfig:
    min_white : int
    max_off_track_count : int
    finders_speed : int
    missing_line_distance: float

@dataclass
class SonarConfig:
    launch_stop_distance : int
    
@dataclass
class MotorsConfig:
    maxSpeed : int
    minSpeed : int
    maxAcceleration : int
    maxAngularAcc : int
    maxLeftAngle : int
    maxRightAngle : int
    maxSpeedInMeterPerSecond : float
    rayon_courbure: float
    maxZeroZone : int
    minZeroZone : int
    wheelDistance : float
    centerAngle : int

@dataclass
class ObstacleAvoidanceConfig:
    obstacleDetectedDistance : int
    turnAngle1 : int
    turnAngle2 : int
    turnAngle3 : int
    turnAngle4 : int
    straightDistance1 : int
    straightDistance2 : int
    straightDistance3 : int
    backwardDistance : int