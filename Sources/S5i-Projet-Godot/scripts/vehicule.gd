extends VehicleBody3D
class_name Vehicule

@export var MAX_STEER = 0.6
@export var ENGINE_POWER = 100
const USE_WEBSOCKET = true

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if USE_WEBSOCKET :
		# Direction des roues
		var radian = (90 - GlobalData.wheel_angle) * PI / 180
		steering = move_toward(steering, radian  * MAX_STEER, delta * 20)
		# Avance ou recule
		engine_force = GlobalData.bw_speed / 100 * ENGINE_POWER
		if linear_velocity.length() > 1 and GlobalData.bw_speed < 37:
			brake = 3
		else:
			brake = 0.5
	else :
		steering = move_toward(steering, Input.get_axis("right","left") * MAX_STEER, delta * 2.5)
		engine_force = Input.get_axis("down","up") * ENGINE_POWER
		
