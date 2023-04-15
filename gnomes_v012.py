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

import tcod


def main():
	print("Hello World!")
	
if __name__ == "__main__":
	main()