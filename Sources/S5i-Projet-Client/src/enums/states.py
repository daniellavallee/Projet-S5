from enum import Enum

class RunStates(Enum):
    STARTING = 1
    LINE_FOLLOWING = 2
    FINDING_LINE = 3
    OBSTACLE_AVOIDANCE = 4
    OBSTACLE_DETECTED = 5
    BACKWARD = 6
    STOP = 7

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
    STOPPING = 2
    BACKWARD = 3
    SLEEPING = 4
    AVOIDING_OBSTACLE_TURN_1 = 5
    AVOIDING_OBSTACLE_STRAIGHT_1 = 6
    AVOIDING_OBSTACLE_TURN_2 = 7
    AVOIDING_OBSTACLE_STRAIGHT_2 = 8
    AVOIDING_OBSTACLE_TURN_3 = 9
    AVOIDING_OBSTACLE_STRAIGHT_3 = 10
    AVOIDING_OBSTACLE_TURN_4 = 11
    STOP = 12