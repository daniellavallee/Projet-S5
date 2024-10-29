extends RayCast3D

@onready var ligne: StaticBody3D = $"../../AreaLigneBlanche/Ligne"
@onready var plancher: StaticBody3D = $"../../AreaPlancher/Plancher"
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if is_colliding():
		if get_collider() == ligne:
			GlobalData.line[0] = 0
		else: if get_collider() == plancher:
			GlobalData.line[0] = 255
