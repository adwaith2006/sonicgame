import pygame#this module helps to build our game
import os
import random
pygame.init()

screen_height = 600#height and width of screen is stored in 2 variables
screen_width = 1100
screen = pygame.display.set_mode((screen_width, screen_height))#these values are set ot the screen

running = [pygame.image.load(os.path.join("Assets/Dino", "sonic1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "sonic2.png"))]#two images are added to make the object move
jumping = pygame.image.load(os.path.join("Assets/Dino", "sonicjump.png"))
ducking = [pygame.image.load(os.path.join("Assets/Dino", "sonicduck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "sonicduck2.png"))]



obstacle1 = [pygame.image.load(os.path.join("Assets/Cactus", "knuckles.png")),
               pygame.image.load(os.path.join("Assets/Cactus", "rock.png")),
               pygame.image.load(os.path.join("Assets/Cactus", "rock.png"))]         
   
bird = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]


bg = pygame.image.load(os.path.join("Assets/Other", "ground.png"))


class Sonic:
    x = 80
    y = 290
    y_duck = 340
    jump_velocity = 8.5#at this velocity the character is able to jump through the obstacle

    def __init__(sonic):#The python __init__ method is declared within a class and is used to initialize the attributes of an object as soon as the object is formed
        sonic.duck_img = ducking
        sonic.run_img = running
        sonic.jump_img = jumping

        sonic.sonic_duck = False
        sonic.sonic_run = True
        sonic.sonic_jump = False

        sonic.step_index = 0
        sonic.jump_vel = sonic.jump_velocity
        sonic.image = sonic.run_img[0]
        sonic.sonic_rect = sonic.image.get_rect()#coordinates of the object are provded
        sonic.sonic_rect.x = sonic.x
        sonic.sonic_rect.y = sonic.y

    def update(sonic, userInput):
        if sonic.sonic_duck:
            sonic.duck()#duck functon is called
        if sonic.sonic_run:
            sonic.run()#run functon is called
        if sonic.sonic_jump:
            sonic.jump()#jump functon is called

        if sonic.step_index >= 10:
            sonic.step_index = 0

        if userInput[pygame.K_UP] and not sonic.sonic_jump:#Inorder to avoid double jumping
            sonic.sonic_duck = False#when up arow key is pressed only jumping happens
            sonic.sonic_run = False
            sonic.sonic_jump = True
        elif userInput[pygame.K_DOWN] and not sonic.sonic_jump:
            sonic.sonic_duck = True#when down arow key is pressed only ducking happens
            sonic.sonic_run = False
            sonic.sonic_jump = False
        elif not (sonic.sonic_jump or userInput[pygame.K_DOWN]):
            sonic.sonic_duck = False#when no arowkey is pressed only running happens
            sonic.sonic_run = True
            sonic.sonic_jump = False

    def duck(sonic):#defining duck function
        sonic.image = sonic.duck_img[sonic.step_index // 5]
        sonic.sonic_rect = sonic.image.get_rect()
        sonic.sonic_rect.x = sonic.x
        sonic.sonic_rect.y = sonic.y_duck#tthe object will change its coordinates tot he given while ducking
        sonic.step_index += 1

    def run(sonic):
        sonic.image = sonic.run_img[sonic.step_index // 5]
        sonic.sonic_rect = sonic.image.get_rect()
        sonic.sonic_rect.x = sonic.x#these are the default coordinates of the object
        sonic.sonic_rect.y = sonic.y
        sonic.step_index += 1

    def jump(sonic):
        sonic.image = sonic.jump_img
        if sonic.sonic_jump:
            sonic.sonic_rect.y -= sonic.jump_vel * 4
            sonic.jump_vel -= 0.8
        if sonic.jump_vel < - sonic.jump_velocity:
            sonic.sonic_jump = False
            sonic.jump_vel = sonic.jump_velocity

    def draw(sonic, screen):
        screen.blit(sonic.image, (sonic.sonic_rect.x, sonic.sonic_rect.y))#blit() is used to place an image onto the screens of pygame applications



class Obstacle:
    def __init__(obstacle, image, type):
        obstacle.image = image
        obstacle.type = type
        obstacle.rect = obstacle.image[obstacle.type].get_rect()
        obstacle.rect.x = screen_width

    def update(self):
        self.rect.x -= game_speed#the x coordinates of the obstacle decrease simultaneouly with the ground which moves with gamespeed
        if self.rect.x < -self.rect.width:
            obstacles.pop()#obstacle goes out of screen

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)





class Knuckles(Obstacle):#class for obstacle
    def __init__(knuckles, image):
        knuckles.type = 0
        super().__init__(image, knuckles.type)
        knuckles.rect.y = 280


class Bird(Obstacle):#class for bird
    def __init__(bird, image):
        bird.type = 0
        super().__init__(image, bird.type)
        bird.rect.y = 220
        bird.index = 0

    def draw(bird, screen):#this fntn displays the images of the both obstacles
        if bird.index >= 9:
            bird.index = 0
        screen.blit(bird.image[bird.index//5], bird.rect)
        bird.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()#component of pygame,clock
    player = Sonic()

    game_speed = 30
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf',20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 0.5
        if points % 100 == 0:
            game_speed += 1#after each time score crosses 100 gamespeed increases

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        screen.blit(text, textRect)#the text is displayed

    def background():

        global x_pos_bg, y_pos_bg
        screen.blit(bg, (x_pos_bg, y_pos_bg))
        image_width = bg.get_width()
        screen.blit(bg, (x_pos_bg, y_pos_bg))
        screen.blit(bg, (image_width + x_pos_bg, y_pos_bg))

        if x_pos_bg <= -image_width:
            screen.blit(bg, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill((255,255,255))
        if points >700:
            screen.fill((0, 0, 0))#when points cross 700,the background turns dark
        if points >1400:
            screen.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()#when any key is pressed gameis started

        player.draw(screen)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 1:
                obstacles.append(Knuckles(obstacle1))#randomly both obstacles appear
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(bird))

        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            if player.sonic_rect.colliderect(obstacle.rect):#when player collides with obstacles(this is done by using colliderect fntn),game is stopped
                pygame.time.delay(1000)
                death_count += 1
                menu(death_count)

        background()



        score()

        clock.tick(30)
        pygame.display.update()

def menu(death_count):
    global points
    run = True
    while run:
        screen.fill((255,255,255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))

        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))

            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            try:
                s=str(points)
                f=open('score.txt','w+')
                f.write(s+'\n')
                
                
                
            except EOFError:
                break
            scoreRect = score.get_rect()
            scoreRect.center = (screen_width // 2, screen_height // 2 + 50)
            screen.blit(score, scoreRect)#points are displayed
        
        textRect = text.get_rect()
        textRect.center = (screen_width // 2, screen_height // 2)
        screen.blit(text, textRect)
        screen.blit(running[0], (screen_width // 2 - 20, screen_height // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)#initial death_count
