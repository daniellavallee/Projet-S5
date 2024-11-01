import src.constants
from src.enums.states import RunStates
from src.modules.motors import Motors
from src.models import RaspberryPiResponse
from src.enums import ObstacleAvoidanceState


class ObstacleManager():
    """
    This class is responsible for handling the avoidance of an obstacle.
    """
    
    def __init__(self, motor_module:Motors, verbose:bool=False):
        """
        Description: This method is responsible for initializing the ObstacleManager class.
        """
        self.motor_module = motor_module
        self.verbose = verbose
        
        # Obstacle avoidance state
        self.obstacle_avoidance_state = ObstacleAvoidanceState.STARTING

    def is_obstacle_detected(self, RPi_response:RaspberryPiResponse)->bool:
        """
        Description: This method is responsible for checking if an obstacle is detected.
        """
        return RPi_response.sonar < src.constants.OBSTACLE_DETECTED_DISTANCE
    
    def run(self, RPi_response:RaspberryPiResponse)->RunStates:
        """
        Description: This method is responsible for running the obstacle avoidance algorithm.
        """
        
        if (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_1):
            if self.motor_module.turn_to_angle(src.constants.TURN_ANGLE_1):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_STRAIGHT_1
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_STRAIGHT_1):
            if self.motor_module.move(src.constants.STRAIGHT_DISTANCE_1):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_2
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_2):
            if self.motor_module.turn_to_angle(src.constants.TURN_ANGLE_2):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_STRAIGHT_2
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_STRAIGHT_2):
            if self.motor_module.move(src.constants.STRAIGHT_DISTANCE_2):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_3
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_3):
            if self.motor_module.turn_to_angle(src.constants.TURN_ANGLE_3):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_STRAIGHT_3
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_STRAIGHT_3):
            if self.motor_module.move(src.constants.STRAIGHT_DISTANCE_3):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.STOP
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.STOP):
            self.obstacle_avoidance_state = ObstacleAvoidanceState.STARTING
            return RunStates.LINE_FOLLOWING
        
        return RunStates.OBSTACLE_AVOIDANCE
        

    