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
    
class TurnState(Enum):
    STARTING = 1
    TURNING_WHEEL = 2
    MOVING_FORWARD = 3
    RETOUR_ANGLE = 4
    STOP = 5

class ObstacleAvoidanceState(Enum):
    STARTING = 1
    AVOIDING_OBSTACLE_TURN_1 = 2
    AVOIDING_OBSTACLE_STRAIGHT_1 = 3
    AVOIDING_OBSTACLE_TURN_2 = 4
    AVOIDING_OBSTACLE_STRAIGHT_2 = 5
    AVOIDING_OBSTACLE_TURN_3 = 6
    AVOIDING_OBSTACLE_STRAIGHT_3 = 7
    STOP = 8