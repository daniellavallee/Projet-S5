from pathlib import Path
from datetime import datetime

CONFIGS_PATH = Path(__file__).parent.parent.parent / 'configs'
OUTPUTS_PATH = Path(__file__).parent.parent.parent / 'output'

OUTPUTS_PATH.mkdir(parents=True, exist_ok=True)

LINE_FOLLOWER_CONFIG = CONFIGS_PATH / 'line_follower.json'
SONAR_CONFIG = CONFIGS_PATH / 'sonar.json'
MOTOR_CONFIG = CONFIGS_PATH / 'motors.json'

SAMPLES_PATH = OUTPUTS_PATH / f'samples-{datetime.now().timestamp()}.csv'