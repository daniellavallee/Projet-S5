extends Area3D
var enterArea = false
var parent = get_parent()
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _on_body_entered(body: Node3D) -> void:
	while body.name == "Obstacle":
		print(body.global_position)
		print(parent.name)
		await get_tree().create_timer(1).timeout
		
