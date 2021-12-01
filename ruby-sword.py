import pygame
import os
from pygame.locals import *
import sys
import time
 
pygame.init()

# define size constants
WIDTH = 800
HEIGHT = 350

FPS = 60
SPEED = 5
LIZARD_SPEED = 3

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

#get background image
print(os.path.join('bg.png'))
bg = pygame.transform.scale(pygame.image.load(os.path.join('bg.png')), (WIDTH, HEIGHT))


# get default sprite images
default_sprite_right = pygame.transform.scale(pygame.image.load(os.path.join( 'default-standing', 'standing-right.png')), (SPRITE_WIDTH, SPRITE_HEIGHT))
default_sprite_left = pygame.transform.scale(pygame.image.load(os.path.join( 'default-standing', 'standing-left.png')), (SPRITE_WIDTH, SPRITE_HEIGHT))
default_sprite_right.set_colorkey(SPRITE_SHEET_BG)
default_sprite_left.set_colorkey(SPRITE_SHEET_BG)

# player object
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 15
        self.is_jump = False
        self.left = False
        self.right = False
        self.attack = False
        self.walk_count = 0
        self.facing_right = True
        self.attack_frame = 0
        self.hitbox = (self.x + 15, self.y, 35, 80)
        self.hurtbox = (self.x + 15, self.y, 35, 80)

    
    def draw(self, screen):
        # walk count will cycle through the list of images in walk_right/walk_left
        # when walk count exceeds images * frame per images, reset to 0 and restart the cycle
        if self.walk_count + 1 >= 45:
            self.walk_count = 0
        if self.attack:
            #when attack is set to true (via spacebar) attack images are loaded and cycled through. images depend on which way self is facing
            if self.facing_right and self.attack_frame < 15:
                self.hitbox = (self.x + 60, self.y, 80, 80)
                self.hurtbox = (self.x + 20, self.y, 40, 80)
                image = attack_right[self.attack_frame//3]
                image.set_colorkey(SPRITE_SHEET_BG)
                image = pygame.transform.scale(image, (SPRITE_WIDTH * 3, SPRITE_HEIGHT))
                screen.blit(image, (self.x - attack_sprite_offset, self.y))
                self.attack_frame += 1
            elif not self.facing_right and self.attack_frame < 15:
                self.hitbox = (self.x - 60, self.y, 80, 80)
                self.hurtbox = (self.x + 20, self.y, 40, 80)
                image = attack_left[self.attack_frame//3]
                image.set_colorkey(SPRITE_SHEET_BG)
                image = pygame.transform.scale(image, (SPRITE_WIDTH * 3, SPRITE_HEIGHT))
                screen.blit(image, (self.x - attack_sprite_offset, self.y))
                self.attack_frame += 1
            # when all 25 frames have been used, set attack to false. this is to prevent animation loop. frames reset to 0 when attack key is pressed
            else:
                self.attack = False
        # if either left or right are true (when left/right keys are pressed), the images from corressponding list will load and cycle through as per walk_count
        # each image is shown for 5 frames as per the integer division
        # players x position will also moved by SPEED pixels in either direction
        elif self.right and self.x < WIDTH - SPRITE_WIDTH:
            self.x += SPEED
            image = walk_right[self.walk_count//5]
            image.set_colorkey(SPRITE_SHEET_BG)
            image = pygame.transform.scale(image, (SPRITE_WIDTH, SPRITE_HEIGHT))
            screen.blit(image, (self.x, self.y))
            self.walk_count += 1
            self.facing_right = True
        elif self.left and self.x > 0:
            self.x -= SPEED 
            image = walk_left[self.walk_count//5]
            image.set_colorkey(SPRITE_SHEET_BG)
            image = pygame.transform.scale(image, (SPRITE_WIDTH, SPRITE_HEIGHT))
            screen.blit(image, (self.x, self.y))
            self.walk_count += 1
            self.facing_right = False   
        
        # if neither left or right or attack is true, load default self
        else:
            if self.facing_right:
                screen.blit(default_sprite_right, (self.x, self.y))
            else:
                screen.blit(default_sprite_left, (self.x, self.y))

        # set the hitbox for character on each redraw
        pygame.draw.rect(screen, (255, 0, 0), (self.hitbox), 2)
        pygame.draw.rect(screen, (0, 255, 0), (self.hurtbox), 2)
        self.hitbox = (self.x + 15, self.y, 50, 80)
        self.hurtbox = (self.x + 15, self.y, 50, 80)



#lizard enemy object
class lizard(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.alive = True
        self.walk_count = 0
        self.left = False
        self.right = True
        self.hitbox = (self.x + 20, self.y, 40, 80)
        self.alive = True

    

    def draw(self, screen):
        if self.x > 750:
            self.left = True
            self.right = False
        elif self.x < 380:
            self.left = False
            self.right = True
        if self.walk_count + 1 >= 45:
            self.walk_count = 0
        if self.alive and self.right:
            self.x += LIZARD_SPEED
            image = lizard_walk_right[self.walk_count//5]
            image.set_colorkey(SPRITE_SHEET_BG)
            image = pygame.transform.scale(image, (SPRITE_WIDTH, SPRITE_HEIGHT))
            screen.blit(image, (self.x, self.y))
            self.walk_count += 1
            self.right = True
        elif self.alive and self.left:
            self.x -= LIZARD_SPEED 
            image = lizard_walk_left[self.walk_count//5]
            image.set_colorkey(SPRITE_SHEET_BG)
            image = pygame.transform.scale(image, (SPRITE_WIDTH, SPRITE_HEIGHT))
            screen.blit(image, (self.x, self.y))
            self.walk_count += 1
        
        # set the hitbox for character on each redraw  
        self.hitbox = (self.x + 20, self.y, 40, 80)
        pygame.draw.rect(screen, (255, 0, 0), (self.x + 20, self.y, 40, 80), 2)

        if not self.alive:
            del self



green_lizard = lizard(351, HEIGHT - 80, 80, 80)

lizard_list = []

for i in range(10):
    green_lizard1 = lizard(351 + (i * 20), HEIGHT - 80, 80, 80)
    lizard_list.append(green_lizard1)
    print(lizard_list)
SPAWNENEMY = pygame.USEREVENT



def check_for_hit(sprite, green_lizard):
    if sprite.attack and green_lizard.hitbox[0]  < sprite.hitbox[0] + sprite.hitbox[2] and green_lizard.hitbox[0] + green_lizard.hitbox[2] / 2 > sprite.hitbox[0]:
         pygame.draw.rect(screen, (0, 0, 255), (green_lizard.x + 20, green_lizard.y, 40, 140), 5)
         print(sprite.hitbox[0])
         green_lizard.alive = False
    # elif not sprite.attack and sprite.x < green_lizard.x and sprite.x + (sprite.width) > green_lizard.x:
    #     print('lose')


sprite = player(200, HEIGHT - 80, 80, 80)   
# import walking images
walk_right = [pygame.image.load(os.path.join( 'walking','R_0.png')), pygame.image.load(os.path.join( 'walking','R_1.png')), pygame.image.load(os.path.join( 'walking','R_2.png')), 
            pygame.image.load(os.path.join( 'walking','R_3.png')), pygame.image.load(os.path.join( 'walking','R_4.png')),
            pygame.image.load(os.path.join( 'walking','R_5.png')), pygame.image.load(os.path.join( 'walking','R_6.png')), pygame.image.load(os.path.join( 'walking','R_7.png')), 
            pygame.image.load(os.path.join( 'walking','R_8.png'))]

walk_left = [pygame.image.load(os.path.join( 'walking','L_0.png')), pygame.image.load(os.path.join( 'walking','L_1.png')), pygame.image.load(os.path.join( 'walking','L_2.png')), 
            pygame.image.load(os.path.join( 'walking','L_3.png')), pygame.image.load(os.path.join( 'walking','L_4.png')),
            pygame.image.load(os.path.join( 'walking','L_5.png')), pygame.image.load(os.path.join( 'walking','L_6.png')), pygame.image.load(os.path.join( 'walking','L_7.png')), 
            pygame.image.load(os.path.join( 'walking','L_8.png'))]

# import attacking images
attack_left = [pygame.image.load(os.path.join( 'attacking','attack_L0.png')), pygame.image.load(os.path.join( 'attacking','attack_L1.png')), pygame.image.load(os.path.join( 'attacking','attack_L2.png')),
                pygame.image.load(os.path.join( 'attacking','attack_L3.png')), pygame.image.load(os.path.join( 'attacking','attack_L4.png')), pygame.image.load(os.path.join( 'attacking','attack_L5.png'))]

attack_right = [pygame.image.load(os.path.join( 'attacking','attack_R0.png')), pygame.image.load(os.path.join( 'attacking','attack_R1.png')), pygame.image.load(os.path.join( 'attacking','attack_R2.png')),
                pygame.image.load(os.path.join( 'attacking','attack_R3.png')), pygame.image.load(os.path.join( 'attacking','attack_R4.png')), pygame.image.load(os.path.join( 'attacking','attack_R5.png'))]


#because attacking sprites are larger, need to offset them so they load in the same position as the default sprite
attack_sprite_offset = SPRITE_WIDTH

#import lizard enemy images
lizard_walk_right = [pygame.image.load(os.path.join( 'enemy_walk_right','enemy_R0.png')), pygame.image.load(os.path.join( 'enemy_walk_right','enemy_R1.png')), pygame.image.load(os.path.join( 'enemy_walk_right','enemy_R2.png')),
            pygame.image.load(os.path.join( 'enemy_walk_right','enemy_R3.png')), pygame.image.load(os.path.join( 'enemy_walk_right','enemy_R4.png')),
            pygame.image.load(os.path.join( 'enemy_walk_right','enemy_R5.png')), pygame.image.load(os.path.join( 'enemy_walk_right','enemy_R6.png')), pygame.image.load(os.path.join( 'enemy_walk_right','enemy_R7.png')), 
            pygame.image.load(os.path.join( 'enemy_walk_right','enemy_R8.png'))]

lizard_walk_left = [pygame.image.load(os.path.join( 'enemy_walk_left','enemy_L0.png')), pygame.image.load(os.path.join( 'enemy_walk_left','enemy_L1.png')), pygame.image.load(os.path.join( 'enemy_walk_left','enemy_L2.png')),
            pygame.image.load(os.path.join( 'enemy_walk_left','enemy_L3.png')), pygame.image.load(os.path.join( 'enemy_walk_left','enemy_L4.png')),
            pygame.image.load(os.path.join( 'enemy_walk_left','enemy_L5.png')), pygame.image.load(os.path.join( 'enemy_walk_left','enemy_L6.png')), pygame.image.load(os.path.join( 'enemy_walk_left','enemy_L7.png')), 
            pygame.image.load(os.path.join( 'enemy_walk_left','enemy_L8.png'))]

green_lizard1 = lizard(381, HEIGHT - 80, 80, 80)

#draw function will draw the screen and the players actions
def draw_window(sprite, green_lizard, screen, lizard_list):
    screen.blit(bg, (0,0))
    sprite.draw(screen)
    lizard_list[2].draw(screen)
    green_lizard.draw(screen) 
    green_lizard1.draw(screen) 
    
    pygame.display.update()

def createEnemy(screen):
    green_lizard1 = lizard(351, HEIGHT - 80, 80, 80)
    green_lizard1.draw(screen) 


def main():
    run = True
    clock = pygame.time.Clock()
    
    green_lizard1 = lizard(351, HEIGHT - 80, 80, 80)
    green_lizard1.draw(screen) 
    #main loop for running the game
    while run:
        clock = pygame.time.Clock()
        clock.tick(FPS)
        draw_window(sprite, green_lizard, screen,lizard_list)
        check_for_hit(sprite, green_lizard)
        keys_pressed = pygame.key.get_pressed()
        pygame.time.set_timer(SPAWNENEMY,1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
            if event.type == SPAWNENEMY:
                print('spawn')
                createEnemy(screen)
    
        # sprite_movement(keys_pressed, player)
        # left and right flags are used for walk animations
        # attack flag is also, used, below is logic so that sprite can't attack while walking. pressing atk button while stop walk
            if event.type == KEYDOWN:
                if pygame.key.name(event.key) == 'left' and sprite.x > 0: 
                    sprite.left = True 
                    sprite.right = False  
                    sprite.attack = False
                elif pygame.key.name(event.key) == 'right' and sprite.x < WIDTH - SPRITE_WIDTH:
                    sprite.left = False
                    sprite.right = True
                    sprite.attack = False

                #check for attack key press
                #set attack_frame back to 0 if it had been used before
                elif pygame.key.name(event.key) == 'space':
                    sprite.attack_frame = 0
                    sprite.attack = True
                    # sprite.right = False
                    # sprite.left = False
            elif event.type == KEYUP:
                if(pygame.key.name(event.key) == 'left'): 
                    sprite.left = False 
                elif(pygame.key.name(event.key) == 'right'):
                    sprite.right = False
                #check for attack key press
                

        #check for jump
        if sprite.is_jump == False and keys_pressed[pygame.K_UP]:
            sprite.is_jump = True

        if sprite.is_jump == True:
            if sprite.vel >= -15:
                sprite.y -= sprite.vel
                sprite.vel -= 1
            else:
                sprite.vel = 15
                sprite.is_jump = False


main()
