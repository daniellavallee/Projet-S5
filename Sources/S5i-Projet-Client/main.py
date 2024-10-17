from src.ws import WebSocketClient

HOST = "localhost"
PORT = 42069

ws = WebSocketClient(HOST, PORT)

while True:
    ws.send("Hello, World")
    print("Sent")
    print("Receiving...")
    result =  ws.recv()
    print("Received '%s'" % result)