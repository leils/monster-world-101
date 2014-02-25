import os 
import entities 
import pickle

p1 = entities.Point(2, 2)
p2 = entities.Point(3, 5)
p3 = entities.Point(2, 9)
p4 = entities.Point(0, 1)
gatherer = entities.CSCStudent('Nathan', 3, p1)
generator = entities.CampusMarket('market', 6, p2)
res1 = entities.MonsterEnergy('res', p3)
res2 = entities.MonsterEnergy('res2', p4)

entList = [gatherer, generator, res1, res2]

with open('gaia.sav', 'wb') as output: 
	pickle.dump(entList, output, pickle.HIGHEST_PROTOCOL)

f = open('gaia.sav', 'r')
newList = pickle.load(f)
'''
for ent in entList: 
	if isinstance(ent, entities.CSCStudent): 

		f.write('gatherer' + ' ' + ent.name + ' ' + str(ent.resource_limit) + ' ' + str(ent.position.x) + ' ' + str(ent.position.y))
	elif isinstance(ent, entities.CampusMarket): 
		f.write(ent.name + ' ' + ent.rate + ' ' + ent.position.x + ' ' + ent.position.y)
	elif isinstance(ent, entities.MonsterEnergy): 
		f.write(ent.name + ' ' + ent.position.x + ' ' + ent.position.y)

	
f.close()
		'''