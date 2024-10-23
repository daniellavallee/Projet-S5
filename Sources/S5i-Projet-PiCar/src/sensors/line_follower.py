from typing import List
from ..line_follower_module import Line_Follower

lf = Line_Follower.Line_Follower()

def read_line_follower() -> List[int]:
    return lf.read_analog()