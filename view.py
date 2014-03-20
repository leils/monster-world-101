import pygame 
import os 
import entities
import model
import controller
#manages drawing to screen 

'''
Draws the world. 
Allows you to move the viewpoint (scan through the world) 
DOES NO ACTUAL MODIFICATION TO THE WORLD, ONLY DRAWS 
'''
# define cell size
CELL_SIZE = 32
WHITE = (255, 255, 255)

def imgLoad(images): 
	images.resSprite = pygame.image.load(os.path.join("Monster.bmp")).convert()
	images.gathSprite = pygame.image.load(os.path.join("CSCStudent.bmp")).convert()
	images.Background = pygame.image.load(os.path.join("Background.bmp")).convert()
	images.Concrete = pygame.image.load(os.path.join("Concrete.bmp")).convert()
	images.Rock = pygame.image.load(os.path.join("Rocks.bmp")).convert()
	images.Trail = pygame.image.load(os.path.join("Trail.bmp")).convert()
	images.greenBox = pygame.image.load(os.path.join("greenBox.bmp")).convert()
	images.redBox = pygame.image.load(os.path.join("redBox.bmp")).convert()
	images.T1 = pygame.image.load(os.path.join("T1.bmp")).convert()
	images.T2 = pygame.image.load(os.path.join("T2.bmp")).convert()
	images.C1 = pygame.image.load(os.path.join("consumeA1.bmp")).convert()
	images.C2 = pygame.image.load(os.path.join("consumeA2.bmp")).convert()
	images.M1 = pygame.image.load(os.path.join("Market.bmp")).convert()
	images.M2 = pygame.image.load(os.path.join("Market2.bmp")).convert()
	images.M3 = pygame.image.load(os.path.join("Market3.bmp")).convert()
	images.resSprite.set_colorkey(WHITE)
	images.gathSprite.set_colorkey(WHITE)
	images.Background.set_colorkey(WHITE)
	images.Concrete.set_colorkey(WHITE)
	images.Rock.set_colorkey(WHITE)
	images.Trail.set_colorkey(WHITE)
	images.greenBox.set_colorkey(WHITE)
	images.redBox.set_colorkey(WHITE)
	images.T1.set_colorkey(WHITE)
	images.T2.set_colorkey(WHITE)
	images.C1.set_colorkey(WHITE)
	images.C2.set_colorkey(WHITE)
	images.M1.set_colorkey(WHITE)
	images.M2.set_colorkey(WHITE)
	images.M3.set_colorkey(WHITE)
	images.transformList += [images.T1, images.T2]
	images.consumeList += [images.C1, images.C2]
	images.marketList += [images.M1, images.M2, images.M3, images.M2]

# draw the 2D grid
# can edit to take in a list and determine the image that should be placed 
def draw(img, screen, grid, bgGrid, screenW, screenH): #originPoint, viewH viewW (IN GRIDS)
	origin = grid.origin
	for y in range(0, screenH):
		for x in range(0, screenW):
			p = entities.Point(x + origin.x, y + origin.y)
			value = model.get_cell(grid, p)
			bgValue = model.get_cell(bgGrid, p)
			#Background handling - concrete and grass

			screen.blit(img.Background, (x * CELL_SIZE, y * CELL_SIZE))

			if bgValue == model.CONCRETE: 
				screen.blit(img.Concrete, (x * CELL_SIZE, y * CELL_SIZE))
			#Entity handling

			if value == model.GATHERER: 
				g = grid.entityList[controller.findEntity(grid.entityList, p)]
				if g.move: 
					screen.blit(img.gathSprite, (x * CELL_SIZE, y * CELL_SIZE))
				else: 
					screen.blit(img.consumeList[g.animationLoop], (x * CELL_SIZE, y * CELL_SIZE))



			elif value == model.GENERATOR: 
				g = grid.entityList[controller.findEntity(grid.entityList, p)]
				screen.blit(img.marketList[g.times], (x * CELL_SIZE, y * CELL_SIZE))
			elif value == model.RESOURCE: 
				screen.blit(img.resSprite, (x * CELL_SIZE, y * CELL_SIZE))
			elif value == model.OBSTACLE: 
				screen.blit(img.Rock, (x * CELL_SIZE, y * CELL_SIZE))
			elif value == model.TRAIL: 
				screen.blit(img.Trail, (x * CELL_SIZE, y * CELL_SIZE))
			elif value == model.TRANSFORM: 
				g = grid.entityList[controller.findEntity(grid.entityList, p)]
				screen.blit(img.transformList[g.times - 1], (x * CELL_SIZE, y * CELL_SIZE))
				#if click-drag is used to place these, and then tried to transform, 
				#get error 


	mPointx = grid.mouseHover.x + origin.x 
	mPointy = grid.mouseHover.y + origin.y
	mPoint = entities.Point(mPointx, mPointy)
	hoverVal = model.get_cell(grid, mPoint)
	if hoverVal == model.EMPTY: 
		screen.blit(img.greenBox, (grid.mouseHover.x  * CELL_SIZE, grid.mouseHover.y * CELL_SIZE))
	else: 
		screen.blit(img.redBox,  (grid.mouseHover.x  * CELL_SIZE, grid.mouseHover.y * CELL_SIZE))
				