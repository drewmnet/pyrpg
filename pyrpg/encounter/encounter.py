# PROTOTYPE

from random import random as rnd


class Enemy:
    def __init__(self, name):
        self.name = name
        self.target = None
        
    def acquire_target(self, party):
        member = int(rnd() * len(party))
        self.target = party[member]
        print(f"{self.name} targets {self.target.name}")
        
class Member:
    def __init__(self, name):
        self.name = name
        self.target = None
        
    def select_target(self, party):
        for n, member in enumerate(party):
            print(f"{n}: {member.name}")
        
        is_choosing = True
        while is_choosing:
            choice = int(input(f"{self.name}'s target: "))
            if choice >= 0 and choice < len(party):
                self.target = party[choice]
                is_choosing = False
                print(f"{self.name} targets {self.target.name}")
            else:
                print("Choice out of range")
            
cok1 = Enemy("Cockatrice")
cok2 = Enemy("Cockatrice")
enemy_party = [ cok1, cok2 ]

elaine = Member("Elaine")
talin = Member("Talin")
avat5 = Member("AVAT5")
player_party = [ elaine, talin, avat5 ]

for enemy in enemy_party:
    enemy.acquire_target(player_party)
    
for member in player_party:
    member.select_target(enemy_party)


'''
    Enemy mob touches player
    Fade out and fade into encounter screen
    Get input for each live player character
     [ a selector box ]
    Get commands for each enemy and their targets
    Roll for initiative
    Begin combat
    Resolve status effects
    Get input for each live player character

'''

