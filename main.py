#! /usr/bin/env python3

# v012 - START OVER ========= SWITCH TO TCOD not curses =================
# v011 - Add list of direct refs to all objs on map (quicker to update all in list rather than iterate over all contents of all tiles).
# v010 - Add flowers! TODO: If wall and flower in same tile, should show wall (usu layer 2) not flower (usu layer 6) 
# v009 - Skeleton for improvememnt to Thing.move(). Add Thing.step() to attempt single-tile orthogonal move and update map with results,
#   changed Thing.move() to handle multi-step moves. Add sign(x) to check for +ve/-ve. Fix map drawing issue that leaves edges blank.
# v008 - Cut 250+ lines of unnec comments. Fix color. Fold up verion notes apparently.
# v007 - Add gnome! For now just standalone Thing that random-walks and occasionally builds an ad hoc gnome house (also Thing)
# v006 - Improve push/pop/peek/remove incl adding wrappers in Tile and Map and fixing attempts to draw empty Tiles. 
#   Added simple 'build' (b in game loop places Wall). Added 'facing' dictionary and player.face, incl track where player's facing on move.
# v005 - omg did everything. Improve map/tile structure and methods. Add Things. Add queues so can stack stuff on tiles. Etc.
#   WOO AND IT WORKS! Got map, can move, can't move through walls. Didn't draw walls as expected, and doesn't draw objs until first move.
# v004 - Add annoying debug messages.
# v003 - Add game loop. Add player. Can move. Successful edge detection.
#   Can't clear map without getting pure black screen.
# v002 - curses not pygame. Draws a map!
# v001 - pygame. Random obstacles that block movt. Player (green square)

#   can move. Baddies (red squares) random-walk way too fast.
import copy

import tcod

from engine import Engine
import entity_factories
from input_handlers import EventHandler
from procgen import generate_dungeon

def main():
	screen_width = 80
	screen_height = 50	
	
	map_width = 80
	map_height = 45
	
	room_max_size = 10
	room_min_size = 6
	max_rooms = 30
	
	max_monsters_per_room = 2
	
	tileset = tcod.tileset.load_tilesheet(
		"dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
	)
	
	event_handler = EventHandler()
	
	player = copy.deepcopy(entity_factories.player)
	
#	Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
	
	game_map = generate_dungeon(
		max_rooms=max_rooms,
		room_min_size=room_min_size,
		room_max_size=room_max_size,
		map_width=map_width,
		map_height=map_height,
		max_monsters_per_room=max_monsters_per_room,
		player=player
	)
	
	engine = Engine(event_handler=event_handler, game_map=game_map, player=player)
	
	with tcod.context.new_terminal(
		screen_width,
		screen_height,
		tileset=tileset,
		title="Gnomes!",
		vsync=True,
	) as context:
		root_console = tcod.Console(screen_width, screen_height, order="F")

		while True:
				engine.render(console=root_console, context=context)
				
				events = tcod.event.wait()
				
				engine.handle_events(events)			


if __name__ == "__main__":
	main()