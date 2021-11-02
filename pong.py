import pygame
import math
import random
from pygame.constants import K_UP
pygame.font.init()

#Colours:
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)

ballColour = [50, 50, 250]

pygame.init()

#Blank Screen:

size = (640,480)
screen = pygame.display.set_mode(size)


ballWidth = 20
ballX = 150
ballY = 200

xDirection = 1
yDirection = 1

paddX = 0
paddY = 60

paddXLength = 15
paddYLength = 60

paddMovePerFrame = 15 #The number of pixels the ball moves per frame.

score = 0
highScore = 0

#The title of the new window:
pygame.display.set_caption("Pong")

#When this is true, the game will end:
done = False

clock = pygame.time.Clock()


   
### This is the Game Loop:
while not done:
    
    #User inputs and controls:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        #endif    
    #next
    
    keys = pygame.key.get_pressed()
    # If the up key is pressed and the paddle won't go offscreen, move it up.
    if keys[pygame.K_UP] and (paddY - paddMovePerFrame >= 0):
        paddY -= paddMovePerFrame
    #endif

    # If the down key is pressed and the paddle won't go offscreen, move it down.
    if keys[pygame.K_DOWN] and (paddY + paddMovePerFrame <= 420):
        paddY += paddMovePerFrame
    #endif

    ##The Game Logic:
    screen.fill(BLACK)

    pygame.draw.rect(screen, ballColour, (ballX,ballY,ballWidth,ballWidth)) #Ball
    pygame.draw.rect(screen, WHITE, (paddX,paddY,paddXLength,paddYLength)) #Paddle

     # If the ball has collided with the right wall, make it bounce.
    if ballX >= 640 - ballWidth:
        xDirection = -xDirection

    # If the ball has gone past the left wall, reset it.
    elif ballX < 0 - ballWidth:
        ballX = 150
        ballY = 200
        xDirection = 1
        yDirection = 1
        score = 0
        ballColour = [50, 50, 250]

    #If the ball hits the top or bottom of the screen, make it bounce.
    elif (ballY <= 0) or (ballY >= 480 - ballWidth):
        yDirection = -yDirection

    #If the ball hits the face of the paddle, make it bounce.
    elif (ballX == paddXLength) and (ballY <= paddY + paddYLength) and (paddY <= ballWidth + ballY):    
        
        # Make the ball and paddle speed up each time it is hit by the paddle.
        xDirection = -2 * xDirection
        yDirection = 2 * yDirection

        # Increases the score by 1.
        score += 1
        if score > highScore:
            highScore = score

        # Changes the colour of the ball.
        if ballColour[0] + 50 <= 250:
            ballColour[0] = ballColour[0] + 50
        if ballColour[2] - 50 <= 0:
            ballColour[2] = ballColour[2] - 50

    # Move the ball in the given direction.
    ballX += xDirection
    ballY += yDirection

    score_font = pygame.font.SysFont('Comic Sans MS', 15)
    yourScore = score_font.render("Your Score:", False, YELLOW)
    scoreDisplay = score_font.render(str(score), False, ballColour)
    
    yourHighScore = score_font.render("Highscore:", False, YELLOW)
    highScoreDisplay = score_font.render(str(highScore), False, ballColour)

    
    screen.blit(yourScore, (20,0))
    screen.blit(scoreDisplay,(110,0))

    screen.blit(yourHighScore, (20,15))
    screen.blit(highScoreDisplay, (110,15))

    #This will flip the display to reveal the new position of objects:
    pygame.display.flip()

    #The clock ticks over:
    clock.tick(60)

#endwhile - The end of the game loop.

pygame.quit()

        
