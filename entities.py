#will contain data definitions
import os, pygame

NEAR = 0
FAR = 1

class Point():
	def __init__(self, a, b): 
		self.x = a
		self.y = b

class CSCStudent():  
	def __init__(self, r, p):

		#pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.image.load(os.path.join("Ash.png")).convert()

		self.resource_limit = r
		self.position = p
		self.resource_count = 0
		self.aim = None 
		self.rate = 100
		self.direction = NEAR

class CampusMarket(): 
	def __init__(self, r, p):

		#pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.image.load(os.path.join("House.png")).convert()

		self.rate = r
		self.position = p

#pygame.sprite.Sprite
class MonsterEnergy(): 
	def __init__(self, p):

		#pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.image.load(os.path.join("Ball.png")).convert()

		self.position = p
		self.delayTime = 2000

class Obstacle(): 
	def __init__(self, p): 
		self.position = p