from __future__ import annotations

import copy
import random
from typing import Tuple, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
	from game_map import GameMap
	
T = TypeVar("T", bound="Entity")

class Entity:
	"""
	A generic object to represent players, enemies, items, etc.
	"""
	def __init__(
		self, 
		x: int = 0, 
		y: int = 0, 
		char: str = "?", 
		color: Tuple[int, int, int] = (255, 255, 255),
		name: str = "<Unnamed>",
		blocks_movement: bool = False,
	):
		self.x = x 
		self.y = y 
		self.char = char
		self.color = color
		self.name = name
		self.blocks_movement = blocks_movement
		
	def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
		"""Spawn a copy of this instance at the given location"""
		clone = copy.deepcopy(self)
		clone.x = x
		clone.y = y
		gamemap.entities.add(clone)
		return clone
		
	def move(self, dx: int, dy: int):
		self.x += dx
		self.y += dy
		
	# Added by BYF
	def seek(self, entity: Entity):
		dx, dy = 0, 0
		if entity.x < self.x:
			dx = -1
		if entity.x > self.x:
			dx = 1
		if entity.y < self.y:
			dy = -1
		if entity.y > self.y:
			dy = 1
		for i in range(random.randint(0, 2 if abs(entity.x-self.x) > 1 and abs(entity.y-self.y) > 1 else 1)): # If beside entity, move 0-1, else move 0-2
			self.move(dx, dy)
			