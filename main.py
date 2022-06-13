import pygame
import pong
import snake

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


def initalize():
    font = pygame.font.SysFont("comicsansms", 35)
    text = font.render("Press S to play Snake", True, WHITE)
    text_rect = text.get_rect(center=(windowWidth / 2, windowHeight / 2 - 100))
    window.blit(text, text_rect)

    text = font.render("Press P to play Pong", True, WHITE)
    text_rect = text.get_rect(center=(windowWidth / 2, windowHeight / 2))
    window.blit(text, text_rect)

    text = font.render("Press Q to quit", True, WHITE)
    text_rect = text.get_rect(center=(windowWidth / 2, windowHeight / 2 + 150))
    window.blit(text, text_rect)


#main function
def mainLoop():

    initalize()
    close = False

    while not close:
        for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    close = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pong.gameLoop()
                        initalize()
                    if event.key == pygame.K_s:
                        snake.gameLoop()
                        initalize()
            
        #update display
        pygame.display.update()
       
    pygame.quit()
    quit()
 
mainLoop()