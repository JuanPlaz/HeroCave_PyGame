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

def flip(sprites):      #We need to flip the sprites in all the animations when they are facing left.
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]     #True, False, to split only in x axis, not in y.    

def load_sprite_sheets(dir1, dir2, width, height, direction=False):     #Directory 1 and 2 to load more images. Measures of the images, and we dont need to load multiple directions "False"
    path = join("assets", dir1, dir2)   #The path of the images we are gonna be loading
    images = [f for f in listdir(path) if isfile(join(path, f))]    #It is gonna load any file inside the path directory

    all_sprites = {}    #key will be "animation style" and the value is all of the images in that animation

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha() #Loading the sprite sheet using the path to the image, by getting the transparent background thanks to convert alpha

        sprites = []    
        for i in range(sprite_sheet.get_width() // width):  #now, we need to get all the individual images from the sprite sheets.
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)  #We need to create a "surface" where the individual animation frame will be. This should be the same size of the images (32). Then we have to "draw" our image into our surface and then, we will export that surface.
            rect = pygame.Rect(i * width, 0, width, height)  #Location of the original image that we want to grab this new frame from. 
            surface.blit(sprite_sheet, (0,0), rect) #To draw the frame i want from the sprite sheet in the surface, we need the source, the destination and the area we are gonna use.
            sprites.append(pygame.transform.scale2x(surface))   #it is gonna be 2x larger than default. So, the sprites will be 64x64.

        if direction:       #To do a multidirectional animation we have to add two keys to our dictionary as follows:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites      #This block of code will load our sprite sheets.


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES =   load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)     #We pass both directories with our character sprites, and True to be multidirectional.
    ANIMATION_DELAY = 3

    def __init__ (self, x, y, width, height):       #Initial player properties
        self.rect = pygame.Rect(x, y, width , height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"     #I need to know where the sprite is face to. So it will have the correct animation
        self.animation_count = 0    #The animation needs to be reseted once the sprite changes positions
        self.fall_count = 0

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
        #self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY )   #This is gonna be a "realistic gravity" in the game. After 1 sec (60 frames) we will see the graviity in action.        
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update_sprite()
    
    def update_sprite(self):
        sprite_sheet = "idle"   #Default sprite sheet if we are not doing anything.
        if self.x_vel != 0:        #If there is some value in x axis, we are running
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction   #We add the direction to know which exact sprite sheet we want.
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)    #It helps to use a different sprite thanks to the amount of frames happening
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()
    
    def update(self):       #This method is to update the mask to match the sprite
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)   #it allows pixel perfect collision
          

    def draw(self, win):
        #pygame.draw.rect(win, self.COLOR, self.rect)       #Line of code to draw a rectangle on the screen.
        #self.sprite = self.SPRITES["idle_" + self.direction][0]   #We have to look into the dictionary with the key and select the first frame (0).
        win.blit(self.sprite, (self.rect.x, self.rect.y))   #To draw in the position of the screen

    
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

def handle_move(player):
    keys = pygame.key.get_pressed()     #This will catch the key you are pressing in the keyboard

    player.x_vel = 0                    #You need to set the vel on 0, or character will keep moving even if you are not pressing any key.
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)

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
        
        player.loop(FPS)        #We need to call loop function to keep moving in every frame
        handle_move(player)
        draw(window, background, bg_image, player)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)


