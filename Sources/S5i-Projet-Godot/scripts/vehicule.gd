extends CharacterBody3D

@export var speed_multiplier = 0.1
@export var angle_multiplier = 0.3

@export var USE_WEBSOCKET = true

@onready var roueAvantDroit = $"AvantDroit"
@onready var roueAvantGauche = $"AvantGauche"

func _ready() -> void:
	pass # Replace with function body.

func physic(controle_angle:float,controle_moteur:float):
	var angle_roues = controle_angle * angle_multiplier
	var up = Vector3(0,1,0)
	if controle_moteur < 0:
		up *= -1
	var forward = Vector3(0,0,1)
	var new_forward = Vector3(sin(angle_roues),0,cos(angle_roues)) * forward
	print(new_forward)
	var vel = new_forward * controle_moteur * speed_multiplier
	var magn = vel.length()
	translate(vel)
	rotate(up,angle_roues*magn)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float):
	if Input.is_action_pressed("reset"):
		get_parent().get_tree().reload_current_scene()
	var controle_angle = 0
	var controle_moteur = 0
	if USE_WEBSOCKET :
		controle_angle = 1.5 * -(GlobalData.wheel_angle - 90)/45
		controle_moteur = 0.5 * GlobalData.bw_speed / 100
	else :
		controle_angle = Input.get_axis("right","left")
		controle_moteur = Input.get_axis("down", "up")
	physic(controle_angle,controle_moteur)
