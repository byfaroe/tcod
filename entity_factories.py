from components.ai import HostileEnemy
from components.fighter import Fighter
from entity import Actor

player = Actor(
	char="@", 
	color=(255, 255, 255), 
	name="Player",
	ai_cls=HostileEnemy,
	fighter=Fighter(hp=30, defense=2, power=5)
)

orc = Actor(
	char="o", 
	color=(63, 127, 63), 
	name="Orc", 
	ai_cls=HostileEnemy,
	fighter=Fighter(hp=10, defense=0, power=3)
)
troll = Actor(
	char="T", 
	color=(0, 127, 0),
	name="Troll", 
	ai_cls=HostileEnemy,
	fighter=Fighter(hp=16, defense=1, power=4)
)


gnome = Actor(
	char="o", #"ô", 
	color=(255, 255, 255), 	# color=(27, 240, 200), 
	name="Gnome",
	ai_cls=HostileEnemy,
	fighter=Fighter(hp=10, defense=0, power=3)
)

bunny = Actor(
	char="v", 
	color=(255, 255, 255), 
	name="Bunny",
	ai_cls=HostileEnemy,
	fighter=Fighter(hp=6, defense=999999, power=0)
)