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
			setDirYandX(gatherer, gatherer.aim)
		grid.spacePressed = False

	elif keys[K_2]: 
		grid.keyPressed = 2
		print("Key pressed 2") 
		gathList = listOfGatherers(grid.entityList)
		for gatherer in gathList: 
			gatherer.aim = determineFarthest(grid.entityList, gatherer)
			setDirYandX(gatherer, gatherer.aim)
		grid.spacePressed = False

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


def handleLeftClicks(actionList, grid, keys, p, bgGrid):
	if keys[K_LSHIFT]: 
		#new function below, pass grid, p, actionlist) 
		e = findEntity(grid.entityList, p)
		if not e: 
			return 

		if isinstance(grid.entityList[e], entities.MonsterEnergy): 
			grid.entityList.pop(e)
			t = entities.transformingMonster(p)
			grid.entityList.append(t)
			actionList.insert(t, 0)

	elif grid.placeMode == model.GATHERER: 
		removePrevInCell(grid, p)
		newGath = entities.CSCStudent(5, p)
		grid.entityList.append(newGath)
	elif grid.placeMode == model.GENERATOR: 
		removePrevInCell(grid, p)
		newGen = entities.CampusMarket(4, p)
		grid.entityList.append(newGen)
	elif grid.placeMode == model.RESOURCE: 
		removePrevInCell(grid, p)
		newRes = entities.MonsterEnergy(p)
		grid.entityList.append(newRes)
	elif grid.placeMode == model.OBSTACLE: 
		removePrevInCell(grid, p)
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

	print (grid.entityList)

def removePrevInCell(grid, p):
	if not model.get_cell(grid, p) == 0: 
		a = findEntity(grid.entityList, p)
		grid.entityList.pop(a)

def setDirYandX(gat, res): 
	if gat.position.y < res.position.y: 
		gat.diry = 1 
	else: 
		gat.diry = -1

	if gat.position.x < res.position.x: 
		gat.dirx = 1
	else: 
		gat.dirx = -1

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

def determineNewGathererPosition(grid, gat, res):
	#Determines position one grixel toward the CLOSEST resource in both the x and y axis
	#Eventually, will determine the closest resource of a list of resources


	newGathP = entities.Point(gat.position.x, gat.position.y)
	diry = gat.diry
	dirx = gat.dirx

	if not isinstance(res, entities.MonsterEnergy): 
		return
	

	if not (gat.position.x == res.position.x) and not gat.priY: 
		direction = res.position.x - gat.position.x
		unitDir = int(direction / abs(direction)) #will be either +1 or -1
		newGathP.x += unitDir
		cellVal = model.get_cell(grid, newGathP)
		if not canMove(cellVal):
			newGathP.x -= unitDir
			newGathP.y += diry
			cellVal = model.get_cell(grid, newGathP) 
			if not canMove(cellVal): 
				newGathP.y -= 2 * diry
				cellVal = model.get_cell(grid, newGathP) 
				if not canMove(cellVal): 
					newGathP.y -= diry
					newGathP.x -= unitDir
					gat.priY = True

	elif not gat.position.y == res.position.y or gat.priY: 
		direction = res.position.y - gat.position.y
		if direction == 0: direction = 1
		unitDir = int(direction / abs(direction) )
		newGathP.y += unitDir
		gat.priY = False
		cellVal = model.get_cell(grid, newGathP)
		if not canMove(cellVal): 
			newGathP.y -= unitDir 
			newGathP.x += dirx
			gat.priY = True
			cellVal = model.get_cell(grid, newGathP)
			if not canMove(cellVal): 
				newGathP.x -= 2 * dirx
				cellVal = model.get_cell(grid, newGathP)
				if not canMove(cellVal): 
					newGathP.x -= dirx
					newGathP.y -= unitDir
					gat.priY = False

	gat.position = newGathP

def canMove(cellVal): 
	return (cellVal == model.EMPTY or cellVal == model.RESOURCE)

