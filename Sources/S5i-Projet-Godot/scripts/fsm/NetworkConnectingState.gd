class_name NetworkFSMConnectingState
extends StateMachineState

const PORT = 42069
var current_value = "BLANK"
# Called when the state machine enters this state.
func on_enter() -> void:
	print("Network Connecting State entered")
	# You should connect to the websocket server here. With the socket variable of NetworkFSM
	get_parent().socket.client_connected.connect(_connected)
	get_parent().socket.client_disconnected.connect(_disconnected)
	get_parent().socket.message_received.connect(_on_data)
	# Start listening on the given port.
	var err = get_parent().socket.listen(PORT)
	if err != OK:
		print("Unable to start server")
		set_process(false)

# Called every frame when this state is active.
func on_process(delta: float) -> void:
	get_parent().socket.poll()


# Called every physics frame when this state is active.
func on_physics_process(delta: float) -> void:
	pass
	


# Called when there is an input event while this state is active.
func on_input(event: InputEvent) -> void:
	pass

# Called when the state machine exits this state.
func on_exit() -> void:
	print("Network Connecting State left")
	
func _connected(id, proto):
	# This is called when a new peer connects, "id" will be the assigned peer id,
	# "proto" will be the selected WebSocket sub-protocol (which is optional)
	print("Client %d connected with protocol: %s" % [id, proto])

func _close_request(id, code, reason):
	# This is called when a client notifies that it wishes to close the connection,
	# providing a reason string and close code.
	print("Client %d disconnecting with code: %d, reason: %s" % [id, code, reason])

func _disconnected(id, was_clean = false):
	# This is called when a client disconnects, "id" will be the one of the
	# disconnecting client, "was_clean" will tell you if the disconnection
	# was correctly notified by the remote peer before closing the socket.
	print("Client %d disconnected, clean: %s" % [id, str(was_clean)])

func _on_data(id,message):
	# Print the received packet, you MUST always use get_peer(id).get_packet to receive data,
	# and not get_packet directly when not using the MultiplayerAPI.
	current_value = message
	print(message)
	get_parent().socket.send(id,message)
