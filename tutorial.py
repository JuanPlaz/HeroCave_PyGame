import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init() #Initialize pygame module

pygame.display.set_caption("Heroe Cave") #Set the caption at the top of the window

##BG_COLOR = (255, 255, 255) #Initial Background color, no needed after setting tiles drawing 
WIDTH, HEIGHT = 950, 750
FPS = 60 #Frames per second
PLAYER_VEL = 5 #Player Velocity

window = pygame.display.set_mode((WIDTH, HEIGHT))   

def get_background(name):   #Generating the background
    image = pygame.image.load(join("assets", "Background", name))
    __, __, width, height = image.get_rect()    #width and height of the tiles. (__, __, = x and y).
    tiles = []

    for i in range(WIDTH // width + 1):     #Tiles needed in the "x" and "y" direction of the screen
        for j in range(HEIGHT // height + 1):   # 1 is added to avoid any gaps
            pos = (i * width, j * height)      #Position of (starting on) the top left hand corner of the current tile added 
            tiles.append(pos)

    return tiles, image

def draw(window, background, bg_image):
    for tile in background:
        window.blit(bg_image, tile)       #Drawing the background image, tile by tile

    pygame.display.update()     #it needs to be updated to avoid old drawings on the screen

def main(window): #Event loop function
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")       #Getting the image for the background
    
    run = True
    while run:
        clock.tick(FPS) #Ensure game runs 60 fps

        for event in pygame.event.get():    #Loop to ensure closing game once is closed
            if event.type == pygame.QUIT:
                run = False
                break
        
        draw(window, background, bg_image)

    pygame.quit()
    quit()
    

if __name__ == "__main__":
    main(window)


