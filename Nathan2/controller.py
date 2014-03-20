import entities 
import model 
import view 
import copy 
import math
import pygame 
from pygame.locals import*

#events and draw, response to input, 
'''
takes input and reports directly to model and view. 
DOES NOT CHANGE ANYTHING. 
Responds to input by telling the other two to do stuff

THIS SHOULD HANDLE TICKS (i think) or DIRECTLY USING TICKS 
'''
'''-------------------------------------------------------------------------'''
'''Keyboard and Mouseclicks'''
def handleKeys(grid, keys, gatherer): 
	'''----------Entity Movement-----------'''
	if keys[K_1]: 
		grid.keyPressed = 1
		print ("Key pressed 1")
		gathList = listOfGatherers(grid.entityList)
		for gatherer in gathList: 
			gatherer.aim = determineNearest(grid.entityList, gatherer)
		grid.spacePressed = False
		print (gatherer.aim)

	elif keys[K_2]: 
		grid.keyPressed = 2
		print("Key pressed 2") 
		gathList = listOfGatherers(grid.entityList)
		for gatherer in gathList: 
			gatherer.aim = determineFarthest(grid.entityList, gatherer)
		grid.spacePressed = False
		print (gatherer.aim)

	if keys[K_SPACE]: 
		print ("Key pressed Space") 
		grid.spacePressed = True

	'''----------Viewport-----------'''
	if keys[K_RIGHT]: 
		if (grid.origin.x < grid.width - grid.screenW): 
			grid.origin.x += 1
		else: print("Can't move anymore")

	elif keys[K_LEFT]: 
		if (grid.origin.x > 0): 
			grid.origin.x -= 1
		else:print ("Can't move anymore")

	elif keys[K_DOWN]: 
		if (grid.origin.y < grid.height - grid.screenH): 
			grid.origin.y += 1
		else: print("Can't move anymore")

	elif keys[K_UP]: 
		if (grid.origin.y > 0): 
			grid.origin.y -= 1
		else: print("Can't move anymore")

	if keys[K_LSHIFT]: 
		if keys[K_RIGHT]: 
			pass

	'''----------Place Entity Mode-----------'''
	if keys[K_q]: 
		grid.placeMode = model.GATHERER
	if keys[K_w]: 
		grid.placeMode = model.GENERATOR
	if keys[K_e]: 
		grid.placeMode = model.RESOURCE
	if keys[K_r]: 
		grid.placeMode = model.OBSTACLE
	if keys[K_t]: 
		grid.placeMode = model.CONCRETE
	if keys[K_y]: 
		grid.placeMode = model.EMPTY


def handleLeftClicks(grid, keys, p, bgGrid):
	if grid.placeMode == model.GATHERER: 
		newGath = entities.CSCStudent(5, p)
		grid.entityList.append(newGath)
	elif grid.placeMode == model.GENERATOR: 
		newGen = entities.CampusMarket(4, p)
		grid.entityList.append(newGen)
	elif grid.placeMode == model.RESOURCE: 
		newRes = entities.MonsterEnergy(p)
		grid.entityList.append(newRes)
	elif grid.placeMode == model.OBSTACLE: 
		newObs = entities.Obstacle(p)
		grid.entityList.append(newObs)
	#The following two only affect the bgGrid
	elif grid.placeMode == model.EMPTY: 
		model.set_cell(bgGrid, p, model.EMPTY)
	elif grid.placeMode == model.CONCRETE: 
		model.set_cell(bgGrid, p, model.CONCRETE)

	else: 
		newRes = resourceClick(grid, p, grid.entityList)
		grid.entityList += newRes

def handleRightClicks(grid, point):
	if not model.get_cell(grid, point) == 0: 
		model.set_cell(grid, point, 0)
		for entity in grid.entityList: 
			if samePt(entity.position, point):
				grid.entityList.remove(entity)

def resourceClick(grid, point, entityL): 
	if model.get_cell(grid, point) == 3: 
		print ("Clicked Resource at ", point.x, point.y) 
		return model.spawnResources(grid, point, entityL, 2, 1)
	else: 
		print ("Did not click resource") 
		return []

def clickToPoint(grid, x, y): #need to write to take in origin point 
	#converts position of clicks to a point on the grid

	x = math.trunc(x / view.CELL_SIZE) + grid.origin.x
	y = math.trunc(y/ view.CELL_SIZE) + grid.origin.y
	return entities.Point(x, y)

def samePt(p1, p2): 
	return p1.x == p2.x and p1.y == p2.y

