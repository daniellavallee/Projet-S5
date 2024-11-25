import sys

from .base_loop import BaseLoop
from src.models import RaspberryPiResponse
from src.enums import Hosts
from src.constants import SAMPLES_PATH
#import keyboard
from datetime import timedelta

class CalibLoop(BaseLoop):
    def __init__(self, host: Hosts = False) -> None:
        super().__init__(host, is_verbose=False)
        self.samples : list[tuple[timedelta,int]] = []
        self.max_num_samples = 30
        if not SAMPLES_PATH.exists():
            with SAMPLES_PATH.open('w') as f:
                title = "Sample Name,dt,"
                for i in range(self.max_num_samples):
                    title += f"Sample {i},"
                title = title[:-1]
                title += "\n"
                f.write(title)
    def control(self, rpi_response: RaspberryPiResponse):
        sys.stdout.flush()
        self.obstacle_manager.is_obstacle_detected(rpi_response)
        print(rpi_response, end='\r')
        self.samples.append([self.time_module.dt,rpi_response.sonar])
        if len(self.samples) > self.max_num_samples:
            self.samples.pop(0)
        print(f"Samples: {sum([sample[1] for sample in self.samples])/self.max_num_samples}", end='\r')
        """
        if keyboard.is_pressed('space'):
            if len(self.samples) < self.max_num_samples:
                print("Not enough samples")
                return
            sys.stdout.flush()
            sample_name = input("\nEnter sample name:")
            
            with SAMPLES_PATH.open('a') as f:
                f.write(f"{sample_name.strip()},")
                f.write(f"{sum([sample[0].total_seconds() for sample in self.samples])/len(self.samples)}")
                for sample in self.samples:
                    f.write(f",{sample[1]}")
                f.write("\n")
            self.samples = []
        """