extends Node3D

var speed = 1

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if Input.is_action_pressed("ui_left"):
		position += Vector3.RIGHT * delta * speed
	if Input.is_action_pressed("ui_right"):
		position += Vector3.LEFT * delta * speed
	if Input.is_action_pressed("ui_up"):
		position += Vector3.BACK * delta * speed
	if Input.is_action_pressed("ui_down"):
		position += Vector3.FORWARD * delta * speed
