from enum import Enum

class RunStates(Enum):
    STARTING = 1
    LINE_FOLLOWING = 2
    FINDING_LINE = 3
    OBSTACLE_AVOIDANCE = 4
    STOP = 5

class MoveForwardState(Enum):
    STARTING = 1
    MOVING_ACC = 2
    MOVING_FORWARD = 3
    MOVING_DECC = 4
    STOP = 5
    

    