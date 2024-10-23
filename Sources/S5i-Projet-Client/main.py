from src.ws import WebSocketClient
from src.json_helper import read_raspberry_pi_response, write_controller_response
from src.models import ControllerResponse

USE_RASPBERRY_PI = False

if USE_RASPBERRY_PI:
    HOST = "192.168.72.62"
else:
    HOST = "localhost"
PORT = 42069

ws = WebSocketClient(HOST, PORT)

response = ControllerResponse(0, 0)
while True:
    message = write_controller_response(response)
    ws.send(message)
    result =  ws.recv()
    rpr = read_raspberry_pi_response(result)
    print("Received '%s'" % rpr)