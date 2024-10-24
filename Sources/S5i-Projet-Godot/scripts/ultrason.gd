extends Area3D
var enterArea = false

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _on_body_entered(body: Node3D) -> void:
	enterArea = true
	while body.name == "Obstacle" and enterArea:
		var distance = int(global_position.distance_to(body.global_position) * 100)
		print(distance)
		await get_tree().create_timer(0.5).timeout

func _on_body_exited(body: Node3D) -> void:
	enterArea = false
