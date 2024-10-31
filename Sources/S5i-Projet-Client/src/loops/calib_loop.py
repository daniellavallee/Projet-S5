import sys

from .base_loop import BaseLoop
from src.models import ControllerResponse, RaspberryPiResponse
from src.enums import Hosts
from src.constants import SAMPLES_PATH
import keyboard

class CalibLoop(BaseLoop):
    def __init__(self, host: Hosts = False) -> None:
        super().__init__(host, is_verbose=False)
        self.samples : list[float] = []
        self.max_num_samples = 30
        if not SAMPLES_PATH.exists():
            with SAMPLES_PATH.open('w') as f:
                title = "Sample Name, "
                for i in range(self.max_num_samples):
                    title += f"Sample {i},"
                title = title[:-1]
                title += "\n"
                f.write(title)
    def control(self, rpi_response: RaspberryPiResponse) -> ControllerResponse:
        sys.stdout.flush()
        print(rpi_response, end='\r')
        self.samples.append(rpi_response.sonar)
        if len(self.samples) >= self.max_num_samples:
            self.samples.pop(0)
        if keyboard.is_pressed('space'):
            sys.stdout.flush()
            sample_name = input("\nEnter sample name:")
            
            with SAMPLES_PATH.open('a') as f:
                f.write(f"{sample_name.strip()}")
                for sample in self.samples:
                    f.write(f",{sample}")
                f.write("\n")
        