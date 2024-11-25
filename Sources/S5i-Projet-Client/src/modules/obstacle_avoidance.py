from src.enums.states import RunStates
from src.modules.motors import Motors
from src.models import RaspberryPiResponse, ObstacleAvoidanceConfig
from src.enums import ObstacleAvoidanceState, Direction
#from scipy import stats


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
        self.is_decc = True
        self.sonar_buffer = []
        self.max_samples = 100
        # Obstacle avoidance state
        self.obstacle_avoidance_state = ObstacleAvoidanceState.STARTING

    def is_obstacle_detected(self, RPi_response:RaspberryPiResponse)->bool:
        """
        Description: This method is responsible for checking if an obstacle is detected.
        """
        corrected_value = RPi_response.sonar * 0.9638523     # 0.9638523 is the correction factor from linear regression
        detected = corrected_value < self.config.obstacleDetectedDistance and corrected_value > -1
        #return detected
        if len(self.sonar_buffer) < 5:
            return False
        
        # t-test
        moyenne = sum(self.sonar_buffer)/len(self.sonar_buffer)
        mu = self.config.obstacleDetectedDistance
        variance_ech = sum([(x - moyenne)**2 for x in self.sonar_buffer])/(len(self.sonar_buffer)-1)
        t_stat = (moyenne - mu)/(variance_ech/len(self.sonar_buffer)**0.5)
        print("t_stat: ", t_stat)

        #t_stat, p_value = stats.ttest_1samp(self.sonar_buffer, RPi_response.sonar)
        ##print("Le p-value est: ", p_value)
        if len(self.sonar_buffer) >= self.max_samples:
            self.sonar_buffer.pop(0)
        self.sonar_buffer.append(RPi_response.sonar)
        print("Sonar : ", RPi_response.sonar)
        print("Sonar buffer: ", sum(self.sonar_buffer)/len(self.sonar_buffer))

        # Retourner false si le t-test est significatif a un seuil de 5%
        if t_stat < 1.98:
            return False
        
        #if p_value < 0.05:
        #    return False

        
        #print("Detected: ", detected)
        #print("obstacledetecteddistance: ", self.config.obstacleDetectedDistance)
        return detected
    
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
            if self.motor_module.move(self.config.backwardDistance, backward=True, is_decc=self.is_decc):
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
            if self.motor_module.move(self.config.straightDistance3, is_decc=self.is_decc):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_4
                
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.AVOIDING_OBSTACLE_TURN_4):
            if self.motor_module.turn_to_angle(Direction.RIGHT_DIRECTION, self.config.turnAngle4, is_decc=self.is_decc):
                self.obstacle_avoidance_state = ObstacleAvoidanceState.STOP
        
        elif (self.obstacle_avoidance_state == ObstacleAvoidanceState.STOP):
            self.obstacle_avoidance_state = ObstacleAvoidanceState.STARTING
            return RunStates.LINE_FOLLOWING
        
        return RunStates.OBSTACLE_AVOIDANCE
        

    
