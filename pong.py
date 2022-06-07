from cmath import sqrt
import pygame
import time
from random import randint, random
from random import seed
from enum import Enum
 
#start the engine
pygame.init()
pygame.display.set_caption('Spielesammlung')
 
#define class Paddle
class Paddle:
    velocity = 0
    size = 150
    yPosition  = 0
    xPosition = 0
    def update(self, vel):
        velocity = vel
        self.yPosition += vel
        #pygame.draw.rect(window, WHITE, [Paddle.xPosition, Paddle.yPosition, 20,Paddle.size])


#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#define windowsize 
windowWidth = 1200
windowHeight = 900
window = pygame.display.set_mode((windowWidth, windowHeight))


#define Paddles
p1 = Paddle()
p2 = Paddle()

p1.xPosition = windowWidth-(windowWidth-20)
p2.xPosition = windowWidth -40


#clock for ticks 
clock = pygame.time.Clock()

#size of blocks and speed of the ball
ticktime = 60
ballspeed = 10
ballIncreasment = 1.10
paddleSpeed = 8

seed(time.time)

def gameLoop():
    #true when the window gets closed
    close = False
    #true when the game is over and the player can restart
    restart = False

    p1.yPosition=windowHeight/2 - p1.size/2
    p2.yPosition=windowHeight/2 - p2.size/2

    p1Vel = 0
    p2Vel = 0

    #define ball
    xBallVelocity = randint(-10,10)
    yBallVelocity = randint(-5,5)
    while xBallVelocity == 0:
        xBallVelocity = randint(-10,10)

    while yBallVelocity == 0:
        yBallVelocity = randint(-5,5)

    yBallPosition = windowHeight/2
    xBallPosition = windowWidth/2

    while not close:
        while restart == True:        
            #Display postgame info
            font = pygame.font.SysFont("comicsansms", 35)

            if (xBallPosition > windowWidth -100):
                text = font.render("Spieler 1 hat gewonnen", True, WHITE)
            if (xBallPosition < 100):
                text = font.render("Spieler 2 hat gewonnen", True, WHITE)
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
                if ( event.key == pygame.K_w ):
                    p1Vel = -paddleSpeed
                    break
                elif (event.key == pygame.K_s ):
                    p1Vel = paddleSpeed
                    break
                elif (event.key == pygame.K_UP):                 
                    p2Vel = -paddleSpeed
                    break
                elif (event.key == pygame.K_DOWN):                  
                    p2Vel = paddleSpeed
                    break   
            if event.type == pygame.KEYUP:
                if ( event.key == pygame.K_w ):
                    p1Vel = 0
                    break
                elif (event.key == pygame.K_s ):
                    p1Vel = 0
                    break
                elif (event.key == pygame.K_UP):                 
                    p2Vel = 0
                    break
                elif (event.key == pygame.K_DOWN):                  
                    p2Vel = 0
                    break   
        
        if(p1.yPosition+p1Vel<0 or p1.yPosition+150+p1Vel > windowHeight):
            p1Vel = 0
        if(p2.yPosition+p2Vel<0 or p2.yPosition+150+p2Vel > windowHeight):
            p2Vel = 0

        p1.update(p1Vel)
        p2.update(p2Vel)

        # ball movement

        length = sqrt(xBallVelocity*xBallVelocity+yBallVelocity*yBallVelocity).real

        xBallVelocity = (xBallVelocity/length)*ballspeed
        yBallVelocity = (yBallVelocity/length)*ballspeed

        if (xBallVelocity < 1 and xBallVelocity > 0):
            xBallVelocity += 1
        elif(xBallVelocity > -1 and xBallVelocity < 0):
            xBallVelocity += 1
        
        if (yBallVelocity < 1 and yBallVelocity > 0):
            yBallVelocity += 1
        elif(yBallVelocity > -1 and yBallVelocity < 0):
            yBallVelocity += 1
        
        xBallVelocity = int(xBallVelocity)
        yBallVelocity = int(yBallVelocity)

        xBallPosition += xBallVelocity
        yBallPosition += yBallVelocity

        #ball colision and velocity update for top and bottom wall  
        if(yBallPosition+15 > windowHeight):
            yBallVelocity = -yBallVelocity
        if(yBallPosition-15 < 0):
            yBallVelocity = -yBallVelocity


        #ball colision with paddle
        if(xBallPosition+15 > windowWidth-40):
            if(yBallPosition-15 > p2.yPosition+150 or yBallPosition+15< p2.yPosition):
                restart = True
            if(yBallPosition < p2.yPosition+50):
                xBallVelocity = -xBallVelocity*ballIncreasment
                yBallVelocity -= 1
            elif(p2.yPosition+50<=yBallPosition and yBallPosition < p2.yPosition+100):
                xBallVelocity = -xBallVelocity*ballIncreasment
            elif(p2.yPosition+100<=yBallPosition):
                xBallVelocity = -xBallVelocity*ballIncreasment
                yBallVelocity += 1


        if(xBallPosition-15 < 40):
            if(yBallPosition-15 > p1.yPosition+150 or yBallPosition+15< p1.yPosition):
                restart = True
            if(yBallPosition < p1.yPosition+50):
                xBallVelocity = -xBallVelocity*ballIncreasment
                yBallVelocity -= 1
            elif(p1.yPosition+50<=yBallPosition and yBallPosition < p1.yPosition+100):
                xBallVelocity = -xBallVelocity*ballIncreasment
            elif(p1.yPosition+100<=yBallPosition):
                xBallVelocity = -xBallVelocity*ballIncreasment
                yBallVelocity += 1


        #draw paddles, ball, background
        window.fill(BLACK)   
        pygame.draw.rect(window, WHITE, [p1.xPosition, p1.yPosition, 20, p1.size])
        pygame.draw.rect(window, WHITE, [p2.xPosition, p2.yPosition, 20, p2.size])   
        pygame.draw.circle(window, WHITE,[xBallPosition,yBallPosition],15,0)

        #update display
        pygame.display.update()
        #set speed/framerate
        clock.tick(ticktime)

    pygame.quit()
    quit()
 
