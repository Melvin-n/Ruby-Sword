import pygame
import os

# define size constants
WIDTH = 600
HEIGHT = 450

FPS = 20
SPEED = 5

# color variables
WHITE = (0, 255, 255)
BLACK = (0, 0, 0)
BROWN = (100, 100, 100)
GREEN = (34, 177, 76)
SPRITE_SHEET_BG = (192, 192, 192)


SPRITE_HEIGHT = 60
SPRITE_WIDTH = 45

#isWalking = False

screen = pygame.display.set_mode((WIDTH, HEIGHT))

sprite_sheet = pygame.image.load((os.path.join('cs50-final', 'spritesheet-sword.png'))).convert_alpha()

pygame.display.set_caption('Ruby Sword')

sprite_column = 64
sprite_row = 64


def get_image(sheet, frame_row, frame_column, width, height, color):
    # create a surface the size of width and height and assign it to image
    image = pygame.Surface((width, height)).convert_alpha()
    # take the sprite sheet and only take the area starting between last param coordinates, from the row/column in the sheet
    image.blit(sheet, (0, 0), (sprite_column * frame_column, sprite_row * frame_row, width, height))
    # removes the background color of the spritesheet as per color passed in
    image.set_colorkey(color)
    return image

frame_0 = get_image(sprite_sheet, 9, 5, 64, 64, SPRITE_SHEET_BG)
print(frame_0)

def draw_window(player, isWalking):
    screen.fill(WHITE)
    screen.blit(frame_0, (200, HEIGHT - 64))
 
    pygame.display.update()


# def sprite_movement(keys_pressed, player, isWalking): 
#     #horizontal movement, make sure sprite is not past screen boundaries
    
    


def main():
    player = pygame.Rect(200, HEIGHT - SPRITE_HEIGHT,SPRITE_WIDTH, SPRITE_HEIGHT)
    run = True
    isJump = False
    vel_y = 15
    global isWalking
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
        # sprite_movement(keys_pressed, player, isWalking)
        if(keys_pressed[pygame.K_LEFT] and player.x > 0):
            isWalking = True
            player.x -= SPEED    
        if(keys_pressed[pygame.K_RIGHT] and player.x < WIDTH - SPRITE_WIDTH):
            player.x += SPEED
            isWalking = True
        else:
            isWalking = False

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