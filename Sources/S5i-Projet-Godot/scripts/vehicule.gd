extends VehicleBody3D
class_name Vehicule

@export var MAX_STEER = 0.6
@export var ENGINE_POWER = 30
@export var USE_WEBSOCKET = true
@onready var bille: RigidBody3D = $"../Bille"
var BREAK: bool = false
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float):
	if Input.is_action_pressed("reset"):
		get_parent().get_tree().reload_current_scene()
	if USE_WEBSOCKET :
		# Direction des roues
		var radian = (90 - GlobalData.wheel_angle) * PI / 180
		steering = move_toward(steering, radian  * MAX_STEER, delta * 20)
		# Avance ou recule
		engine_force = GlobalData.bw_speed / 100 * ENGINE_POWER
	else :
		steering = move_toward(steering, Input.get_axis("right","left") * MAX_STEER, delta * 2.5)
		engine_force = Input.get_axis("down","up") * ENGINE_POWER
