from enum import Enum

class RunStates(Enum):
    STARTING = 1
    LINE_FOLLOWING = 2
    FINDING_LINE = 3
    OBSTACLE_AVOIDANCE = 4
    STOP = 5
    