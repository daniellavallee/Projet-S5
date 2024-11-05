extends RayCast3D

var distance_null = -1

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if is_colliding():
		GlobalData.distance = round(global_transform.origin.distance_to(get_collision_point())*100 / 21.868)
	else:
		GlobalData.distance = distance_null

	print(GlobalData.distance)
