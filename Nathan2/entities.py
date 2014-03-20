#will contain data definitions
import os, pygame
import random

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
		self.rate = random.randint(1000, 3000)
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

#Ordered list for actions.
class OrderedList():
	def __init__(self):
		self.list = []

	def empty(self):
		return not self.list

	def insert(self, item, ord):
		size = len(self.list)
		idx = 0
		
		while (idx < size and self.list[idx].ord < ord):
			idx += 1
		self.list[idx:idx] = [ListItem(item, ord)]

	def remove(self, item):
		size = len(self.list)
		idx = 0

		while (idx < size and self.list[idx].item != item):
			idx += 1

		if idx < size:
			self.list[idx:idx+1] = []

	def head(self):
		return self.list[0] if self.list else None

	def pop(self):
		if self.list:
			return self.list.pop(0)

class ListItem():
	def __init__(self, item, ord):
		self.item = item
		self.ord = ord

	def __eq__(a, b):
		return a.item == b.item and a.ord == b.ord