extends Area3D

var properties = [0,0,0,0,0]


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func _get_property_list() -> Array[Dictionary]:
	
	return properties
	

func _on_capteur_ligne_1_area_entered(area: Area3D) -> void:
	print("Capteur1") # Replace with function body.
	properties[0] = 255

func _on_capteur_ligne_2_area_entered(area: Area3D) -> void:
	print("Capteur2") # Replace with function body.
	properties[1] = 255

func _on_capteur_ligne_3_area_entered(area: Area3D) -> void:
	print("Capteur3") # Replace with function body.
	properties[2] = 255

func _on_capteur_ligne_4_area_entered(area: Area3D) -> void:
	print("Capteur4") # Replace with function body.
	properties[3] = 255

func _on_capteur_ligne_5_area_entered(area: Area3D) -> void:
	print("Capteur5") # Replace with function body.
	properties[4] = 255
	print(properties)


func _on_capteur_ligne_1_area_exited(area: Area3D) -> void:
	properties[0] = 0 # Replace with function body.
	print(properties)

func _on_capteur_ligne_2_area_exited(area: Area3D) -> void:
	properties[1] = 0 # Replace with function body.
	print(properties)

func _on_capteur_ligne_3_area_exited(area: Area3D) -> void:
	properties[2] = 0 # Replace with function body.
	print(properties)

func _on_capteur_ligne_4_area_exited(area: Area3D) -> void:
	properties[3] = 0 # Replace with function body.
	print(properties)

func _on_capteur_ligne_5_area_exited(area: Area3D) -> void:
	properties[4] = 0 # Replace with function body.
	print(properties)
	
	
