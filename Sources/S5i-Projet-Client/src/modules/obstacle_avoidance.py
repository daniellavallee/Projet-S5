from src.enums.states import RunStates
from src.modules import Motors, LineFollower
from src.models import RaspberryPiResponse, ObstacleAvoidanceConfig
from src.enums import ObstacleAvoidanceState, Direction
import numpy as np
#from scipy import stats


class ObstacleManager():
    """
    This class is responsible for handling the avoidance of an obstacle.
    """
    
    def __init__(self, config : ObstacleAvoidanceConfig, motor_module:Motors, line_follower:LineFollower, verbose:bool=False):
        """
        Description: This method is responsible for initializing the ObstacleManager class.
        """
        self.config = config
        self.motor_module = motor_module
        self.line_follower = line_follower
        self.verbose = verbose
        self.is_decc = False
        self.sonar_buffer = []
        self.max_samples = 5
        # Obstacle avoidance state
        self.obstacle_avoidance_state = ObstacleAvoidanceState.STARTING

    def is_obstacle_detected(self, RPi_response:RaspberryPiResponse)->bool:
        """
        Description: This method is responsible for checking if an obstacle is detected.
        """
        corrected_value = RPi_response.sonar + 5#* 0.9638523 - 1.67     # 0.9638523 is the correction factor from linear regression
        RPi_response.sonar = corrected_value

        if len(self.sonar_buffer) >= self.max_samples:
            self.sonar_buffer.pop(0)
        self.sonar_buffer.append(RPi_response.sonar)
        if len(self.sonar_buffer) < 5:
            return False
        moyenne_buffer = self.sonar_buffer #np.mean(self.sonar_buffer)
        
        return moyenne_buffer <= self.config.obstacleDetectedDistance and corrected_value > -1
    
    def run(self, RPi_response:RaspberryPiResponse)->RunStates:
        """
        Description: This method is responsible for running the obstacle avoidance algorithm.
        """
        #print(self.obstacle_avoidance_state)
        if (self.obstacle_avoidance_state == ObstacleAvoidanceState.STARTING):
            self.obstacle_avoidance_state = ObstacleAvoidanceState.STOPPING
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.STOPPING):
            if self.motor_module.get_speed() == 0:
                self.obstacle_avoidance_state = ObstacleAvoidanceState.BACKWARD
            else:
                self.motor_module.set_speed(0)
                self.motor_module.set_angle(self.motor_module.config.centerAngle)
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.BACKWARD):
            if self.motor_module.move(self.config.backwardDistance, backward=True, is_decc=True):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_1
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_1):
            if self.motor_module.turn_to_angle(Direction.RIGHT_DIRECTION, self.config.turnAngle1, is_decc=self.is_decc):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_STRAIGHT_1
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_STRAIGHT_1):
            if self.motor_module.move(self.config.straightDistance1, is_decc=self.is_decc):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_2
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_2):
            if self.motor_module.turn_to_angle(Direction.LEFT_DIRECTION, self.config.turnAngle2, is_decc=self.is_decc):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_STRAIGHT_2
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_STRAIGHT_2):
            if self.motor_module.move(self.config.straightDistance2, is_decc=self.is_decc):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_3
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_3):
            if self.motor_module.turn_to_angle(Direction.LEFT_DIRECTION, self.config.turnAngle3, is_decc=self.is_decc):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_STRAIGHT_3
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_STRAIGHT_3):
            if self.line_follower.found_line(RPi_response):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_4
            else:
                self.motor_module.set_speed(self.motor_module.config.maxSpeed)
                self.motor_module.set_angle(self.motor_module.config.centerAngle)
                
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_4):
            if self.motor_module.turn_to_angle(Direction.RIGHT_DIRECTION, self.config.turnAngle4, is_decc=self.is_decc):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.STOP
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.STOP):
            self.obstacle_avoidance_state = ObstacleAvoidanceState.STARTING
            return RunStates.LINE_FOLLOWING
        
        return RunStates.OBSTACLE_AVOIDANCE
        

    
