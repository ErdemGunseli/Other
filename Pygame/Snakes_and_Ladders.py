import pygame
import random

#Colours:
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)

pygame.init()
size = (640,480)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Snakes and Ladders")


class GameLogic():

    def generatePlayers(): # Generates Players
        numberOfPlayers = int(input("How many players will there be?\n"))
        for i in range(numberOfPlayers):
            myPlayer = Player(0)
            playerGroup.append(myPlayer)

    def generateSnakes(): # Generates Snakes
        for i in range(numberOfSnakes):
            mySnake = Snake(snakePositions[0], snakePositions[1])
            snakeGroup.append(mySnake)

    def generateLadders():# Generates Ladders
        for i in range(numberOfSnakes):
            myLadder = Ladder(ladderPositions[0], ladderPositions[1])
            snakeGroup.append(myLadder)
    
    def generateDice(): # Generates Dice
        numberOfFaces = input("How many faces should the dice have?\n")
        myDice = Dice(numberOfFaces)
        diceGroup.append(myDice)

    def startGame():# Generates Everything
        GameLogic.generateSnakes()
        GameLogic.generateLadders()
        GameLogic.generateDice()
        GameLogic.generatePlayers()
        

class GameBoard():
    pass

class Gateway(): # The parent class of snakes and ladders.

    def __init__(self, enterPos, exitPos): # Paramenters are the enter and exit positions, taken from a list.
        self.enterPos = enterPos
        self.exitPos = exitPos


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

            for i in gatewayPositions: # Checks the position of the player against a list of gateways to determine whether the player needs to be transported.
                if self.position == i[0]:
                    self.position = i[1]
                    print("They went through a gateway.")
                    # TODO: break
        print("They have been moved to " + str(self.position))
        print()
      
        return self.position
        # TODO: Snakes and Ladders transport player
    
    def update(self):
        for player in playerGroup:
            player.move()
        


class Dice():

    def __init__(self, numberOfFaces): # For flexibility, the parameters include the number of faces of the die as well as the number of dice.
        self.numberOfFaces = int(numberOfFaces)
    
    
    
    def diceRoll(self): # Rolls the dice and determines the score.

        result = random.randrange(1, self.numberOfFaces + 1) #change to self.numberOfFaces
        print("The result is " + str(result))
        return result
        

playerGroup = []
snakeGroup = []
ladderPositions = []
diceGroup = []

# The entrance and exit positions for snakes and ladders:
snakePositions = [(36, 6), (32, 10), (62, 18), (88, 24), (48, 26), (95, 56), (97, 78)]
ladderPositions = [(1, 38), (4, 14), (8, 30), (21, 42), (28, 76), (50, 67), (71, 92), (86, 99)]
gatewayPositions = snakePositions + ladderPositions

# QoL variables
numberOfSnakes = len(snakePositions)
numberOfLadders = len(ladderPositions)


done = False

clock = pygame.time.Clock()

GameLogic.startGame()

### This is the Game Loop:
while not done:
    pygame.event.get()
    screen.fill(WHITE)  
    pygame.draw.rect(screen, BLUE, (10, 10, 10, 10))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True



    for i in range(len(playerGroup)): # Should be i in playerGroup - current state for testing purposes.
        print("Player {}'s turn! ".format(str(i + 1)))
        playerGroup[i].move()




    pygame.display.flip()

    #The clock ticks over:
    clock.tick(60)



pygame.quit()

        
