from math import ceil

import numpy as np


class Grid:
	def __init__(self, width, height, cell_quantity):
		self.grid_shape = (cell_quantity, cell_quantity)
		self.cell_shape = (width/cell_quantity, height/cell_quantity)
		self.content = np.zeros(shape=self.grid_shape, dtype=dict)

	def get_cell(self, torus):
		
		'''
			Given a torus, discover in which cell it is.
		'''
		
		x, y = torus.location.x, torus.location.y

		cell_offset_x, cell_offset_y = 0, 0

		cell_offset_x = int(ceil(abs(x) / self.cell_shape[0])) - 1
		cell_offset_y = int(ceil(abs(y) / self.cell_shape[1])) - 1

		x_middle = self.grid_shape[0] / 2
		y_middle = self.grid_shape[1] / 2

		grid_position_x = grid_position_y = 0

		if x < 0 and y < 0:
			grid_position_x = x_middle - cell_offset_x
			grid_position_y = y_middle + cell_offset_y
		elif x > 0 and y > 0:
			grid_position_x = x_middle + cell_offset_x
			grid_position_y = y_middle - cell_offset_y
		elif x < 0 and y > 0:
			grid_position_x = x_middle - cell_offset_x
			grid_position_y = y_middle - cell_offset_y
		elif x > 0 and y < 0:
			grid_position_x = x_middle + cell_offset_x
			grid_position_y = y_middle + cell_offset_y

		return (grid_position_y, grid_position_x)

	def insert(self, torus):
		'''
			Insert a torus in a cell.
		'''
		grid_coord = self.get_cell(torus)
		
		if self.content[grid_coord] == 0:
			self.content[grid_coord] = {torus.id: torus}
		else:
			if not self.content[grid_coord].has_key(torus.id):
				self.content[grid_coord][torus.id] = torus

	def remove(self, torus):
		'''
			Remove a torus from a cell.
		'''
		grid_coord = self.get_cell(torus)
		if self.content[grid_coord] != 0 and self.content[grid_coord].has_key(torus.id):
			del self.content[grid_coord][torus.id]
			if not self.content[grid_coord]:
				self.content[grid_coord] = 0

	def _get_elements_from_cell(self, cell):
		'''
			Get all torus inside a cell.
		'''
		return [] if self.content[cell] == 0 else self.content[cell].values()

	def get_neighbors(self, torus):
		'''
			Given a torus, returns a 8-neighborhood from the grid.
		'''
		height, width = self.grid_shape
		neighbors = []
		grid_coord_y, grid_coord_x = self.get_cell(torus)
		neighbors += self._get_elements_from_cell((grid_coord_y, grid_coord_x))

		# Immediate neighbors (left and right)
		if grid_coord_x-1 >= 0:
			neighbors += self._get_elements_from_cell((grid_coord_y, grid_coord_x-1)) # left

		if grid_coord_x+1 < width:
			neighbors += self._get_elements_from_cell((grid_coord_y, grid_coord_x+1)) # right

		# Up neighboors
		if grid_coord_y-1 >= 0:

			neighbors += self._get_elements_from_cell((grid_coord_y-1, grid_coord_x)) # Immediate up neighboor

			if grid_coord_x-1 >= 0: # up-left
				neighbors += self._get_elements_from_cell((grid_coord_y-1, grid_coord_x-1))

			if grid_coord_x+1 < width: # up-right
				neighbors += self._get_elements_from_cell((grid_coord_y-1, grid_coord_x+1))

		# Bottom neighboors
		if grid_coord_y+1 < height:

			neighbors += self._get_elements_from_cell((grid_coord_y+1, grid_coord_x)) # Immediate bottom neighboor

			if grid_coord_x-1 >= 0: # bottom-left
				neighbors += self._get_elements_from_cell((grid_coord_y+1, grid_coord_x-1))

			if grid_coord_x+1 < width-1: # bottom-right
				neighbors += self._get_elements_from_cell((grid_coord_y+1, grid_coord_x+1))

		return neighbors
