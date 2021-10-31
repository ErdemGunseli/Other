import pygame

#Colours:
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)

pygame.init()

#Blank Screen:

size = (640,480)
screen = pygame.display.set_mode(size)

#The title of the new window:

pygame.display.set_caption("My Window")

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
    #Next

    ##The Game Logic:

    #The screen background is BLACK:
    screen.fill(BLACK)
    

    #The first 2 values are the coordinates of the top left vertex.
    #And the last 2 values are the length and height respectively.
    pygame.draw.rect(screen, BLUE, (220,165,200,150))

    #The first coordinate is that of the center and the next value is the radius.
    #The last value is the thickness. 0 means it is filled.
    pygame.draw.circle(screen, YELLOW, (40,100),40,0)


    



    #Experimenting
    #pygame.draw.line(screen, YELLOW, (0,0),(100,100),width=20)
    #linePoints = [(10,10), (100,10), (100,100), (10, 100)]
    #pygame.draw.lines(screen, YELLOW, True, linePoints)


    #This will flip the display to reveal the new position of objects:
    pygame.display.flip()

    #The clock ticks over:
    clock.tick(60)

#endwhile - The end of the game loop.

pygame.quit()

        
