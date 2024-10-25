extends VehicleBody3D
class_name Vehicule

const Lignes = preload("res://LigneNoir.gd")

@export var MAX_STEER = 0.9
@export var ENGINE_POWER = 300
const USE_WEBSOCKET = false 
var xy_cap1
var xy_cap2
var xy_cap3
var xy_cap4
var xy_cap5
var ligne1
var ligne2

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if USE_WEBSOCKET :
		pass
	else :
		steering = move_toward(steering, Input.get_axis("right","left") * MAX_STEER, delta * 10)
		engine_force = Input.get_axis("down","up") * ENGINE_POWER
	
	
	
