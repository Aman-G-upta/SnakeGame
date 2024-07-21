import pygame
import random
import os
import sys

# pygame.mixer.init()

a = pygame.init()
# Checking that init function is properly initialized or not
# print(a)

# Color
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)
green=(0,100,0)
yellow=(255,255,0)

screen_width=900
screen_height=600
clock=pygame.time.Clock()

# Creating a gaming window
game_window=pygame.display.set_mode((screen_width,screen_height))

# Background image for welcome
bgimgforwelcome=pygame.image.load("images/snakelogo.png")
bgimgforwelcome=pygame.transform.scale(bgimgforwelcome,(screen_width,screen_height)).convert_alpha()

# Background image for game over
bgimgforgameover=pygame.image.load("images/gameover.png")
bgimgforgameover=pygame.transform.scale(bgimgforgameover,(screen_width,screen_height)).convert_alpha()

# Background image for playing snake window
bgimgforplayingsnake=pygame.image.load("images/snake.png")
bgimgforplayingsnake=pygame.transform.scale(bgimgforplayingsnake,(screen_width,screen_height)).convert_alpha()

font = pygame.font.SysFont('Harrington', 55)
# 55 is basically a font size

# Setting a name of the game
pygame.display.set_caption("Snake Game ")
pygame.display.update()

def text_screen(text,color,x,y):
    screen_text=font.render(text,True,color)
    game_window.blit(screen_text,[x,y])

def plot_snake(game_window,color,snake_list,snake_size):
    for x,y in snake_list:
       pygame.draw.rect(game_window,color,[x,y,snake_size,snake_size])

with open("hiscore.txt","r") as f:
        hiscore=f.read()       

def welcome():
    pygame.mixer.music.load("songs/welcome_bgm.mp3")
    pygame.mixer.music.play(-1)
    exit_game=False
    while not exit_game:
        # game_window.fill((128,128,128))
        game_window.blit(bgimgforwelcome,(0,0))
        
        # text_screen("Welcome to snake",black,120,160)
        text_screen("Press Enter To Continue !!",green,230,420)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game=True
            if event.type==pygame.KEYDOWN:     
                if event.key==pygame.K_RETURN:
                    pygame.mixer.music.load("songs/bgm.mp3")
                    pygame.mixer.music.play(-1)
                    gameloop()    

        pygame.display.update()
        clock.tick(60)        

# Creating a game loop
def gameloop():
    
    # creating an game specific variable
    exit_game=False
    game_over=False
    snake_x=45
    snake_y=55
    snake_size=25
    clock=pygame.time.Clock()
    fps=30
    init_velocity=5
    velocity_x=0
    velocity_y=0
    score=0
    food_x=random.randint(20,screen_width//2)
    food_y=random.randint(20,screen_height//2)
    snake_list=[]
    snake_length=1
    if (not os.path.exists("hiscore.txt")):
        with open("hiscore.txt","w") as f:
            f.write("0")

    with open("hiscore.txt","r") as f:
        hiscore=f.read()       

    while not exit_game:

        if game_over:
            with open("hiscore.txt","w") as f:
                f.write(str(hiscore))
                game_window.blit(bgimgforgameover,(0,0))
                text_screen("Hiscore : "+ str(hiscore),yellow,320,500)
                text_screen("Press enter to continue",yellow,230,540)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game= True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        pygame.mixer.music.load("songs/bgm.mp3")
                        pygame.mixer.music.play()
                        gameloop()    
        else:    

            for event in pygame.event.get():
            #   print(event)
                if event.type==pygame.QUIT:
                    exit_game= True
                if event.type== pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT:
                        velocity_x=init_velocity
                        velocity_y=0
                    if event.key==pygame.K_LEFT:
                        velocity_x=-init_velocity
                        velocity_y=0    
                    if event.key==pygame.K_DOWN:
                        velocity_y=init_velocity
                        velocity_x=0          
                    if event.key==pygame.K_UP:
                        velocity_y=-init_velocity
                        velocity_x=0
            
            snake_x+=velocity_x
            snake_y+=velocity_y

            if abs(snake_x-food_x)<6 and abs(snake_y-food_y)<6:
                score+=10        
                food_x=random.randint(20,screen_width//2)
                food_y=random.randint(20,screen_height//2)
                snake_length+=5

                if score>int(hiscore):
                    hiscore=score

            game_window.blit(bgimgforplayingsnake,(0,0))
            text_screen("Score : "+str(score)+"       Hiscore : "+ str(hiscore),black,5,5)
            pygame.draw.circle(game_window, red, (food_x + snake_size // 2, food_y + snake_size // 2), snake_size // 2)

            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
            if len(snake_list)>snake_length:
                del snake_list[0]
            if head in snake_list[:-1]:
                game_over=True
                pygame.mixer.music.load("songs/game-over.mp3")
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over=True
                game_window.blit(bgimgforwelcome,(0,0))
                pygame.mixer.music.load("songs/game-over.mp3")
                pygame.mixer.music.play()    
            plot_snake(game_window,green,snake_list,snake_size)
        
        # If what ever we make changes in the display we have to update the display as below
        pygame.display.update()
        clock.tick(fps)
        
    pygame.quit()
    sys.exit()

welcome() 

# What is an event
# Anything that we are doing from the keyboard are event