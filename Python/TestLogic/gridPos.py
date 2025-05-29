def XYfromGrid(gridnum, grid_size=5):
	x = gridnum%grid_size
	y = gridnum//grid_size
	return x, y