def handleHover(grid, x, y): 
	x = math.trunc(x / view.CELL_SIZE)
	y = math.trunc(y / view.CELL_SIZE)
	p = entities.Point(x, y)
	grid.mouseHover = p


'''-------------------------------------------------------------------------'''
'''Entity Movement'''

def takeAction(grid, space, key, gatherer): 
	if space: 
		if key == 1 or key == 2:
			determineNewGathererPosition(grid, gatherer, gatherer.aim)

def determineNearest(entlist, gatherer): 
#returns position of nearest resource
	dist = []
	nearest = 0
	resList = listOfResources(entlist)
	for resource in resList:
		dist.append(distance(resource.position, gatherer.position))

	for i in range(len(dist)):
		if dist[i] < dist[nearest]:
			nearest = i
	return (resList[nearest])
	
def determineFarthest(entlist, gatherer):   
#returns position of farthest resource
	dist = []
	farthest = 0
	resList = listOfResources(entlist)
	for resource in resList:
			dist.append(distance(resource.position, gatherer.position))

	for i in range(len(dist)):
		if dist[i] > dist[farthest]:
			farthest = i
	return (resList[farthest])

def distance(p1, p2): 
	dist = math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
	return dist

def determineNewGathererPosition(grid, gatherer, resource):
	#Determines position one grixel toward the CLOSEST resource in both the x and y axis
	#Eventually, will determine the closest resource of a list of resources
	oldx = gatherer.position.x 
	oldy = gatherer.position.y
	oldpoint = entities.Point(oldx, oldy) 

	if resource.position.x > gatherer.position.x:    
		gatherer.position.x += 1
	elif resource.position.x < gatherer.position.x: 
		gatherer.position.x -= 1
	if model.get_cell(grid, gatherer.position) == 4: 
		gatherer.position.x = oldx
		
	#Handling Y 
	if resource.position.y > gatherer.position.y: 
		gatherer.position.y += 1
	elif resource.position.y < gatherer.position.y: 
		gatherer.position.y -= 1
	if model.get_cell(grid, gatherer.position) == 4: 
		gatherer.position.y = oldy

	if not samePt(gatherer.position, oldpoint): 
		model.set_cell(grid, oldpoint, 5)

def updateGatherers(grid): 
	resList = listOfResources(grid.entityList)
	gathList = listOfGatherers(grid.entityList) 

	for gatherer in gathList: 
		if gatherer.aim: 
			determineNewGathererPosition(grid, gatherer, gatherer.aim)
		else: 
			if gatherer.direction == entities.NEAR: 
				gatherer.aim = determineNearest(resList, gatherer)
			if gatherer.direction == entities.FAR: 
				gatherer.aim = determineFarthest(resList, gatherer) 


'''-------------------------------------------------------------------------'''
'''List Handling'''
def returnCopiesOf(stuffList): 
	#will return a copy of the current list DEEPCOPY
	newList = []
	for obj in stuffList: 
		newList.append(copy.deepcopy(obj))
	return newList

def listOfGatherers(entlist): 
	newList = []
	for ent in entlist: 
		if isinstance(ent, entities.CSCStudent): 
			newList.append(ent)
	return newList

def listOfGenerators(entlist): 
	newList = []
	for ent in entlist: 
		if isinstance(ent, entities.CampusMarket): 
			newList.append(ent)
	return newList

def listOfResources(entlist): 
	newList = []
	for ent in entlist: 
		if isinstance(ent, entities.MonsterEnergy): 
			newList.append(ent)
	return newList

def cleanUp(entlist): 
	for a in entlist: 
		if isinstance(a, entities.CSCStudent): 
			for b in entlist: 
				if (not a == b and isinstance(b, entities.MonsterEnergy) 
					and samePt(a.position, b.position)): 
					entlist.remove(b)

def initializeActions(actionList, entityList): 
	for entity in entityList: 
		if isinstance(entity, entities.CSCStudent): 
			actionList.insert(entity, entity.rate)

def handleTicks(grid, actionList, ticks):
	while not actionList.empty() and actionList.head().ord < ticks:
		
		action = actionList.pop()

		if isinstance(action.item, entities.CSCStudent):
			print("Handled a CSC tick")
			determineNewGathererPosition(grid, action.item, action.item.aim)
			rescheduleItem(actionList, ticks, action.item)

def rescheduleItem(actionList, ticks, item): 
	actionList.insert(item, ticks + item.rate)
