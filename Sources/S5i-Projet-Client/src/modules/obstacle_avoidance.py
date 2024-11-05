from src.enums.states import RunStates
from src.modules.motors import Motors
from src.models import RaspberryPiResponse, ObstacleAvoidanceConfig
from src.enums import ObstacleAvoidanceState, Direction


class ObstacleManager():
    """
    This class is responsible for handling the avoidance of an obstacle.
    """
    
    def __init__(self, config : ObstacleAvoidanceConfig, motor_module:Motors, verbose:bool=False):
        """
        Description: This method is responsible for initializing the ObstacleManager class.
        """
        self.config = config
        self.motor_module = motor_module
        self.verbose = verbose
        
        # Obstacle avoidance state
        self.obstacle_avoidance_state = ObstacleAvoidanceState.STARTING

    def is_obstacle_detected(self, RPi_response:RaspberryPiResponse)->bool:
        """
        Description: This method is responsible for checking if an obstacle is detected.
        """
        return RPi_response.sonar < self.config.obstacleDetectedDistance and RPi_response.sonar != -1
    
    def run(self, RPi_response:RaspberryPiResponse)->RunStates:
        """
        Description: This method is responsible for running the obstacle avoidance algorithm.
        """
        if (self.obstacle_avoidance_state == ObstacleAvoidanceState.STARTING):
            self.obstacle_avoidance_state = ObstacleAvoidanceState.STOPPING
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.STOPPING):
            if self.motor_module.get_speed() == 0:
                self.obstacle_avoidance_state = ObstacleAvoidanceState.BACKWARD
            else:
                self.motor_module.set_speed(0)
                self.motor_module.set_angle(self.motor_module.config.centerAngle)
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.BACKWARD):
            if self.motor_module.move(self.config.backwardDistance, backward=True):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_1
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_1):
            if self.motor_module.turn_to_angle(Direction.RIGHT_DIRECTION, self.config.turnAngle1):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_STRAIGHT_1
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_STRAIGHT_1):
            if self.motor_module.move(self.config.straightDistance1):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_2
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_2):
            if self.motor_module.turn_to_angle(Direction.LEFT_DIRECTION, self.config.turnAngle2):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_STRAIGHT_2
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_STRAIGHT_2):
            if self.motor_module.move(self.config.straightDistance2):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_3
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_3):
            if self.motor_module.turn_to_angle(Direction.LEFT_DIRECTION, self.config.turnAngle3):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_STRAIGHT_3
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_STRAIGHT_3):
            if self.motor_module.move(self.config.straightDistance3):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.STOP
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.STOP):
            self.obstacle_avoidance_state = ObstacleAvoidanceState.STARTING
            return RunStates.LINE_FOLLOWING
        
        return RunStates.OBSTACLE_AVOIDANCE
        

    