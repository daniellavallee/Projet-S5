from pathlib import Path

CONFIGS_PATH = Path(__file__).parent.parent.parent / 'configs'

LINE_FOLLOWER_CONFIG = CONFIGS_PATH / 'line_follower.json'
SONAR_CONFIG = CONFIGS_PATH / 'sonar.json'
MOTOR_CONFIG = CONFIGS_PATH / 'motors.json'
OBSTACLE_AVOIDANCE_CONFIG = CONFIGS_PATH / 'obstacle_avoidance.json'
