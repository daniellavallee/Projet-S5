from websocket import create_connection
class WebSocketClient():
    def __init__(self, host:str, port:int) -> None:
        self.ws = create_connection(f"ws://{host}:{port}")
        pass
    def send(self, message:str) -> None:
        self.ws.send(message)
    def recv(self) -> str:
        return self.ws.recv()
    def close(self) -> None:
        self.ws.close()