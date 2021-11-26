import pygame
import os
from pygame.locals import *
import sys
 

# define size constants
WIDTH = 800
HEIGHT = 350

FPS = 60
SPEED = 5

# color variables
WHITE = (0, 255, 255)
BLACK = (0, 0, 0)
BROWN = (100, 100, 100)
GREEN = (34, 177, 76)
SPRITE_SHEET_BG = (192, 192, 192)

# sprites size
SPRITE_HEIGHT = 80
SPRITE_WIDTH = 80

# create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# set caption
pygame.display.set_caption('Ruby Sword')

# variables for the sprite
sprite_x = 200
sprite_y = HEIGHT - 64

#get background image
print(os.path.join('bg.png'))
bg = pygame.transform.scale(pygame.image.load(os.path.join('bg.png')), (WIDTH, HEIGHT))


# get default sprite images
default_sprite_right = pygame.transform.scale(pygame.image.load(os.path.join( 'default-standing', 'standing-right.png')), (SPRITE_WIDTH, SPRITE_HEIGHT))
default_sprite_left = pygame.transform.scale(pygame.image.load(os.path.join( 'default-standing', 'standing-left.png')), (SPRITE_WIDTH, SPRITE_HEIGHT))
default_sprite_right.set_colorkey(SPRITE_SHEET_BG)
default_sprite_left.set_colorkey(SPRITE_SHEET_BG)



# import walking images
walk_right = [pygame.image.load(os.path.join( 'walking','R_0.png')), pygame.image.load(os.path.join( 'walking','R_1.png')), pygame.image.load(os.path.join( 'walking','R_2.png')), pygame.image.load(os.path.join( 'walking','R_3.png')), pygame.image.load(os.path.join( 'walking','R_4.png')),
            pygame.image.load(os.path.join( 'walking','R_5.png')), pygame.image.load(os.path.join( 'walking','R_6.png')), pygame.image.load(os.path.join( 'walking','R_7.png')), 
            pygame.image.load(os.path.join( 'walking','R_8.png'))]

walk_left = [pygame.image.load(os.path.join( 'walking','L_0.png')), pygame.image.load(os.path.join( 'walking','L_1.png')), pygame.image.load(os.path.join( 'walking','L_2.png')), pygame.image.load(os.path.join( 'walking','L_3.png')), pygame.image.load(os.path.join( 'walking','L_4.png')),
            pygame.image.load(os.path.join( 'walking','L_5.png')), pygame.image.load(os.path.join( 'walking','L_6.png')), pygame.image.load(os.path.join( 'walking','L_7.png')), 
            pygame.image.load(os.path.join( 'walking','L_8.png'))]

# import attacking images
attack_left = [pygame.image.load(os.path.join( 'attacking','attack_L0.png')), pygame.image.load(os.path.join( 'attacking','attack_L1.png')), pygame.image.load(os.path.join( 'attacking','attack_L2.png')),
                pygame.image.load(os.path.join( 'attacking','attack_L3.png')), pygame.image.load(os.path.join( 'attacking','attack_L4.png')), pygame.image.load(os.path.join( 'attacking','attack_L5.png'))]

attack_right = [pygame.image.load(os.path.join( 'attacking','attack_R0.png')), pygame.image.load(os.path.join( 'attacking','attack_R1.png')), pygame.image.load(os.path.join( 'attacking','attack_R2.png')),
                pygame.image.load(os.path.join( 'attacking','attack_R3.png')), pygame.image.load(os.path.join( 'attacking','attack_R4.png')), pygame.image.load(os.path.join( 'attacking','attack_R5.png'))]

# variables for walking, direction and attack_frame will need to be accessed globally
walk_count = 0
facing_right = True
attack_frame = 0

#because attacking sprites are larger, need to offset them so they load in the same position as the default sprite
attack_sprite_offset = SPRITE_WIDTH

#draw function will draw the screen and the players actions
def draw_window(player, left, right, attack):
    global walk_count
    global facing_right
    global attack_frame
    screen.blit(bg, (0,0))
    # walk count will cycle through the list of images in walk_right/walk_left
    # when walk count exceeds images * frame per images, reset to 0 and restart the cycle
    if walk_count + 1 >= 45:
        walk_count = 0
    if attack_frame >= 25:
        attack_frame = 0
        attack = False
    if attack:
        #when attack is set to true (via spacebar) attack images are loaded and cycled through. images depend on which way sprite is facing
        if facing_right:
            image = attack_right[attack_frame//5]
            image.set_colorkey(SPRITE_SHEET_BG)
            image = pygame.transform.scale(image, (SPRITE_WIDTH * 3, SPRITE_HEIGHT))
            screen.blit(image, (player.x - attack_sprite_offset, player.y))
            attack_frame += 1
        else:
            image = attack_left[attack_frame//5]
            image.set_colorkey(SPRITE_SHEET_BG)
            image = pygame.transform.scale(image, (SPRITE_WIDTH * 3, SPRITE_HEIGHT))
            screen.blit(image, (player.x - attack_sprite_offset, player.y))
            attack_frame += 1
    # if either left or right are true (when left/right keys are pressed), the images from corressponding list will load and cycle through as per walk_count
    # each image is shown for 5 frames as per the integer division
    # players x position will also moved by SPEED pixels in either direction
    elif right:
        player.x += SPEED
        image = walk_right[walk_count//5]
        image.set_colorkey(SPRITE_SHEET_BG)
        image = pygame.transform.scale(image, (SPRITE_WIDTH, SPRITE_HEIGHT))
        screen.blit(image, (player.x, player.y))
        walk_count += 1
        facing_right = True
    elif left:
        player.x -= SPEED 
        image = walk_left[walk_count//5]
        image.set_colorkey(SPRITE_SHEET_BG)
        image = pygame.transform.scale(image, (SPRITE_WIDTH, SPRITE_HEIGHT))
        screen.blit(image, (player.x, player.y))
        walk_count += 1
        facing_right = False   
    
    # if neither left or right or attack is true, load default sprite
    else:
        if facing_right:
            screen.blit(default_sprite_right, (player.x, player.y))
        else:
            screen.blit(default_sprite_left, (player.x, player.y))

            
    pygame.display.update()


def main():
    player = pygame.Rect(sprite_x, HEIGHT - SPRITE_HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT)
    run = True
    is_jump = False
    vel_y = 15
    clock = pygame.time.Clock()
 
    # walking animation
    left = False
    right = False
    attack = False
    
    #main loop for running the game
    while run:
        clock = pygame.time.Clock()
        clock.tick(FPS)
        draw_window(player, left, right, attack)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        keys_pressed = pygame.key.get_pressed()
        # sprite_movement(keys_pressed, player)
        # left and right flags are used for walk animations
        # attack flag is also, used, below is logic so that sprite can't attack while walking. pressing atk button while stop walk
        if(keys_pressed[pygame.K_LEFT] and player.x > 0): 
            left = True 
            right = False  
            attack = False
        elif(keys_pressed[pygame.K_RIGHT] and player.x < WIDTH - SPRITE_WIDTH):
            left = False
            right = True
            attack = False
        else:
            right = False
            left = False
            walk_count = 0
        #check for attack key press
        if(keys_pressed[pygame.K_SPACE]):
            print(keys_pressed)
            print('attack')
            attack = True
            right = False
            left = False
        else:
            attack = False
        

        #check for jump
        if is_jump == False and keys_pressed[pygame.K_UP]:
            is_jump = True

        if is_jump == True:
            if vel_y >= -15:
                player.y -= vel_y
                vel_y -= 1
            else:
                vel_y = 15
                is_jump = False


main()