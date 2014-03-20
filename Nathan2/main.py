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
import persistance

def main(): 
	pygame.init() 

	displayWidth = 640
	displayHeight = 640 


	screen = pygame.display.set_mode((displayWidth, displayHeight))
	grid = model.Grid(40, 40, model.EMPTY, 20, 20)
	bgGrid = model.Grid(40, 40, model.EMPTY, 20, 20)

	view.loadSprites()

	grid.entityList = model.initialEntities(grid)
	model.placeEntities(grid)

	persistance.load(grid, bgGrid) #Loads on startup of file.

	pygame.time.set_timer(pygame.USEREVENT, 1000)
	pendingActionList = entities.OrderedList()

#	controller.initializeActions(pendingActionList, grid.entityList)

#must be placed elsewhere 

	gatherer = grid.entityList[0]
	gatherer.aim = grid.entityList[2]
	for entity in grid.entityList: 
		if isinstance(entity, entities.MonsterEnergy): 
			gatherer.aim = entity 
			break 
	print (gatherer.aim)

	controller.initializeActions(pendingActionList, grid.entityList)

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
			if event.type == pygame.USEREVENT:
				controller.handleTicks(grid, pendingActionList, pygame.time.get_ticks())
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
				persistance.save(grid, bgGrid)
			if keys[K_l]:
				persistance.load(grid, bgGrid)
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
