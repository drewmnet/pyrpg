import operator
from random import random as rnd

class Battler:
    def __init__(self, name, agility):
        self.name = name
        self.agility = agility
        
        self.initiative = 0
        
    def roll(self):
        self.initiative = int(rnd() * 20) + 1 + self.agility

fighters = [ Battler("Elaine", 2),Battler("Talin", 3),Battler("AVAT5", 1),Battler("Cok1", 3),Battler("Cok2", 3) ]

for fighter in fighters:
    fighter.roll()

for fighter in sorted(fighters, key=operator.attrgetter('initiative'))[::-1]:
    print(f"{fighter.name} {fighter.initiative}")
