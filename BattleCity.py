import pygame
import time
import random
import sys

from math import pi

pygame.init()

clock = pygame.time.Clock()
# set title
pygame.display.set_caption('Battle City 2015')

######### resulotion and FPS ##############
display_width = 800
display_height = 600
FPS = 30
gameDisplay = pygame.display.set_mode((display_width, display_height))

########### colors #############
white = (255, 255, 255)
black = (0, 0, 0)
red = (155, 0, 0)
light_red = (255, 0, 0)
yellow = (150, 180, 0)
light_yellow = (255, 255, 0)
green = (34, 177, 76)
med_sea_green = (60, 179, 113)
light_green = (0, 255, 0)
oliva_drab = (107, 142, 35)
desert = (205, 133, 0)
desear_2 = (205, 179, 139)
fire_color = (205, 197, 191)

########### fonts ###############
smallfont = pygame.font.SysFont("comicsansms", 25)
midfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 75)

########### [begin] tank figure ###########
tank_width = 40
tank_height = 20
power_max = 100

move_sound = pygame.mixer.Sound("move.wav")
engine_sound = pygame.mixer.Sound("engine.wav")

# friendly tank position
tank_x = display_width * 0.1
tank_y = display_height * 0.9
########### [end] tank figure ###########
    
def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "mid":
        textSurface = midfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()
            
def message_to_screen(msg, color, y_display=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    # center the text
    textRect.center = (display_width / 2), (display_height / 2) + y_display
    gameDisplay.blit(textSurf, textRect)
        
def button(text, figure, color, shadowColor, action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(gameDisplay, color, figure)
    text_to_button(text, figure, shadowColor)
    if figure[0] + figure[2] > cur[0] > figure[0] and figure[1] + figure[3] > cur[1] > figure[1]:
        pointList = [(figure[0] - 1, figure[1]), (figure[0] - 1, figure[1] + figure[3]), (figure[0] + figure[2] - 1, figure[1] + figure[3])]
        pygame.draw.lines(gameDisplay, shadowColor, False, pointList, 2)
        if click[0] == 1 and action != None:
            if action == "play":
                game_loop()
        
def text_to_button(msg, figure, color, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((figure[0] + figure[2] / 2), (figure[1] + figure[3] / 2))
    gameDisplay.blit(textSurf, textRect)
        
####################### ###########################
#######################          ##################
#######################    ########################
#####################       #######################
################                 ##################
################                 ##################
#################  #  #  #  #  ####################
###################################################
def tank(x, y):
    x = int(x)
    y = int(y)
    # where the tank is
    pygame.draw.circle(gameDisplay, green, (x, y), tank_height / 2)
    # cannon turret position
    pygame.draw.line(gameDisplay, green, (x, y), (x + 20, y - 10), 5)
    # body and wheels
    pygame.draw.rect(gameDisplay, green, (x - tank_width / 2, y, tank_width, tank_height))
    wheel = x - tank_width / 2
    while wheel <= x + tank_width / 2:
        pygame.draw.circle(gameDisplay, green, (wheel, y + tank_height), tank_height / 4)
        wheel += tank_width / 8

def fire(power, turret_pos):
    print ("shot a cannon with " + str(power) + " power")
    
    bullets = turret_pos[0]
    while bullets <= display_width:
        print ("prepare to draw")
        pygame.draw.line(gameDisplay, red, (bullets, turret_pos[1]), (bullets + 5, turret_pos[1] + 5))
        print ("Drew")
        bullets += 10
    
        
def quit_event():
    pygame.quit()
    sys.exit()
 
def game_intro():
    intro = True
    
    while(intro):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_event()
        
        gameDisplay.fill(white)
        message_to_screen("Battle City 2015", green, -120, size = "large")
        message_to_screen("- shoot and destroy -", med_sea_green, -60)
        message_to_screen("Press P to pause during game play", black)
                    
        figure_play = (150, 500, 100, 50)
        button("Play", figure_play, med_sea_green, black, "play")
        pygame.display.update()
        clock.tick(FPS)
        
        
def game_loop():
    global tank_x
    global tank_y
    tank_move = 0
    power = 0
    
    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_event()
                
            ########## move friendly tank ##########
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pygame.mixer.Sound.stop(engine_sound)
                    pygame.mixer.Sound.play(move_sound)
                    tank_move = -5 
                elif event.key == pygame.K_RIGHT:
                    pygame.mixer.Sound.stop(engine_sound)
                    pygame.mixer.Sound.play(move_sound)
                    tank_move = 5 
                    
                # press SPACE to fire    
                elif event.key == pygame.K_SPACE:
                    power = 0.001
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    pygame.mixer.Sound.stop(move_sound)
                    pygame.mixer.Sound.play(engine_sound, -1)
                    tank_move = 0
                elif event.key == pygame.K_SPACE:
                    # release SPACE to fire
                    fire(power, (tank_x, tank_y))
                    print("here already")
                    power = 0
        tank_x += tank_move
        power += power
        
        # prevent tank from going through left edge
        if tank_x - tank_width / 2 - tank_height / 4 < 0:
            tank_x = tank_height / 4 + tank_width / 2
        # prevent fire power from exceeding maximum
        if power > power_max:
            power = power_max
        
        gameDisplay.fill(desear_2)
        
        ####### draw friendly tank ########
        tank(tank_x, tank_y)
        
        pygame.display.update()
        clock.tick(FPS)
    
    
game_intro()