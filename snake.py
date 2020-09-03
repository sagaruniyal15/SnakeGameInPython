import os
import pygame as py
import random
py.mixer.init()
py.init()

#colors
white = (255,255,255)
red = (255,0,0)
black =(0,0,0)
green = (0,255,0)

fps = 60

def plot(gameWindow,color,snk_list,size):
    for x,y in snk_list:
        py.draw.rect(gameWindow,color,[x,y,size,size])

clock = py.time.Clock()
font = py.font.SysFont(None,30)


def text_on_screen(text,color,x,y):
    '''this function is for printing the score on the screen i.e  game window '''
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])


#screen width and height
width = 600
height = 400

# creating game window
gameWindow = py.display.set_mode((width,height))

bgimg1 = py.image.load("outro.png")
bgimg2 = py.image.load("gameOver.jpg")
bgimg1 = py.transform.scale(bgimg1,(width,height)).convert_alpha()
bgimg2 = py.transform.scale(bgimg2,(width,height)).convert_alpha()

# game title
py.display.set_caption("Snake Game")
py.display.update()

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(black)
        gameWindow.blit(bgimg1,(0,0))
        # text_on_screen("WELCOME TO SNAKE GAME",white,180,150)
        text_on_screen("PRESS SPACE BAR TO PLAY GAME",white,130,280)
        for event in py.event.get():
                if event.type == py.QUIT:
                    exit_game = True
                if event.type == py.KEYDOWN:
                    if event.key == py.K_SPACE:
                        gameloop()
                
        py.display.update()
        clock.tick(60)

def gameloop():
    # game specific variable
    exit_game = False
    game_over = False
    snake_size = 15
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    score = 0
    init__velocity = 3
    food_x = random.randint(15,width-15)
    food_y = random.randint(15,height-15)
    snake_length = 1
    snake_list = []
    # check whether highscore.txt exixts or not
    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt",'w') as f:
            f.write('0')

    with open("highscore.txt",'r') as f:
        hiscore = f.read() 

    while not exit_game:
        if game_over:
            with open("highscore.txt",'w') as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            gameWindow.blit(bgimg2,(0,0))
            text_on_screen("SCORE : "+str(score),red,250,200)
            text_on_screen("PRESS ENTER TO PLAY AGAIN",red,150,230)
            for event in py.event.get():
                if event.type == py.QUIT:
                    exit_game = True
                if event.type == py.KEYDOWN:
                    if event.key == py.K_RETURN:
                        welcome()

        else:
            for event in py.event.get():
                if event.type == py.QUIT:
                    exit_game = True
                if event.type == py.KEYDOWN:
                    if event.key == py.K_RIGHT or event.key == py.K_d:
                        velocity_x = init__velocity
                        velocity_y = 0
                    if event.key == py.K_LEFT or event.key == py.K_a:
                        velocity_x = -init__velocity
                        velocity_y = 0
                    if event.key == py.K_DOWN or event.key == py.K_s:
                        velocity_y = init__velocity
                        velocity_x = 0
                    if event.key == py.K_UP or event.key == py.K_w:
                        velocity_y = -init__velocity
                        velocity_x = 0
                    if event.key == py.K_q:
                        score += 5
                
            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x)<7 and abs(snake_y - food_y)<7:
                score += 10
                food_x = random.randint(20,width-20)
                food_y = random.randint(20,height-20)
                snake_length += 5
                py.mixer.music.load("eat.mp3")
                py.mixer.music.play()

                if score > int(hiscore):
                    hiscore = score


            gameWindow.fill(black)
            
            text_on_screen("SCORE : "+str(score) + " HI SCORE : "+ str(hiscore),green,5,5)
            py.draw.rect(gameWindow,red,[food_x,food_y,snake_size,snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if snake_x < 2 or snake_x > width-2 or snake_y < 2 or snake_y > height-2:
                game_over = True
                py.mixer.music.load("game_over.mp3")
                py.mixer.music.play()
            
            if head in snake_list[:-1]:
                game_over = True
                py.mixer.music.load("game_over.mp3")
                py.mixer.music.play()

            # py.draw.rect(gameWindow,black,[snake_x,snake_y,snake_size,snake_size])
            plot(gameWindow,white,snake_list,snake_size)
            
        py.display.update()
        clock.tick(fps)

    py.quit()
    quit()

if __name__ == "__main__":
    welcome()