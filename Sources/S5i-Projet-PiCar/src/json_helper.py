import json
from .json_encoder import EnhancedJSONEncoder
from .models import ControllerResponse, RaspberryPiResponse

def read_controller_response(input:str) -> ControllerResponse:
    data = json.loads(input)
    return ControllerResponse(**data)

def write_raspberry_pi_response(response:RaspberryPiResponse) -> str:
    return json.dumps(response, cls=EnhancedJSONEncoder)