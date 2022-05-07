# a simple logic tree that would be used for travel between planets
# similar to overland travel in Pathfinder

from random import random as rnd

roll = lambda d: int(rnd()*d) + 1

# ship's attributes; these numbers are totally arbitrary
ship_speed = 10
ship_maneuver = 8
ship_accuracy = 5
ship_fuel = 100
ship_weapons = 5 # based on equipped weapons?

r = roll(20)

if r >= 10:
    print("You receive a distress signal")
elif r < 10:
    print("You're being pursued by pirates")
    r = roll(20) + ship_speed
    if r >= 18:
        print("You manage to outrun the pirates")
    else:
        print("The pirates are hot on your tail")
        r = roll(20) + ship_weapons
        if r >= 15:
            print("You've hit the pirates and they're backing off")
        else:
            print("You missed the pirates and are taking fire")
            r = roll(20) + ship_maneuver
            if r >= 16:
                print("You've managed to evade their weapons and escape")
            else:
                print("They've hit you and now you're being boarded")
                print("PREPARE FOR BATTLE!")
