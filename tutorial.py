import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init() #Initialize pygame module

pygame.display.set_caption("Heroe Cave") #Set the caption at the top of the window

##BG_COLOR = (255, 255, 255) #Initial Background color, no needed after setting tiles drawing 
WIDTH, HEIGHT = 900, 750
FPS = 60 #Frames per second
PLAYER_VEL = 5 #Player Velocity

window = pygame.display.set_mode((WIDTH, HEIGHT))   

def flip(sprites):      #To flip the sprites in all the animations when they are facing left.
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]     #True, False, to split only in x axis, not in y.    

def load_sprite_sheets(dir1, dir2, width, height, direction=False):     #Directory 1 and 2 to load more images. Measures of the images, and we dont need to load multiple directions "False"
    path = join("assets", dir1, dir2)   #The path of the images to be loading
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

    return all_sprites      #This previous block of code will load our sprite sheets.

def get_block(size):        #Getting the sprites of the block from our files, we decide the size.
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()     #We get a transparent background
    surface = pygame.Surface((size, size),pygame.SRCALPHA, 32)  #To create an image of the size of the block
    rect = pygame.Rect(96, 0, size, size)       #(96,0) is the position that I want to load the image from in the selected sprite sheet.
    surface.blit(image, (0,0), rect)        #To take the image from the path and draw it on the position 0,0 of the background (using the rect one).

    return pygame.transform.scale2x(surface)


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES =   load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)   #We pass both directories with our character sprites, and True to be multidirectional.
    ANIMATION_DELAY = 3

    def __init__ (self, x, y, width, height):       #Initial player properties
        super().__init__()
        self.rect = pygame.Rect(x, y, width , height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"     #I need to know where the sprite is face to. So it will have the correct animation
        self.animation_count = 0    #The animation needs to be reseted once the sprite changes positions
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * 8      #it is negative to substract from Y axis and jump in the air. Then, gravity will take player down.
        self.animation_count = 0            #reset the animation in the sprite sheet
        self.jump_count += 1                #variable to allow a double jump
        if self.jump_count == 1:            #If player jumped in a range of 1 second after,
            self.fall_count = 0             #Gravity is reseted.
        
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True
        self.hit_count = 0

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
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY )   #This is gonna be a "realistic gravity" in the game. After 1 sec (60 frames) we will see the graviity in action.        
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:        #This would be 2 seconds.
            self.hit = False

        self.fall_count += 1
        self.update_sprite()
    
    def landed(self):
        self.fall_count = 0     #Usefull to stop adding gravity
        self.y_vel = 0          #If landed on a block, stop moving the player down
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1    #It will make bouncing off when hitting an object.

    def update_sprite(self):
        sprite_sheet = "idle"   #Default sprite sheet if we are not doing anything.

        if self.hit:
            sprite_sheet = "hit" 
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:     #Patch to avoid glitching between the 2 states, falling, and idle.
            sprite_sheet = "fall"
        elif self.x_vel != 0:        #If there is some value in x axis, we are running
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction   #We add the direction to know which exact sprite sheet we want.
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)    #It helps to use a different sprite thanks to the amount of frames happening
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()
    
    def update(self):       #This method is to update the mask to match the sprite and allows to have a perfect collision.
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)   #it allows pixel perfect collision, not rectangle collision.
          
    def draw(self, win, offset_x):
        #pygame.draw.rect(win, self.COLOR, self.rect)       #Line of code to draw a rectangle on the screen.
        #self.sprite = self.SPRITES["idle_" + self.direction][0]   #We have to look into the dictionary with the key and select the first frame (0).
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))   #To draw in the position of the screen

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)   #Helps support transparent images
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image)

class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]        #0 is first sprite in the sprite sheet "off"
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"
    
    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]        #Get the sprite sheet of fire
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)    #It helps to use a different sprite thanks to the amount of frames happening
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))    #updating the rect
        self.mask = pygame.mask.from_surface(self.image)   #it allows pixel perfect collision, not rectangle collision.
        
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):     #"animation_count" needs to be reset to avoid unstoppable increase of the value and lagging the game
            self.animation_count = 0 


def get_background(name):   #Generating the background
    image = pygame.image.load(join("assets", "Background", name))
    __, __, width, height = image.get_rect()    #width and height of the tiles. (__, __, = x and y).
    tiles = []

    for i in range(WIDTH // width + 1):     #Tiles needed in the "x" and "y" direction of the screen
        for j in range(HEIGHT // height + 1):   # 1 is added to avoid any gaps
            pos = (i * width, j * height)      #Position of (starting on) the top left hand corner of the current tile added 
            tiles.append(pos)

    return tiles, image

def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)       #Drawing the background image, tile by tile
    
    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)
    pygame.display.update()     #it needs to be updated to avoid old drawings on the screen

def handle_vertical_collision(player, objects, dy):
    collide_objetcs = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj): #This will tell if the objects are colliding
            if dy > 0:      #if displacement greater than 0 (player is falling) 
                player.rect.bottom = obj.rect.top   #Do the feet player position, the top of the object player is colling with.
                player.landed() #To land on a block
            elif dy < 0:    #if displacement smaller than 0 (player is jumping) 
                player.rect.top = obj.rect.bottom   #Do the top of player position, the bottom of the object player is colliding with.
                player.hit_head()   #To hit a block
        
            collide_objetcs.append(obj)
    
    return collide_objetcs

def collide(player, objects, dx):
    player.move(dx, 0)          #Move the player
    player.update()             #Updating the mask
    collided_object = None
    for obj in objects:         #Checking if the player will collide with something,
        if pygame.sprite.collide_mask(player, obj): #If it will move in that direction 
            collided_object = obj
            break
    
    player.move(-dx, 0)     #player is moved back to the previous position. This is to prevent to move into the block.
    player.update()         #update the mask again
    return collided_object

def handle_move(player, objects):
    keys = pygame.key.get_pressed()     #This will catch the key you are pressing in the keyboard

    player.x_vel = 0                    #You need to set the vel on 0, or character will keep moving even if you are not pressing any key.
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:    #Checking is player is able to move left based on current position
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:  #Checking is player is able to move rigth
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_right, collide_left, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()


def main(window): #Event loop function
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")       #Getting the image for the background

    block_size = 96

    player = Player(100, 100, 50, 50)
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)  #The last 16, and 32 are the dimensions of the single sprite. Remember "y" axis is positive by going down, and negative going up.
    fire.on()
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
                #X coordinate position, Bottom of the screen
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
                           #Amount of left blocks,  rigth blocks on the floor 
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * 3, HEIGHT - block_size * 4, block_size), fire]
    
    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS) #Ensure game runs 60 fps

        for event in pygame.event.get():    #Loop to ensure closing game once is closed
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:        #Event of pressing and releasing a key in the keyboard.
                if event.key == pygame.K_SPACE and player.jump_count < 2:   #Allows double jumping
                    player.jump()

        
        player.loop(FPS)        #We need to call loop function to keep moving in every frame
        fire.loop()
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (  #setting the offset, once the player is close to a boundary, the system will redraw allthe objects on a new position
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)


