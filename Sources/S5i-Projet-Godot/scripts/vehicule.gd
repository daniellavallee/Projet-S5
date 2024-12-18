extends CharacterBody3D

var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")
@export var USE_WEBSOCKET = true
@onready var roueAvantDroit = $"AvantDroit"
@onready var roueAvantGauche = $"AvantGauche"
var L = 0.14 * 10
var angle_multiplier = 45
var speed_multiplier = 2.68
var multiplier = speed_multiplier
var multiplerX = 0.7 * multiplier
var multiplerY = 0.7 * multiplier

func _ready() -> void:
	pass # Replace with function body.

func physic(controle_angle:float,controle_moteur:float, delta:float):
	var up = Vector3(0,1,0)
	if controle_moteur < 0:
		up *= -1
	var angle_roues = deg_to_rad(controle_angle * 45)
	var radius = 0
	if angle_roues != 0:
		radius = L / tan(angle_roues)
	var magn = controle_moteur * speed_multiplier * delta
	var theta = angle_roues*angle_multiplier * delta * magn
	var vel = Vector3(0,0,1)
	if controle_angle == 0:
		vel = vel * magn
	else:
		var deltaX = radius - radius * cos(theta)
		var deltaY = radius * sin(theta)
		vel = Vector3(multiplerX*deltaX,0,multiplerY*deltaY)
	translate(vel)
	rotate(up,theta)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float):
	if Input.is_action_pressed("reset"):
		get_parent().get_tree().reload_current_scene()
	var controle_angle = 0
	var controle_moteur = 0
	if USE_WEBSOCKET :
		controle_angle = -(GlobalData.wheel_angle - 90)/45
		controle_moteur = GlobalData.bw_speed / 100
	else :
		controle_angle = Input.get_axis("right","left")
		controle_moteur = Input.get_axis("down", "up")
	physic(controle_angle,controle_moteur,delta)
