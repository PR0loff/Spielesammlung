import pygame
import time
import random
 
#start the engine
pygame.init()
 
#define colors
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 102)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

#define windowsize 
dis_width = 1200
dis_height = 900
dis = pygame.display.set_mode((dis_width, dis_height))

pygame.display.set_caption('Spielesammlung')
 
#clock for ticks 
clock = pygame.time.Clock()

#size of blocks and speed of the snake
snake_block = 10
blocksize = 30
snake_speed = 15
 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)



 
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])
  
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
 
 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
 
 
def gameLoop():
    game_over = False
    game_close = False
 
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_list = [pygame.Rect(x1, y1, blocksize, blocksize)]
 
    foodx = round(random.randrange(0, dis_width - blocksize) / blocksize) * blocksize
    foody = round(random.randrange(0, dis_height - blocksize) / blocksize) * blocksize


    while not game_over:
 
        while game_close == True:
            dis.fill(blue)
            
            message("You Lost! Press C-Play Again or Q-Quit", red)
            #Your_score(Length_of_snake - 1)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.type == pygame.QUIT:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -blocksize
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = blocksize
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -blocksize
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = blocksize
                    x1_change = 0

        #draw snake, food, background
        for x in snake_list:
            pygame.draw.rect(dis, white, x)
        pygame.draw.rect(dis, green, [foodx, foody, blocksize, blocksize])
        dis.fill(blue)
        
        #clone the last snakepiece on top of the snakehead
        snake_list.insert(0, pygame.Rect(snake_list[-1].x, snake_list[-1].y, blocksize, blocksize))
        
        #move the cloned snakepiece according to input
        snake_list[0].x = snake_list[1].x + x1_change
        snake_list[0].y = snake_list[1].y + y1_change

        #collision with food
        if snake_list[0].x == foodx and snake_list[0].y == foody:
            #yes: spawn new food
            foodx = round(random.randrange(0, dis_width - blocksize) / blocksize) * blocksize
            foody = round(random.randrange(0, dis_height - blocksize) / blocksize) * blocksize
        else:
            #no: delete the last snakepiece because its the new snakehead
            del snake_list[-1]

        #collision with boarders
        if snake_list[0].x >= dis_width or snake_list[0].x < 0 or snake_list[0].y >= dis_height or snake_list[0].y < 0:
            game_close = True

        #collision with own body
        for x in snake_list[1:]:
            if (snake_list[0].x == x.x and snake_list[0].y == x.y):
                game_close = True

        #update display
        pygame.display.update()
        
        #set speed/framerate
        clock.tick(snake_speed)

    pygame.quit()
    quit()
 
gameLoop()