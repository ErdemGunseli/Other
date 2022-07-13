import random

# TODO: Import gateway positions from a seperate file.

playerGroup = []
snakeGroup = []
ladderGroup = []
diceGroup = []

# The entrance and exit positions for snakes and ladders:
snakePositions = [(36, 6), (32, 10), (62, 18), (88, 24), (48, 26), (95, 56), (97, 78)]
ladderPositions = [(1, 38), (4, 14), (8, 30), (21, 42), (28, 76), (50, 67), (71, 92), (86, 99)]

# QoL variables
numberOfSnakes = len(snakePositions)
numberOfLadders = len(ladderPositions)

class GameLogic:

    def generatePlayers(self): # Generates Players
        numberOfPlayers = int(input("\nHow many players will there be?    "))
        for player in range(numberOfPlayers):
            myPlayer = Player(0)
            playerGroup.append(myPlayer)

    def generateSnakes(self): # Generates Snakes
        for snake in range(numberOfSnakes):
            mySnake = Snake(snakePositions[snake][0], snakePositions[snake][1])
            snakeGroup.append(mySnake)

    def generateLadders(self):# Generates Ladders
        for ladder in range(numberOfLadders):
            myLadder = Ladder(ladderPositions[ladder][0], ladderPositions[ladder][1])
            ladderGroup.append(myLadder)
    
    def generateDice(self): # Generates Dice
        numberOfFaces = input("\nHow many faces should the dice have?     ")
        myDice = Dice(numberOfFaces)
        diceGroup.append(myDice)

    def startGame(self):# Generates Everything
        print("\nWelcome to Snakes & Ladders!\n")
        GameLogic.generateSnakes()
        GameLogic.generateLadders()
        GameLogic.generateDice()
        GameLogic.generatePlayers()
        GameLogic.playGame()
    
    def playGame(self): # Goes through each player and moves them.
        done = False
        while not done:
            for playerNumber in range(len(playerGroup)):
                if not done:
                    print("\nPlayer {}'s turn! Press ENTER to roll the dice!".format(str(playerNumber + 1)))
                    input()
                    position = playerGroup[playerNumber].move()
                    if position == 100: # Ends the game when a player has finished.
                        done = True
                        print("Player {} has reached 100 and won the game! Congratulations!".format(playerNumber + 1))


class Gateway: # The parent class of snakes and ladders.

    def __init__(self, enterPos, exitPos): # Paramenters are the enter and exit positions, taken from a list.
        self.enterPos = enterPos
        self.exitPos = exitPos

    def getEnterPos(self):
        return self.enterPos
    
    def getExitPos(self):
        return self.exitPos


class Snake(Gateway): # Child of gateways - doesn't need any specialised attributes and only exists for flexibility.

    def __init__(self, enterPos, exitPos):
        super().__init__(enterPos, exitPos)


class Ladder(Gateway): # Child of gateways - doesn't need any specialised attributes and only exists for flexibility.

    def __init__(self, enterPos, exitPos):
        super().__init__(enterPos, exitPos)

   
class Player():

    def __init__(self, position): # Takes in the position of the players.
        self.position = position

    def move(self): # Moves the players
        diceRoll = diceGroup[0].diceRoll()

        print("They were in " + str(self.position))

        if self.position + diceRoll <= 100: # The player cannot move past 100.
            self.position += diceRoll

            for snake in snakeGroup: # Checks the position of the player against a list of gateways to determine whether the player needs to be transported.
                for ladder in ladderGroup:
                    if self.position == Snake.getEnterPos(snake):
                        self.position = Snake.getExitPos(snake)
                        print("They went down a snake.")
                    elif self.position == Ladder.getEnterPos(ladder):
                        self.position = Ladder.getExitPos(ladder)
                        print("They went up a ladder.")
    
        print("They have been moved to {}.\n".format(str(self.position)))
      
        return self.position


class Dice():

    def __init__(self, numberOfFaces): # For flexibility, the parameters include the number of faces of the die as well as the number of dice.
        self.numberOfFaces = int(numberOfFaces)
    
    def diceRoll(self): # Rolls the dice and determines the score.

        result = random.randrange(1, self.numberOfFaces + 1) #change to self.numberOfFaces
        print("The result is " + str(result))
        return result
        

GameLogic.startGame()