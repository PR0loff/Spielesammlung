import pygame
import time
import random
from enum import Enum
 
#start the engine
pygame.init()
pygame.display.set_caption('Spielesammlung')
 
#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#define windowsize 
windowWidth = 1200
windowHeight = 900
window = pygame.display.set_mode((windowWidth, windowHeight))


#clock for ticks 
clock = pygame.time.Clock()

#size of blocks and speed of the snake
blocksize = 30
ticktime = 15
 
#class for the last direction
class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

#main function
def gameLoop():
    #true when the window gets closed
    close = False
    #true when the game is over and the player can restart
    restart = False

    #current Direction
    xVelocity = 0
    yVelocity = 0
    lastDirection = -1
    
    #the list containing all snake rectangles
    snakeList = [pygame.Rect(windowWidth / 2,  windowHeight / 2, blocksize, blocksize)]
    
    #spawn food at random location
    foodX = round(random.randrange(0, windowWidth - blocksize) / blocksize) * blocksize
    foodY = round(random.randrange(0, windowHeight - blocksize) / blocksize) * blocksize

    while not close:
        while restart == True:        
            #Display postgame info
            font = pygame.font.SysFont("comicsansms", 35)

            text = font.render("Your score: " + str(len(snakeList)) + "!", True, WHITE)
            text_rect = text.get_rect(center=(windowWidth / 2, windowHeight / 2 - 50))
            window.blit(text, text_rect)

            text = font.render("Press R to restart or Q to Quit", True, WHITE)
            text_rect = text.get_rect(center=(windowWidth / 2, windowHeight / 2 + 50))
            window.blit(text, text_rect)

            pygame.display.update()

            #handle Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close = True
                    restart = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        gameLoop()
                    if event.key == pygame.K_q:
                        close = True
                        restart = False

        #handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
            #movement: only allow one input per game tick
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and lastDirection != Direction.RIGHT:
                    xVelocity = -blocksize
                    yVelocity = 0
                    lastDirection = Direction.LEFT
                    break
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and lastDirection != Direction.LEFT:
                    xVelocity = blocksize
                    yVelocity = 0
                    lastDirection = Direction.RIGHT
                    break
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and lastDirection != Direction.DOWN:                 
                    xVelocity = 0
                    yVelocity = -blocksize
                    lastDirection = Direction.UP
                    break
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and lastDirection != Direction.UP:                  
                    xVelocity = 0
                    yVelocity = blocksize
                    lastDirection = Direction.DOWN
                    break   


        #clone the last snakepiece on top of the snakehead
        snakeList.insert(0, pygame.Rect(snakeList[-1].x, snakeList[-1].y, blocksize, blocksize))
        
        #move the cloned snakepiece according to input
        snakeList[0].x = snakeList[1].x + xVelocity
        snakeList[0].y = snakeList[1].y + yVelocity

        #collision with food
        if snakeList[0].x == foodX and snakeList[0].y == foodY:
            #yes: spawn new food
            while(True):
                spawnInsideSnake = False
                foodX = round(random.randrange(0, windowWidth - blocksize) / blocksize) * blocksize
                foodY = round(random.randrange(0, windowHeight - blocksize) / blocksize) * blocksize
                for x in snakeList:
                    if (x.x == foodX and x.y == foodY):
                        spawnInsideSnake = True
                        break
                if (not spawnInsideSnake):
                    break
        else:
            #no: delete the last snakepiece because its the new snakehead
            del snakeList[-1]

        #collision with boarders
        if snakeList[0].x >= windowWidth or snakeList[0].x < 0 or snakeList[0].y >= windowHeight or snakeList[0].y < 0:
            restart = True

        #collision with own body
        for x in snakeList[1:]:
            if (snakeList[0].x == x.x and snakeList[0].y == x.y):
                restart = True

        #draw snake, food, background
        window.fill(BLACK)    
        for x in snakeList:
            pygame.draw.rect(window, WHITE, x)
        pygame.draw.rect(window, RED, [foodX, foodY, blocksize, blocksize])       

        #update display
        pygame.display.update()
        
        #set speed/framerate
        clock.tick(ticktime)

    pygame.quit()
    quit()
