extends RayCast3D

@export var line_index : int = 0
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
		#and 
	if is_colliding() and get_collider().name.to_lower().contains("ligne"):
		GlobalData.line[line_index] = 0
	else:
		GlobalData.line[line_index] = 255
