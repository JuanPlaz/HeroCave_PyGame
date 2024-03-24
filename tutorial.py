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

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)

    def __init__ (self, x, y, width, height):       #Initial player properties
        self.rect = pygame.Rect(x, y, width , height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"     #I need to know where the sprite is face to. So it will have the correct animation
        self.animation_count = 0    #The animation needs to be reseted once the sprite changes positions

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):   #In pygame coordinate 0,0 is top left corner. So to advance to the right you have to add a position
        self.x_vel = -vel       #If you wanna go left you have to substract a position. Same for Y coordinate, to go down add, to go up substract
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0


    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):    #This function will be called in every frame (in the "while run loop"), so the character will be uptaded constantly.
        self.move(self.x_vel, self.y_vel)

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)

    



def get_background(name):   #Generating the background
    image = pygame.image.load(join("assets", "Background", name))
    __, __, width, height = image.get_rect()    #width and height of the tiles. (__, __, = x and y).
    tiles = []

    for i in range(WIDTH // width + 1):     #Tiles needed in the "x" and "y" direction of the screen
        for j in range(HEIGHT // height + 1):   # 1 is added to avoid any gaps
            pos = (i * width, j * height)      #Position of (starting on) the top left hand corner of the current tile added 
            tiles.append(pos)

    return tiles, image

def draw(window, background, bg_image, player):
    for tile in background:
        window.blit(bg_image, tile)       #Drawing the background image, tile by tile

    player.draw(window)

    pygame.display.update()     #it needs to be updated to avoid old drawings on the screen

def main(window): #Event loop function
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")       #Getting the image for the background

    player = Player(100, 100, 50, 50)
    
    run = True
    while run:
        clock.tick(FPS) #Ensure game runs 60 fps

        for event in pygame.event.get():    #Loop to ensure closing game once is closed
            if event.type == pygame.QUIT:
                run = False
                break
        
        draw(window, background, bg_image, player)

    pygame.quit()
    quit()
    

if __name__ == "__main__":
    main(window)


