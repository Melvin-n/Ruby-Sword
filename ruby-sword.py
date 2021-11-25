import pygame
import os

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
bg = pygame.transform.scale(pygame.image.load(os.path.join('cs50-final','bg.png')), (WIDTH, HEIGHT))



default_sprite = pygame.transform.scale(pygame.image.load(os.path.join('cs50-final','defaultSprite.png')), (SPRITE_WIDTH, SPRITE_HEIGHT))
default_sprite.set_colorkey(SPRITE_SHEET_BG)


# import walking images
walk_right = [pygame.image.load(os.path.join('cs50-final', 'walking','R_0.png')), pygame.image.load(os.path.join('cs50-final', 'walking','R_1.png')), pygame.image.load(os.path.join('cs50-final', 'walking','R_2.png')), pygame.image.load(os.path.join('cs50-final', 'walking','R_3.png')), pygame.image.load(os.path.join('cs50-final', 'walking','R_4.png')),
            pygame.image.load(os.path.join('cs50-final', 'walking','R_5.png')), pygame.image.load(os.path.join('cs50-final', 'walking','R_6.png')), pygame.image.load(os.path.join('cs50-final', 'walking','R_7.png')), 
            pygame.image.load(os.path.join('cs50-final', 'walking','R_8.png'))]

walk_left = [pygame.image.load(os.path.join('cs50-final', 'walking','L_0.png')), pygame.image.load(os.path.join('cs50-final', 'walking','L_1.png')), pygame.image.load(os.path.join('cs50-final', 'walking','L_2.png')), pygame.image.load(os.path.join('cs50-final', 'walking','L_3.png')), pygame.image.load(os.path.join('cs50-final', 'walking','L_4.png')),
            pygame.image.load(os.path.join('cs50-final', 'walking','L_5.png')), pygame.image.load(os.path.join('cs50-final', 'walking','L_6.png')), pygame.image.load(os.path.join('cs50-final', 'walking','L_7.png')), 
            pygame.image.load(os.path.join('cs50-final', 'walking','L_8.png'))]

walk_count = 0


def draw_window(player, left, right):
    global walk_count
    screen.blit(bg, (0,0))
    # walk count will cycle through the list of images in walk_right/walk_left
    # when walk count exceeds images * frame per images, reset to 0 and restart the cycle
    if walk_count + 1 >= 45:
        walk_count = 0
    # if either left or right are true (when left/right keys are pressed), the images from corressponding list will load and cycle through as per walk_count
    # each image is shown for 5 frames as per the integer division
    if right:
        image = walk_right[walk_count//5]
        image.set_colorkey(SPRITE_SHEET_BG)
        image = pygame.transform.scale(image, (SPRITE_WIDTH, SPRITE_HEIGHT))
        screen.blit(image, (player.x, player.y))
        walk_count += 1
        print('right')
    elif left:
        image = walk_left[walk_count//5]
        image.set_colorkey(SPRITE_SHEET_BG)
        image = pygame.transform.scale(image, (SPRITE_WIDTH, SPRITE_HEIGHT))
        screen.blit(image, (player.x, player.y))
        walk_count += 1
        print('yes')
    # if neither left or right is true, load default sprite
    else:
        screen.blit(default_sprite, (player.x, player.y))
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
    
    

    while run:
        clock = pygame.time.Clock()
        clock.tick(FPS)
        draw_window(player, left, right)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        keys_pressed = pygame.key.get_pressed()
        # sprite_movement(keys_pressed, player)
        # left and right flags are used for walk animations
        if(keys_pressed[pygame.K_LEFT] and player.x > 0):
            player.x -= SPEED  
            left = True 
            right = False            
        elif(keys_pressed[pygame.K_RIGHT] and player.x < WIDTH - SPRITE_WIDTH):
            player.x += SPEED
            left = False
            right = True
        else:
            right = False
            left = False
            walk_count = 0
        #check for jump
        if is_jump == False and keys_pressed[pygame.K_UP]:
            is_jump = True

            walk_count = 0
        if is_jump == True:
            if vel_y >= -15:
                player.y -= vel_y
                vel_y -= 1
            else:
                vel_y = 15
                is_jump = False


main()