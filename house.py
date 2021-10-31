import pygame
import math

from pygame.constants import KEYDOWN

#Colours:
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)
DARKRED = (125, 15, 10)
PALEGREEN = (80, 100, 80)
DARKGREEN = (25,75,10)
GREY = (50,50,50)
skyColour = [30,25,100] #The default sky colour.
windowColour = BLUE

sunSpeed = 5

pygame.init()

#Blank Screen:
size = (640,480)
screen = pygame.display.set_mode(size)

#The title of the new window:
pygame.display.set_caption("My Window")

#When this is true, the game will end:
done = False
sunX = 40
sunY = 100


clock = pygame.time.Clock()


def skyColourChanger(skyColour): #This function changes the colour of the sky according to the x-position of the Sun.
    
    if sunX >= 0 and sunX <= size[0]:
        skyColourIncrement = math.sin(math.pi * (sunX / size[0])) #Outputs a value between 0 and 1.
        skyColour[0] = 25 + 10 * skyColourIncrement #Adds a value between 0 and 10 to the red.
        skyColour[1] = 20 + 75 * skyColourIncrement
        skyColour[2] = 75 + 100 * skyColourIncrement
        return skyColour

def sunMover(sunX): #This function moves the sun in an ark.
    if sunX <= 680: 
        sunX += sunSpeed
    else:
        pygame.time.wait(10000 // sunSpeed)
        sunX = -40
    sunY =  100 - 50 * math.sin(math.pi * (sunX / size[0]))
    return sunX, sunY

def windowColourChanger(sunX): #This function changes the colour of the windows depending on the x-position of the Sun.
    if sunX >= 80 and sunX <= 600: 
        return BLUE
    else:
        return YELLOW

### This is the Game Loop:  
while not done:

    #User inputs and controls:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Allows the changing of the speed of the Sun.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                sunSpeed = sunSpeed + 1
            elif event.key == pygame.K_DOWN:
                sunSpeed = sunSpeed - 1
        #endif
    #Next

    ##The Game Logic:
    screen.fill(skyColour)
 
    skycolour = skyColourChanger(skyColour) #Calls the function that changes the colour of the sky.
    sunX, sunY = sunMover(sunX)
    windowColour = windowColourChanger(sunX)


    pygame.draw.rect(screen, PALEGREEN, (220,360,200,150)) #House
    pygame.draw.rect(screen, GREY, (250, 300, 30, 60))
    pygame.draw.polygon(screen, DARKRED, ((200,360), (440, 360), (320,300))) #Roof
    pygame.draw.circle(screen, YELLOW, (sunX,sunY), 40, 0) #Sun
    
    for i in range(0,150,5): #Places bricks with offset rows
        for j in range(0,200,10):
            if i % 10 == 0:
                pygame.draw.rect(screen,DARKGREEN, (220 + j, 360 + i,10,5), 1)
            elif j <= 180:
                pygame.draw.rect(screen,DARKGREEN, (225 + j, 360 + i,10,5), 1)

    pygame.draw.rect(screen, GREY, (295,410,50,70)) #Door
    
    pygame.draw.rect(screen, windowColour, (250, 400, 30, 30)) #Left Window
    pygame.draw.rect(screen, windowColour, (360, 400, 30, 30)) #Right Window
    
 
    #This will flip the display to reveal the new position of objects:
    pygame.display.flip()

    #The clock ticks over:
    clock.tick(60)

#endwhile - The end of the game loop.
pygame.quit()