def updateGatherers(grid): 
	resList = listOfResources(grid.entityList)
	gathList = listOfGatherers(grid.entityList) 

	for gatherer in gathList:
		if gatherer.move == True: 
			if isinstance(gatherer.aim, entities.MonsterEnergy): 
				pass
				if not (model.get_cell(grid, gatherer.aim.position) == model.RESOURCE): 
					gatherer.aim = None
			else: 
				if len(resList) < 1: 
					gatherer.aim = None
				elif gatherer.direction == entities.NEAR: 
					gatherer.aim = determineNearest(resList, gatherer)
				elif gatherer.direction == entities.FAR: 
					gatherer.aim = determineFarthest(resList, gatherer) 
			
			if not gatherer.aim == None: 
				setDirYandX(gatherer, gatherer.aim)

def ensureMovement(grid, actionList): 
	for ent in grid.entityList:
		if isinstance(ent, entities.CSCStudent): 
			if ent.registered == False: 
				actionList.insert(ent, ent.rate)
				ent.registered = True
		if isinstance(ent, entities.CampusMarket): 
			if ent.registered == False: 
				actionList.insert(ent, ent.rate)
				ent.registered = True




'''-------------------------------------------------------------------------'''
'''Animation'''
def transform(grid, point): 
	'''register an action for transforming
	t = entities.transformingMonster(point)
	grid.entitiesList.append(t)
	action_list.insert(t, 0) #will be immediate 
	''' 
	for entity in grid.entityList: 
		if samePt(entity.position, point): 
			grid.entityList.pop(entity)

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
					a.aim = None
					a.move = False

def findEntity(entlist, p): #returns a position 
	for a in entlist: 
		if samePt(a.position, p): 
			return entlist.index(a)
	return None

'''-------------------------------------------------------------------------'''
'''Tick Handling'''
def initializeActions(actionList, entityList): 
	for entity in entityList: 
		if isinstance(entity, entities.CSCStudent): 
			actionList.insert(entity, entity.rate)
			entity.registered = True
		elif isinstance(entity, entities.CampusMarket): 
			actionList.insert(entity, entity.rate)
			entity.registered = True

def handleTicks(grid, actionList, ticks): 
	#the whole action thing
	while not actionList.empty() and actionList.head().ord < ticks:
		action = actionList.pop()

		if isinstance(action.item, entities.CSCStudent): 
			if action.item.move: 
				determineNewGathererPosition(grid, action.item, action.item.aim)
				rescheduleItem(actionList, ticks, action.item, action.item.rate)
			else: 
				gatherAnimation(actionList, action.item, ticks)

		if isinstance(action.item, entities.transformingMonster):
			if action.item.times == 0: 
				action.item.times += 1
				rescheduleItem(actionList, ticks, action.item, action.item.rate)
			elif action.item.times == 1: 
				action.item.times += 1
				rescheduleItem(actionList, ticks, action.item, action.item.rate)
			elif action.item.times >= 2: 
				r = entities.Obstacle(action.item.position)
				grid.entityList.append(r)
				i = grid.entityList.index(action.item)
				grid.entityList.pop(i)

		if isinstance(action.item, entities.CampusMarket): 
			if action.item.times < 3: 
				action.item.times += 1
			else: 
				action.item.times = 0 
			rescheduleItem(actionList, ticks, action.item, action.item.rate)


def rescheduleItem(actionList, ticks, item, rate): 
	actionList.insert(item, ticks + rate)

def gatherAnimation(actionList, gat, ticks): 
	if gat.animationTimes < 20: 
		if gat.animationLoop == 0: 
			gat.animationLoop = 1
			rescheduleItem(actionList, ticks, gat, 10)
		else: 
			gat.animationLoop = 0
			gat.animationTimes += 1
			rescheduleItem(actionList, ticks, gat, 10)
	else: 
		gat.animationTimes = 0
		gat.move = True
		rescheduleItem(actionList, ticks, gat, gat.rate)
		