from src import read_controller_response, write_raspberry_pi_response, RaspberryPiResponse
from src.controller import control
from datetime import datetime
from src.network import get_ip_address
from src.sensors import read_line_follower, read_sonar
import asyncio
from websockets.server import serve, WebSocketServerProtocol

async def echo(websocket: WebSocketServerProtocol):
    async for message in websocket:
        try:
            controller_response = read_controller_response(message)
            #print(f"Received: {controller_response}")
            control(controller_response)
            line_follower = read_line_follower()
            sonar = read_sonar()
            time = datetime.now().isoformat()
            
            response = RaspberryPiResponse(line_follower, sonar, time)
            raspberry_pi_response = write_raspberry_pi_response(response)
            #print(f"Sent: {raspberry_pi_response}")
            await websocket.send(raspberry_pi_response)
        except Exception as e:
            print(f"Error: {e}")

async def main():
    print(f"Server started at ws://{get_ip_address('wlan0')}:42069")
    async with serve(echo, "0.0.0.0", 42069):
        await asyncio.get_running_loop().create_future()  # run forever

asyncio.run(main())