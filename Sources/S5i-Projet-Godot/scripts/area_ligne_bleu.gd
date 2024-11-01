extends Area3D

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _get_property_list() -> Array[Dictionary]:
	return GlobalData.suiveur_ligne
	

func _on_capteur_ligne_1_area_entered(area: Area3D) -> void:
	#print("Capteur1") # Replace with function body.
	GlobalData.suiveur_ligne[4] = 0


func _on_capteur_ligne_2_area_entered(area: Area3D) -> void:
	#print("Capteur2") # Replace with function body.
	GlobalData.suiveur_ligne[3] = 0


func _on_capteur_ligne_3_area_entered(area: Area3D) -> void:
	#print("Capteur3") # Replace with function body.
	GlobalData.suiveur_ligne[2] = 0


func _on_capteur_ligne_4_area_entered(area: Area3D) -> void:
	#print("Capteur4") # Replace with function body.
	GlobalData.suiveur_ligne[1] = 0


func _on_capteur_ligne_5_area_entered(area: Area3D) -> void:
	#print("Capteur5") # Replace with function body.
	GlobalData.suiveur_ligne[0] = 0
	#print(properties)


func _on_capteur_ligne_1_area_exited(area: Area3D) -> void:
	GlobalData.suiveur_ligne[4] = 255 # Replace with function body.
	#print(properties)


func _on_capteur_ligne_2_area_exited(area: Area3D) -> void:
	GlobalData.suiveur_ligne[3] = 255 # Replace with function body.
	#print(properties)


func _on_capteur_ligne_3_area_exited(area: Area3D) -> void:
	GlobalData.suiveur_ligne[2] = 255 # Replace with function body.
	#print(properties)


func _on_capteur_ligne_4_area_exited(area: Area3D) -> void:
	GlobalData.suiveur_ligne[1] = 255 # Replace with function body.
	#print(properties)


func _on_capteur_ligne_5_area_exited(area: Area3D) -> void:
	GlobalData.suiveur_ligne[0] = 255 # Replace with function body.
	#print(properties)
	
	
