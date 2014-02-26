import pygame 
import os 
import entities
import model
#manages drawing to screen 

'''
Draws the world. 
Allows you to move the viewpoint (scan through the world) 
DOES NO ACTUAL MODIFICATION TO THE WORLD, ONLY DRAWS 
'''
# define cell size
CELL_SIZE = 32
resSprite = None 
genSprite = None 
gathSprite = None 
Background = None 
Concrete = None  
Rock = None
Trail = None


def loadSprites(): 
	global resSprite
	global genSprite
	global gathSprite
	global Background
	global Concrete
	global Rock
	global Trail
	resSprite = pygame.image.load(os.path.join("Monster.png")).convert_alpha()
	genSprite = pygame.image.load(os.path.join("Market.png")).convert_alpha()
	gathSprite = pygame.image.load(os.path.join("CSCStudent.png")).convert_alpha()
	Background = pygame.image.load(os.path.join("Background.jpg")).convert_alpha()
	Concrete = pygame.image.load(os.path.join("Concrete.png")).convert_alpha()
	Rock = pygame.image.load(os.path.join("Rocks.png")).convert_alpha()
	Trail = pygame.image.load(os.path.join("Trail.png")).convert_alpha()

# draw the 2D grid
# can edit to take in a list and determine the image that should be placed 
def draw(screen, grid, bgGrid, screenW, screenH): #originPoint, viewH viewW (IN GRIDS)
	origin = grid.origin
	for y in range(0, screenH):
		for x in range(0, screenW):
			p = entities.Point(x + origin.x, y + origin.y)
			value = model.get_cell(grid, p)
			bgValue = model.get_cell(bgGrid, p)
			#Background handling - concrete and grass
			screen.blit(Background, (x * CELL_SIZE, y * CELL_SIZE))
			if bgValue == 6: 
				screen.blit(Concrete, (x * CELL_SIZE, y * CELL_SIZE))
			#Entity handling
			if value == 1: 
				screen.blit(gathSprite, (x * CELL_SIZE, y * CELL_SIZE))
			elif value == 2: 
				screen.blit(genSprite, (x * CELL_SIZE, y * CELL_SIZE))
			elif value == 3: 
				screen.blit(resSprite, (x * CELL_SIZE, y * CELL_SIZE))
			elif value == 4: 
				screen.blit(Rock, (x * CELL_SIZE, y * CELL_SIZE))
			elif value == 5: 
				screen.blit(Trail, (x * CELL_SIZE, y * CELL_SIZE))
				