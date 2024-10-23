import json
from .json_encoder import EnhancedJSONEncoder
from .models import ControllerResponse, RaspberryPiResponse

def read_raspberry_pi_response(input:str) -> RaspberryPiResponse:
    data = json.loads(input)
    return RaspberryPiResponse(**data)

def write_controller_response(response:ControllerResponse) -> str:
    return json.dumps(response, cls=EnhancedJSONEncoder)