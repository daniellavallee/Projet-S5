extends Area3D

const erreurCapteur = 4.7025728225708
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
		GlobalData.distance = int((get_parent_node_3d().global_position.distance_to(body.global_position) - erreurCapteur) * 100)
		#print(distance)
		await get_tree().create_timer(0.5).timeout

func _on_body_exited(body: Node3D) -> void:
	enterArea = false
	GlobalData.distance = -1
