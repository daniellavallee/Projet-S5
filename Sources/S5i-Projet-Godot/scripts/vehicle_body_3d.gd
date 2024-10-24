extends VehicleBody3D
class_name Vehicule

const Lignes = preload("res://LigneNoir.gd")

@export var MAX_STEER = 0.9
@export var ENGINE_POWER = 300
const USE_WEBSOCKET = false 
var cap1
var cap2
var cap3
var cap4
var cap5
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
		
func get_pos_capteur() -> Array:
	cap1 = get_node("CapteurLigne1")
	cap2 = get_node("CapteurLigne2")
	cap3 = get_node("CapteurLigne3")
	cap4 = get_node("CapteurLigne4")
	cap5 = get_node("CapteurLigne5")
	
	xy_cap1 = cap1.get_world_3d()
	xy_cap2 = cap2.get_world_3d()
	xy_cap3 = cap3.get_world_3d()
	xy_cap4 = cap4.get_world_3d()
	xy_cap5 = cap5.get_world_3d()
	return [xy_cap1, xy_cap2, xy_cap3, xy_cap4, xy_cap5]
	
	print(xy_cap1)
	
	
	
