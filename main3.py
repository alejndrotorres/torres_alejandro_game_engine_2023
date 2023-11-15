# This file was created by: Alejandro Torres
# Code from Chris Bradfield tutorials content from kids can code: http://kidscancode.org/blog/
# https://github.com/kidscancode/pygame_tutorials/tree/master/platform 

#Goals:
#Create a Mario like game that has goombas and other mob die when you hit the top of their heads
#Rules:
#Kill all the mobs on screen
#Freedom:
#Be able to move and jump freely

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *
from math import floor

vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')

class Cooldown():
    def __init__(self): 
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # ticking ensures the timer is counting...
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000) #floor
        self.delta = self.current_time - self.event_time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000) #floor

class Game: #making game
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) #physical borders of the game
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True 
        self.paused = False #if game is paused then stop showing window
        self.cd = Cooldown()
    
    def new(self):
        # create a group for all sprites
        self.bgimage = pg.image.load(os.path.join(img_folder, "Mariolevel.png")).convert() #pulls image from files
        self.score = 0
        self.all_sprites = pg.sprite.Group() #insert groups into sprites 
        self.all_platforms = pg.sprite.Group()  #insert groups into sprites
        self.all_mobs = pg.sprite.Group() #insert groups into sprites
        self.all_Koopas = pg.sprite.Group() #insert groups into sprites
        # instantiate classes
        self.player = Player(self, pg.K_a, pg.K_d, pg.K_w, "mario2.png", 30, 30) #pulls image from files
        # add instances to groups
        self.all_sprites.add(self.player)
        self.ground = Platform(*GROUND)
        self.all_sprites.add(self.ground)
        for p in PLATFORM_LIST:
            # instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)

        for m in range(0,6): #How many mobs there will be on screen
            m = Mob(self, randint(0, WIDTH), randint(0, HEIGHT/2), 20, 20, "normal") #position of mob
            self.all_sprites.add(m) #add mobs to sprites
            self.all_mobs.add(m)  #add mobs to mobs
        for x in range(0,3): #How many Koopas there will be on screen
            x = Koopa(self, randint(0, WIDTH), randint(0, HEIGHT/2), 20, 20, "normal") #position of mob
            self.all_sprites.add(x) #add koopas to sprites
            self.all_Koopas.add(x) #add koopas to koopas

        self.run() #run the following above
    
    def run(self): #when running
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def update(self):
        self.cd.ticking()
        self.all_sprites.update()
        if self.player.pos.x < 0:
            self.player.pos.x = WIDTH
        if self.player.pos.x > WIDTH:
            self.player.pos.x = 0
        
        # this is what prevents the player from falling through the platform when falling down...
        if self.player.vel.y != 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits: 
                if self.player.vel.y > 0: #If player hits the platform then they will not go below it
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
         # this prevents the player from jumping up through a platform
                elif self.player.vel.y <= 0:
                    if self.player.rect.top >= hits[0].rect.top - 5:    
                        self.player.vel.y = -self.player.vel.y
            ghits = pg.sprite.collide_rect(self.player, self.ground) #If player hits the platform from the bottom of it, then the player will not go through it
            if ghits:
                self.player.pos.y = self.ground.rect.top
                self.player.vel.y = 0

    def events(self):
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
    def draw(self):
        # draw the background screen
        self.screen.fill(BLACK)
        self.screen.blit(self.bgimage, (0,0))
        # draw all sprites
        self.draw_text("Coins: " + str(self.player.health), 22, WHITE, WIDTH/2, HEIGHT/24) #Coin appear
        self.all_sprites.draw(self.screen)
        # buffer - after drawing everything, flip display
        pg.display.flip()
    
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

g = Game()
while g.running:
    g.new()

pg.quit()
