import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init() #Initialize pygame module

pygame.display.set_caption("Heroe Cave") #Set the caption at the top of the window

BG_COLOR = (255, 255, 255) #Background color (white)
WIDTH, HEIGHT = 900, 700
FPS = 60 #Frames per second
PLAYER_VEL = 5 #Player Velocity

window = pygame.display.set_mode((WIDTH, HEIGHT))   

def main(window): #Event loop function
    clock = pygame.time.Clock()
    
    run = True
    while run:
        clock.tick(FPS) #Ensure game runs 60 fps

        for event in pygame.event.get():    #Loop to ensure closing game once is closed
            if event.type == pygame.QUIT:
                run = False
                break
    pygame.quit()
    quit()
    

if __name__ == "__main__":
    main(window)


