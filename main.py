#main
'''
You are DA MAIN you must be clean 
and consise and beautiful (such beautiful)
'''
import math 
import random 
import sys, pygame 
from pygame.locals import* 
import copy
import os 
import controller
import view
import model 
import entities 

def main(): 
	pygame.init() 

	displayWidth = 640
	displayHeight = 640 


	screen = pygame.display.set_mode((displayWidth, displayHeight))
	grid = model.Grid(40, 40, model.EMPTY, 20, 20)
	bgGrid = model.Grid(40, 40, model.EMPTY, 20, 20)

	view.loadSprites()

	grid.entityList = model.initialEntities(grid)
	'''
	tl = entities.Point(0, 0)
	tr = entities.Point(0, 19)
	bl = entities.Point(19, 0)
	br = entities.Point(19, 19)
	topLeft = entities.MonsterEnergy('me', tl)
	topRight = entities.MonsterEnergy('me', tr)
	bottomLeft = entities.MonsterEnergy('me', bl)
	bottomRight = entities.MonsterEnergy('me', br)
	grid.entityList = [topLeft, topRight, bottomLeft, bottomRight]
	'''
	model.placeEntities(grid)

#must be placed elsewhere 

	gatherer = grid.entityList[0]
	gatherer.aim = grid.entityList[2]
	for entity in grid.entityList: 
		if isinstance(entity, entities.MonsterEnergy): 
			gatherer.aim = entity 
			break 
	print (gatherer.aim)

	resetCopy = controller.returnCopiesOf(grid.entityList)

	while 1: 
		for event in pygame.event.get(): 
			keys = pygame.key.get_pressed()
			mouse = pygame.mouse.get_pressed()
			x, y = pygame.mouse.get_pos()
			p = controller.clickToPoint(grid, x, y)

			if event.type == QUIT: 
				pygame.quit()
				sys.exit()
			if mouse[0]: 
				controller.handleLeftClicks(grid, keys, p, bgGrid)
			if mouse[2]:
				controller.handleRightClicks(grid, p)

			if keys[K_0]: 
				grid.keyPressed = 0
				print("Key pressed 0")
				grid = model.resetGrid(resetCopy, bgGrid)
				grid.entityList = controller.returnCopiesOf(resetCopy)
				gatherer = grid.entityList[0]
				grid.spacePressed = False
			if keys[K_s]:
				controller.save(grid, bgGrid)
			if keys[K_l]:
				controller.load(grid, bgGrid)
			controller.handleHover(grid, x, y)
			
			controller.handleKeys(grid, keys, gatherer)

		#controller.takeAction(grid, grid.spacePressed, grid.keyPressed, gatherer)
		if grid.spacePressed: 
			controller.updateGatherers(grid)
		view.draw(screen, grid, bgGrid, grid.screenW, grid.screenH)

		#view.handleSprites(screen, entityList)

		controller.cleanUp(grid.entityList)
		pygame.display.flip()

		model.placeEntities(grid)


if __name__ == '__main__':
	main()
