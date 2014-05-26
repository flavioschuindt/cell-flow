import numpy as np
from math import ceil

class Grid:
	def __init__(self, width, height, cell_quantity):
		self.grid_shape = (cell_quantity, cell_quantity)
		self.cell_shape = (width/cell_quantity, height/cell_quantity)
		self.content = np.zeros(shape=self.grid_shape, dtype=list)

	def get_cell(self, torus):
		
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
		grid_coord = self.get_cell(torus)
		
		if self.content[grid_coord] == 0:
			self.content[grid_coord] = {torus.id: torus}
		else:
			if not self.content[grid_coord].has_key(torus.id):
				self.content[grid_coord][torus.id] = torus

	def remove(self, torus):
		grid_coord = self.get_cell(torus)
		if self.content[grid_coord] != 0 and self.content[grid_coord].has_key(torus.id):
			del self.content[grid_coord][torus.id]
			if not self.content[grid_coord]:
				self.content[grid_coord] = 0