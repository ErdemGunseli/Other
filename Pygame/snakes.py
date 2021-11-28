import random

class GameLogic():

    def generatePlayers(numberOfPlayers):
        for i in range(numberOfPlayers):
            myPlayer = Player(0)
            playerGroup.append(myPlayer)

    def generateSnakes(numberOfSnakes):
        for i in range(numberOfSnakes):
            mySnake = Snake(snakePositions[0], snakePositions[1])
            snakeGroup.append(mySnake)

    def generateLadders(numberofLadders):
        for i in range(numberOfSnakes):
            myLadder = Ladder(ladderPositions[0], ladderPositions[1])
            snakeGroup.append(myLadder)

class GameBoard():
    pass

class Gateway(): # The parent class of snakes and ladders.

    def __init__(self, enterPos, exitPos): # Paramenters are the enter and exit positions, taken from a list.
        self.enterPos = enterPos
        self.exitPos = exitPos


class Snake(Gateway): # Child of gateways - doesn't need any specialised attributes and only exists for flexibility.

    def __init__(self):
        super.__init__()
       


class Ladder(Gateway): # Child of gateways - doesn't need any specialised attributes and only exists for flexibility.

    def __init__(self):
        super.__init__()
      


class Player():

    def __init__(self, position): # Takes in the position of the players.
        self.position = position

    def move(self): # Moves the players
        diceRoll = Dice.diceRoll(Dice)

        if self.position + diceRoll <= 100: # The player cannot move past 100.
            self.position += diceRoll

            for i in gatewayPositions: # Checks the position of the player against a list of gateways to determine whether the player needs to be transported.
                if self.position == i[0]:
                    self.position = i[1]
                    # TODO: break
        
        return self.position
        # TODO: Snakes and Ladders transport player
    
    def update(self):
        for i in playerGroup:
            i.update(self)
        


class Dice():

    def __init__(self, numberOfFaces, numberOfDice): # For flexibility, the parameters include the number of faces of the die as well as the number of dice.
        self.numberOfFaces = numberOfFaces
        self.numberOfDice = numberOfDice
    
    def diceRoll(self): # Rolls the dice and determines the score.
        result = 0
        for i in range(self.numberOfDice):
            result += random.randrange(1, self.numberOfFaces)
        return result


# Groups for objects
playerGroup = []
snakeGroup = []
ladderPositions = []

# The entrance and exit positions for snakes and ladders:
snakePositions = [(36, 6), (32, 10), (62, 18), (88, 24), (48, 26), (95, 56), (97, 78)]
ladderPositions = [(1, 38), (4, 14), (8, 30), (21, 42), (28, 76), (50, 67), (71, 92), (86, 99)]
gatewayPositions = snakePositions + ladderPositions

print(gatewayPositions)

# QoL variables
numberOfSnakes = len(snakePositions)
numberOfLadders = len(ladderPositions)


numberOfPlayers = int(input("How many players will there be? "))

GameLogic.generatePlayers(numberOfPlayers)
GameLogic.generateSnakes(numberOfSnakes)
GameLogic.generateLadders(numberOfLadders)

playerGroup.update()