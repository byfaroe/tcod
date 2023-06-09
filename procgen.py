from __future__ import annotations

import random
from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod

import entity_factories
from game_map import GameMap
import tile_types


if TYPE_CHECKING:
	from entity import Engine


class RectangularRoom:
	def __init__(self, x: int, y: int, width: int, height: int):
		self.x1 = x
		self.y1 = y
		self.x2 = x + width
		self.y2 = y + height
		
	@property
	def center(self) -> Tuple[int, int]:
		center_x = int((self.x1 + self.x2) / 2)
		center_y = int((self.y1 + self.y2) / 2)
		
		return center_x, center_y
	
	@property
	def inner(self) -> Tuple[slice, slice]:
		"""Return the inner area of this room as a 2D array index."""
		return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)
		
	def intersects(self, other: RectangularRoom) -> bool:
		"""Return True if this room overlaps with another RectangularRoom."""
		return (
			self.x1 <= other.x2
			and self.x2 >= other.x1
			and self.y1 <= other.y2
			and self.y2 >= other.y1
		)

def place_random_entities(
		room: RectangularRoom,
		dungeon: GameMap,
		entity_types: List[Actor],  # TODO: Assumes entity_types only contains valid entities
		entity_weights: List[int],  # Relative probability of spawning each entity in entity_types
				# TODO: Assumes entity_weights length matches entity_types length
		maximum_entities: int,
		minimum_entities: int = 0,  # TODO: Fn *attempts* at least min entities, but if blocked won't retry to guarantee at least min actually placed
	) -> None:
	number_of_entities = random.randint(minimum_entities, maximum_entities)
	picks = random.choices(entity_types, weights=entity_weights, k=number_of_entities)
	print(picks)
	for next in picks:
		x = random.randint(room.x1 + 1, room.x2 - 1)
		y = random.randint(room.y1 + 1, room.y2 - 1)
		
		if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
			next.spawn(dungeon, x, y)



def tunnel_between(
	start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
	"""Return an L-shaped tunnel between these two points."""
	x1, y1 = start
	x2, y2 = end
	if random.random() < 0.5:  # 50% chance
		# Move horizontally, then vertically
		corner_x, corner_y = x2, y1
	else:
		# Move vertically, then horizontally
		corner_x, corner_y = x1, y2

	# Generate the coordinates for this tunnel
	for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
		yield x, y
	for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
		yield x, y


def generate_field(  # BYF
		map_width: int,
		map_height: int,
		min_entities: int,
		max_entities: int,
		engine: Engine,
	) -> GameMap:
	"""Generate an outdoor map, defaulting to fully explored open space, not walls.
	Create a RectangularRoom congruent with full map for convenience."""
	player = engine.player
	dungeon = GameMap(engine, map_width, map_height, entities=[player], outdoor=True)
	field = RectangularRoom(0, 0, map_width, map_height)
	
	player.place(*field.center, dungeon)
	
	place_random_entities(field, dungeon, entity_types=[entity_factories.bunny, entity_factories.gnome], entity_weights=[8, 2], maximum_entities=max_entities, minimum_entities=min_entities)  
			# TODO: Would rather be able to say entity_types = [orc, troll] and fn assumes they're from entity_factories
	return dungeon

def generate_dungeon(
		max_rooms: int,
		room_min_size: int,
		room_max_size: int,
		map_width: int,
		map_height: int,
		max_monsters_per_room: int,
		engine: Engine,
	) -> GameMap:
	"""Generate a new dungeon map."""
	player = engine.player
	dungeon = GameMap(engine, map_width, map_height, entities=[player])
	
	rooms: list[RectangularRoom] = []
	
	for r in range(max_rooms):
		room_width = random.randint(room_min_size, room_max_size)
		room_height = random.randint(room_min_size, room_max_size)
		
		x = random.randint(0, dungeon.width - room_width - 1)
		y = random.randint(0, dungeon.height - room_height - 1)
		
		new_room = RectangularRoom(x, y, room_width, room_height)
		
		# Run through the other rooms and see if they intersect with this one
		if any(new_room.intersects(other_room) for other_room in rooms):
			continue
			
		dungeon.tiles[new_room.inner] = tile_types.floor
		
		if len(rooms) == 0:
			# Start player in first room
			player.place(*new_room.center, dungeon)
		else:  # All rooms after the first
			# Dig out a tunnel between this room and previous
			for x, y in tunnel_between(rooms[-1].center, new_room.center):
				dungeon.tiles[x, y] = tile_types.floor
		
		place_random_entities(new_room, dungeon, [entity_factories.orc, entity_factories.troll], [8, 2], max_monsters_per_room)
		
		rooms.append(new_room)
	
	return dungeon