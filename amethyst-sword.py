import pygame
import os

# define size constants
WIDTH = 600
HEIGHT = 450

FPS = 60
SPEED = 5

# color variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (100, 100, 100)
GREEN = (0, 255, 150)


SPRITE_HEIGHT = 60
SPRITE_WIDTH = 45
SPRITE = pygame.transform.scale(pygame.image.load(os.path.join('cs50-final', 'swordman-1.png')), (SPRITE_WIDTH, SPRITE_HEIGHT))
WALK = pygame.transform.scale(pygame.image.load(os.path.join('cs50-final', 'swordman-2.png')), (SPRITE_WIDTH, SPRITE_HEIGHT))

#isWalking = False


pygame.display.set_caption('Amethyst Sword')

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_window(player, isWalking):
    WIN.fill(WHITE)
    #WIN.blit(SPRITE, (player.x, player.y))
    if isWalking:
        WIN.blit(WALK, (player.x, player.y))
    else:
        WIN.blit(SPRITE, (player.x, player.y))
    pygame.display.update()


def sprite_movement(keys_pressed, player, isWalking): 
    #horizontal movement, make sure sprite is not past screen boundaries
    
    if(keys_pressed[pygame.K_LEFT] and player.x > 0):
        player.x -= SPEED
        isWalking = True

    if(keys_pressed[pygame.K_RIGHT] and player.x < WIDTH - SPRITE_WIDTH):
        player.x += SPEED
        isWalking = True
    else:
        isWalking = False
        walkCount = 0


def main():
    player = pygame.Rect(200, HEIGHT - SPRITE_HEIGHT,SPRITE_WIDTH, SPRITE_HEIGHT)
    run = True
    isJump = False
    vel_y = 15
    isWalking = False
    
    while run:
        clock = pygame.time.Clock()
        clock.tick(FPS)
        draw_window(player, isWalking)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        keys_pressed = pygame.key.get_pressed()
        sprite_movement(keys_pressed, player, isWalking)

        if isJump == False and keys_pressed[pygame.K_UP]:
            isJump = True
        if isJump == True:
            isWalking = False
            if vel_y >= -15:
                player.y -= vel_y
                vel_y -= 1
            else:
                vel_y = 15
                isJump = False


main()