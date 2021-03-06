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

		self.resource_limit = r
		self.position = p
		self.resource_count = 0
		self.image = None
		self.aim = None 
		self.rate = random.randint(200, 2000) #change to parameter. Set when initialized
		self.direction = NEAR
		self.priY = False
		self.dirx = None
		self.diry = None
		self.registered = False
		self.move = True
		self.animationLoop = 0 #0 or 1 for blink animation
		self.animationTimes = 0 #0-10
		 
class CampusMarket(): 
	def __init__(self, r, p):

		self.rate = 200
		self.position = p
		self.times = 0
		self.registered = False

class MonsterEnergy(): 
	def __init__(self, p):

		self.position = p
		self.delayTime = 2000

class Obstacle(): 
	def __init__(self, p): 
		self.position = p

class transformingMonster(): 
	def __init__(self, p): 
		self.position = p
		self.times = 0
		self.rate = 200
		#will blit an image of exploding 
		#after delayTime, switches to different exploding 
		#after 2 images blitted, turns into an obstacle (rock) 

class Images(): 
	def __init__(self): 
		self.resSprite = None
		self.gathSprite = None 
		self.Background = None 
		self.Concrete = None  
		self.Rock = None
		self.Trail = None
		self.greenBox = None
		self.redBox = None
		self.T1 = None
		self.T2 = None
		self.C1 = None
		self.C2 = None
		self.M1 = None
		self.M2 = None
		self.M3 = None
		self.transformList = []
		self.consumeList = []
		self.marketList = []

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