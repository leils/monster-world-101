import model
import entities

'''-------------------------------------------------------------------------'''
'''Save and Load'''

def save(grid, bgGrid):
	entityList = grid.entityList
	f = open('gaia.sav', 'w')
	
	for entity in entityList:
		if isinstance(entity, entities.CSCStudent):
			f.write('gatherer ' + str(entity.position.x) + ' ' + str(entity.position.y) + ' ' + str(entity.rate) + '\n')
		elif isinstance(entity, entities.CampusMarket):
			f.write('generator ' + str(entity.position.x) + ' ' + str(entity.position.y) + '\n')
		elif isinstance(entity, entities.MonsterEnergy):
			f.write('resource ' + str(entity.position.x) + ' ' + str(entity.position.y) + '\n')
		elif isinstance(entity, entities.Obstacle):
			f.write('obstacle ' + str(entity.position.x) + ' ' + str(entity.position.y) + '\n')

	for x in range(0, bgGrid.width):
		for y in range(0, bgGrid.height):
			p = entities.Point(x, y)
			if model.get_cell(bgGrid, p) == model.CONCRETE:
				f.write('concrete ' + str(x) + ' ' + str(y) + '\n')

	f.close()
	print("You saved the file!")

def load(grid, bgGrid):
	model.emptyGrid(grid)
	model.emptyGrid(bgGrid)
	newList = []

	with open('gaia.sav', 'r') as f:
		for line in f:
			l = line.split()
			if l[0] == 'gatherer':
				p = entities.Point(int(l[1]), int(l[2]))
				resLim = 5
				newEnt = entities.CSCStudent(resLim, p)
				newEnt.rate = int(l[2])*100
				#print('YOU FOUND A GATHERER')

			elif l[0] == 'generator':
				p = entities.Point(int(l[1]), int(l[2]))
				rate = 2
				newEnt = entities.CampusMarket(rate, p)
				#print('YOU FOUND A GENERATOR')

			elif l[0] == 'resource':
				p = entities.Point(int(l[1]), int(l[2]))
				newEnt = entities.MonsterEnergy(p)
				#print('YOU FOUND A RESOURCE')

			elif l[0] == 'obstacle':
				p = entities.Point(int(l[1]), int(l[2]))
				newEnt = entities.Obstacle(p)

			elif l[0] == 'concrete':
				p = entities.Point(int(l[1]), int(l[2]))
				value = 6
				model.set_cell(bgGrid, p, value)

			newList.append(newEnt)
		f.close()
		grid.entityList = newList
		print("You loaded the file!")