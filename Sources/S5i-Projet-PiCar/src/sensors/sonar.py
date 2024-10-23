from ..sonar_module import Ultrasonic_Avoidance

ua = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)

def read_sonar() -> int:
    return ua.get_distance()