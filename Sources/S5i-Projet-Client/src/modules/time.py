from datetime import datetime, timedelta
from src.models import RaspberryPiResponse

class Time():
    """
    This class is responsible for handling the time
    """
    def __init__(self) -> None:
        self.last_datetime = datetime.now()
        self.dt : timedelta = timedelta(0)
    def update_time(self, response:RaspberryPiResponse):
        current_datetime = response.get_datetime()
        self.dt = current_datetime - self.last_datetime
        self.last_datetime = current_datetime
    def get_dt_in_seconds(self) -> float:
        return self.dt.total_seconds()