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
WHITE = (255, 255, 255)
resSprite = None 
genSprite = None 
gathSprite = None 
Background = None 
Concrete = None  
Rock = None
Trail = None
greenBox = None
redBox = None


def loadSprites(): #Will be rewritten to use Dictionaries instead of globals 
	global resSprite
	global genSprite
	global gathSprite
	global Background
	global Concrete
	global Rock
	global Trail
	global greenBox
	global redBox
	resSprite = pygame.image.load(os.path.join("Monster.bmp")).convert()
	genSprite = pygame.image.load(os.path.join("Market.bmp")).convert()
	gathSprite = pygame.image.load(os.path.join("CSCStudent.bmp")).convert()
	Background = pygame.image.load(os.path.join("Background.bmp")).convert()
	Concrete = pygame.image.load(os.path.join("Concrete.bmp")).convert()
	Rock = pygame.image.load(os.path.join("Rocks.bmp")).convert()
	Trail = pygame.image.load(os.path.join("Trail.bmp")).convert()
	greenBox = pygame.image.load(os.path.join("greenBox.bmp")).convert()
	redBox = pygame.image.load(os.path.join("redBox.bmp")).convert()
	resSprite.set_colorkey(WHITE)
	genSprite.set_colorkey(WHITE)
	gathSprite.set_colorkey(WHITE)
	Background.set_colorkey(WHITE)
	Concrete.set_colorkey(WHITE)
	Rock.set_colorkey(WHITE)
	Trail.set_colorkey(WHITE)
	greenBox.set_colorkey(WHITE)
	redBox.set_colorkey(WHITE)

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
			'''
			Rewrite so that the grid holds Objects, only a 0 if empty
			if isinstance(value, entities.Gatherer): 
				if value.status = running: 
					blit the running sprite 
				elif value.status = consuming: 
					blit the consuming sprite 
			
			'''
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
	mPointx = grid.mouseHover.x + origin.x 
	mPointy = grid.mouseHover.y + origin.y
	mPoint = entities.Point(mPointx, mPointy)
	hoverVal = model.get_cell(grid, mPoint)
	if hoverVal == 0: 
		screen.blit(greenBox, (grid.mouseHover.x  * CELL_SIZE, grid.mouseHover.y * CELL_SIZE))
	else: 
		screen.blit(redBox,  (grid.mouseHover.x  * CELL_SIZE, grid.mouseHover.y * CELL_SIZE))
				