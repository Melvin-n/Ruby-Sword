import pygame
import os
from pygame.locals import *
import time
import random
 
pygame.init()

# define size constants
WIDTH = 800
HEIGHT = 350

# FPS and player speed
FPS = 60
SPEED = 5

# speed and spawn time for enemies, will change in further levels of the game
spawn_time = 2500
spawn_fast = 1750
spawn_fastest = 1250
spawn_extreme = 750
spawn_impossible = 500

# define spawn enemy event, call it periodically
SPAWNENEMY = pygame.USEREVENT
pygame.time.set_timer(SPAWNENEMY, spawn_time)


# define game over event
GAME_OVER = pygame.USEREVENT



# color variables
WHITE = (0, 255, 255)
BLACK = (0, 0, 0)
BROWN = (100, 100, 100)
GREEN = (34, 177, 76)
RUBY = (155, 17, 30)
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

# audio files
missed_attack_audio = pygame.mixer.Sound('audio/missed_attack_audio.mp3')
hit_audio = pygame.mixer.Sound('audio/hit_audio.mp3')
death_audio = pygame.mixer.Sound('audio/death_audio.mp3')


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
        self.alive = True

    
    def draw(self, screen):
        # walk count will cycle through the list of images in walk_right/walk_left
        # when walk count exceeds images * frame per images, reset to 0 and restart the cycle
        if self.alive:
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
        self.speed = 3
            
          

    def draw(self, screen):
        if self.x > 750:
            self.left = True
            self.right = False
        elif self.x < 0:
            self.left = False
            self.right = True
        if self.walk_count + 1 >= 45:
            self.walk_count = 0
        if self.alive and self.right:
            self.x += self.speed
            image = lizard_walk_right[self.walk_count//5]
            image.set_colorkey(SPRITE_SHEET_BG)
            image = pygame.transform.scale(image, (SPRITE_WIDTH, SPRITE_HEIGHT))
            screen.blit(image, (self.x, self.y))
            self.walk_count += 1
            self.right = True
        elif self.alive and self.left:
            self.x -= self.speed 
            image = lizard_walk_left[self.walk_count//5]
            image.set_colorkey(SPRITE_SHEET_BG)
            image = pygame.transform.scale(image, (SPRITE_WIDTH, SPRITE_HEIGHT))
            screen.blit(image, (self.x, self.y))
            self.walk_count += 1
        
        # set the hitbox for character on each redraw  
        self.hitbox = (self.x + 20, self.y, 40, 80)

        if not self.alive:
            del self

# define list for lizards, this will hold all enemies after creation
lizard_list = []

#logic for checking hitbox collisions
def check_for_hit(sprite, enemy):
    
    # if start enemey hit box is less than end of sprite hit box and end of enemy hitbox is more than start of sprite hit box
    
    if sprite.attack and sprite.facing_right and enemy.hitbox[0] < sprite.hitbox[0] + 80 and enemy.hitbox[0] > sprite.hitbox[0] and sprite.y == enemy.y:       
        enemy.alive = False
        hit_audio.play()
    # if facing left and enemy hit box is more than end of sprite hitbox and less than start of sprite hitbox
    if sprite.attack and not sprite.facing_right and enemy.hitbox[0] > sprite.hitbox[0] - 80 and enemy.hitbox[0]  < sprite.hitbox[0] and sprite.y == enemy.y:
        enemy.alive = False 
        hit_audio.play()
    # if players hurt box is inside enemy, player loses
    if sprite.hurtbox[0] > enemy.hitbox[0] and sprite.hurtbox[0] < enemy.hitbox[0] + 40 and sprite.y == enemy.y:
        sprite.alive = False
        death_audio.play()
    if sprite.hurtbox[0] + 50 > enemy.hitbox[0] and sprite.hurtbox[0] + 50 < enemy.hitbox[0] + 40 and sprite.y == enemy.y:
        sprite.alive = False
        death_audio.play()



 

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

# get the score by checking how many in lizard list are !alive
def check_score():
    score = 0
    for lizard in lizard_list:
        if not lizard.alive:
            score += 1
    return score

# declare fonts
score_font = pygame.font.SysFont("bookmanoldstyle", 25)
lose_font = pygame.font.SysFont("bookmanoldstyle", 40)
title_font = pygame.font.SysFont("bookmanoldstyle", 60, bold=True)
intro_font = pygame.font.SysFont("bookmanoldstyle", 20, bold=True)
instructions_font = pygame.font.SysFont("bookmanoldstyle", 15)

#draw function will draw the screen and the players actions
def draw_window(sprite, score, screen):
    screen.blit(bg, (0,0))
    if sprite.alive:
        screen.blit(bg, (0,0))
        sprite.draw(screen)
        # draw each enemy which is in the lizard_list, which is being updated on SPAWNENEMY event, also check for hit of each enemy
        # set the speed for enemies once a certain number have been killed
        for liz in lizard_list:
            if liz.alive:
                if lizard_list.index(liz) > 18:
                    liz.speed = 6
                if lizard_list.index(liz) > 10:
                    liz.speed = 5
                if lizard_list.index(liz) > 3:
                    liz.speed = 4
                liz.draw(screen)
                check_for_hit(sprite, liz)
                
        # display score
        score_display = score_font.render(f'Score: {str(score)}', True, (255, 255, 255))
        screen.blit(score_display, (40, 40))
    if not sprite.alive:
        
        lose_text = lose_font.render(f'Game over!', True, (255, 255, 255))
        final_score = lose_font.render(f'Final score: {str(score)}', True, (255, 255, 255))
        back_to_intro = intro_font.render('Press any key to return', True, (255, 255, 255))
        screen.blit(lose_text, (280, 120))
        screen.blit(final_score, (260, 170))
        screen.blit(back_to_intro, (272, 310))
        
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                GAME_OVER
                sprite.left = False
                sprite.right = False
                sprite.attack = False
                lizard_list.clear()
                sprite.alive = True
                intro()
            if event.type == pygame.QUIT:
                pygame.quit()

    pygame.display.update()



# create player
sprite = player(200, HEIGHT - 80, 80, 80)  

# create  enemies, this is called whenever SPAWNENEMY event is triggered
# 3 types of spawns, left side, right side, or both sides. decided by randomiser each time. 
# spawn speed increases as amount of kills grows
def create_enemy():
    enemy_spawn_type = random.randint(1, 3)
    if len(lizard_list) > 35:
        pygame.time.set_timer(SPAWNENEMY, spawn_impossible)
    elif len(lizard_list) > 20:
        pygame.time.set_timer(SPAWNENEMY, spawn_extreme)
    elif len(lizard_list) > 12:
        pygame.time.set_timer(SPAWNENEMY, spawn_fastest)
    elif len(lizard_list) > 5:
        pygame.time.set_timer(SPAWNENEMY, spawn_fast)
    
    
    if enemy_spawn_type  == 1:
        green_lizard28 = lizard(750, HEIGHT - 80, 80, 80) 
        lizard_list.append(green_lizard28)
    elif enemy_spawn_type  == 2: 
        green_lizard27 = lizard(0, HEIGHT - 80, 80, 80) 
        lizard_list.append(green_lizard27)
    elif enemy_spawn_type  == 3:
        green_lizard31 = lizard(0, HEIGHT - 80, 80, 80)
        green_lizard32 = lizard(750, HEIGHT - 80, 80, 80)
        lizard_list.append(green_lizard32)
        lizard_list.append(green_lizard31)

    


def main():
    run = True
    clock = pygame.time.Clock()
    
    
    #main loop for running the game
    while run:
        clock = pygame.time.Clock()
        clock.tick(FPS)
        score = check_score()
        draw_window(sprite, score, screen)
        keys_pressed = pygame.key.get_pressed()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
            if event.type == SPAWNENEMY:
                create_enemy()
                print(score)

            if event.type == GAME_OVER:
                if not sprite.alive:
                    print('game over')
                    run = False
    
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
                    missed_attack_audio.play()
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

def intro():
    intro = True

    while intro:
        screen.blit(bg, (0,0))
        title_text = title_font.render('Ruby Sword', True, RUBY) 
        intro1_text = intro_font.render('The lizard race has taken over!', True, RUBY)
        intro2_text = intro_font.render('Only the holder of the Ruby Sword can slay them.', True, RUBY)
        enter_to_start_text = instructions_font.render('Press enter to start, spacebar to attack, arrow keys to move/jump. ', True, (255, 255, 255))
        screen.blit(title_text, (220, 10))
        screen.blit(intro1_text, (240, 120))
        screen.blit(intro2_text, (150, 155))
        screen.blit(enter_to_start_text, (163, 300))

        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == KEYDOWN:
                if pygame.key.name(event.key) == 'return':
                    main()
                    intro = False
                    
                    pygame.display.update()


intro()


