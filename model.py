import entities 
import random 

#manages grid and entities on the world. 
'''
Anything that relate to placing things in the world. 
Anything that touches and modifies the grid. 
'''
'''
placeEntities

'''

'''-------------------------------------------------------------------------'''
'''Grid Handling'''
# define occupancy value
EMPTY = 0
GATHERER = 1
GENERATOR = 2
RESOURCE = 3
OBSTACLE = 4
TRAIL = 5
CONCRETE = 6
TRANSFORM = 7

class Grid:
	def __init__(self, width, height, occupancy_value, screenW, screenH):
		self.width = width
		self.height = height
		self.cells = []
		self.screenW = screenW
		self.screenH = screenH
		self.origin = entities.Point(0,0)
		self.entityList = []	#so this should really be a dictionary. 
		self.keyPressed = 0
		self.spacePressed = False
		self.placeMode = 0
		self.mouseHover = None
	
		# initialize grid to all specified occupancy value
		for row in range(0, self.height):
			self.cells.append([])
			for col in range(0, self.width):
				self.cells[row].append(occupancy_value)

def set_cell(grid, point, value):
	grid.cells[point.y][point.x] = value

def get_cell(grid, point):
	return grid.cells[point.y][point.x]

def resetGrid(entityList, bgGrid): #rewrite ??
	grid1 = Grid(40, 40, EMPTY, 20, 20)
	grid1.entityList = entityList
	placeEntities(grid1)
	emptyGrid(bgGrid)
	return grid1

def emptyGrid(grid): 
	for x in range(0, grid.width): 
		for y in range(0, grid.height): 
			p = entities.Point(x, y)
			set_cell(grid, p, 0)

def isValidPosition(grid, p):
	#If the point is within the height and width of the grid, returns True
	if (0 < p.x < grid.width) and (0 < p.y < grid.height):
		return True 
	else: 
		return False


'''-------------------------------------------------------------------------'''
'''Entity Handling'''

def initialEntities(grid): 
	#create points for the initial gatherer and generator 
	p1 = entities.Point(random.randrange(0, grid.width), 
		random.randrange(0, grid.height))   
	p2 = entities.Point(random.randrange(5, grid.width - 5), 
		random.randrange(5, grid.height - 5)) 

	gatherer = entities.CSCStudent(5, p1)  
	generator = entities.CampusMarket(.5, p2) 
	resourceList = spawnResources(grid, generator.position, [], 3, 3) 
	entList = [gatherer, generator]
	for ent in resourceList: 
		entList.append(ent)
	return entList

def placeEntities(grid): 
	#Sets cells to value of gatherers
	emptyGrid(grid)
	for ent in grid.entityList: 
		if isinstance(ent, entities.CSCStudent): 
			set_cell(grid, ent.position, GATHERER)
		elif isinstance(ent, entities.CampusMarket): 
			set_cell(grid, ent.position, GENERATOR)
		elif isinstance(ent, entities.MonsterEnergy): 
			set_cell(grid, ent.position, RESOURCE)
		elif isinstance(ent, entities.Obstacle): 
			set_cell(grid, ent.position, OBSTACLE)
		elif isinstance(ent, entities.transformingMonster): 
			set_cell(grid, ent.position, TRANSFORM)
	

def spawnResources(grid, centerPoint, resourceL, numRes, cellRange): 
	#creates new resources in empty cells nearby 
	spawnedResources = [] 
	occupiedList = [centerPoint] #list of currently filled positions
	for resource in resourceL: 
		occupiedList.append(resource.position)
		#is there a reason that I don't just put in the resource.position?
	for x in range(0, numRes):
		resPoint = centerPoint
		loopAgain = True  

		#will loop until 2 valid and empty position are found
		while loopAgain or (not isValidPosition(grid, resPoint)): 
			
			cellList = getSurrounding(centerPoint, cellRange, grid)

			#check how many empty surrounding cells 
			numEmpty = 0
			for cell in cellList: 
				if cell == 0: 
					numEmpty += 1

			#if there are less than 2 empty surrounding cells, stop
			if numEmpty < 2: 
				print ("No space for Resources") 
				return []

			#Reset loopAgain and isOccupied. 
			#This way if not occupied but not valid, will reset
			loopAgain = True  
			isOccupied = False
			resPoint = entities.Point(occupiedList[0].x + 
				random.randrange(-cellRange, cellRange + 1), 
				occupiedList[0].y + random.randrange(-cellRange, cellRange + 1))
			for pos in occupiedList: 
				if (resPoint.x == pos.x) and (resPoint.y == pos.y):
					isOccupied = True
			if not isOccupied: 
			 loopAgain = False

		occupiedList.append(resPoint)
		spawnedResources.append(entities.MonsterEnergy(resPoint))       
	return spawnedResources

def getSurrounding(centerPoint, cellRange, grid): 
	#returns a list of the values of surrounding cells 
	#find the coordinates of the surrounding cells within range
	minx = centerPoint.x - cellRange
	maxx = centerPoint.x + cellRange
	miny = centerPoint.y - cellRange
	maxy = centerPoint.y + cellRange

	#get the values of surrounding cells 
	getCells = []
	for x in range(minx, maxx + 1): 
		for y in range(miny, maxy + 1): 
			getCells.append(get_cell(grid, entities.Point(x, y)))

	return getCells