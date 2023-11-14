# import libraries
import pygame as pg
from pygame.sprite import Sprite
from pygame.math import Vector2 as vec
import os
from settings import *
from math import floor

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images') #pull images from images file

class Cooldown():
    def __init__(self):
        self.current_time = 1
        self.event_time = 0
        self.delta = 0
        # ticking ensures the timer is counting...
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)

class Player(Sprite):
    def __init__(self, game, l_control, r_control, jump_control, img_file, x, y): #controls that the player of the game uses
        Sprite.__init__(self) #pulling into sprite category
        self.game = game
        self.img_file = img_file
        self.image = pg.image.load(os.path.join(img_folder, self.img_file)).convert() 
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0) #starting point
        self.x = x
        self.y = y
        self.pos = vec(self.x, self.y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.health = 100 #gives player a health
        self.canmove = True #gives player ability to move
        self.l_control = l_control #moving left
        self.r_control = r_control #moving right
        self.jump_control = jump_control #jumping
        self.canjump = True
        self.times_jumped = 0
    def controls(self): #keys that will make the player move
        keys = pg.key.get_pressed() #when a key gets pressed, this will happen
        if self.canmove:
            if keys[self.l_control]: #when hitting the l key, player will move left
                self.acc.x = -5 #-4 to the left
                self.game.paused = False
            if keys[self.r_control]: #when hitting the r key, player will move right
                self.acc.x = 5 #+5 to the right
            if keys[self.jump_control]: #when space bar gets pressed, player will jump
                self.jump()
    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False) #when the player jumps and collides with all platforms
        ghits = pg.sprite.collide_rect(self, self.game.ground) #when the player touches the ground, sets boundary for game
        print(self.times_jumped) #counting how many times the player can jump
        if self.canjump and self.times_jumped < 3: #gives player the ability to doulbe jump since jump key can be registered less then 3 times
            self.vel.y = -PLAYER_JUMP
            self.times_jumped += 1 
        if hits: #when player hits any ground or platform 
            self.times_jumped = 0 #when player hits any ground or platform reset the jump count so player can jump again
            self.canjump = True
            if self.rect.y < hits[0].rect.y:
                print("i can jump")
                self.vel.y = -PLAYER_JUMP
        if ghits: #when player hits any ground or platform 
            self.times_jumped = 0  #when player hits any ground or platform reset the jump count so player can jump again
            self.canjump = True 
            if self.rect.y < self.game.ground.rect.y:
                print("i can jump")
                self.vel.y = -PLAYER_JUMP
    def update(self):
        # this prevents players from moving through the left side of the platforms...
        phits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        if self.vel[0] >= 0 and phits:
            if self.rect.right < phits[0].rect.left + 35:
                print("i just hit the left side of a box...") #checking when player hits left side of box
                self.vel[0] = -self.vel[0]
                self.pos.x = phits[0].rect.left - 35
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # if friction - apply here
        self.acc.x += self.vel.x * -PLAYER_FRIC
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if self.rect.x <= 0:
            self.rect.x =0
        self.rect.midbottom = self.pos
        mhits = pg.sprite.spritecollide(self, self.game.all_mobs, False) #instances for when Player collides with mobs
        xhits = pg.sprite.spritecollide(self, self.game.all_Koopas, False) #instances for when Player collides with Koopas
        
        if mhits:
            mhits[0].tagged = True #If player hits mob it marks it as tagged
            mhits[0].cd.event_time = floor((pg.time.get_ticks())/1000)
            mhits[0].image = pg.image.load(os.path.join(img_folder, "coin2.png")).convert() #When player collides with mob, a coin will appear
            mhits[0].image.set_colorkey(BLACK)
        if xhits:
            xhits[0].tagged = True #If player hit Koopa it marks it as tagged
            xhits[0].cd.event_time = floor((pg.time.get_ticks())/1000)
            xhits[0].image = pg.image.load(os.path.join(img_folder, "coin2.png")).convert() #When player collides with mob, a coin will appear
            xhits[0].image.set_colorkey(BLACK)    

# platforms

class Platform(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.category = category
        self.speed = 0
        if self.category == "moving": #if there moving in the platforms setting then...
            self.speed = 5 #it will have a speed of 5
    def update(self):
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed

class Mob(Sprite):
    def __init__(self, game, x, y, w, h, kind):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.image = pg.image.load(os.path.join(img_folder, "enemy.png")).convert() #image of Mob
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x #possible x position
        self.rect.y = y #possible y position
        self.kind = kind #parameer
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.cd = Cooldown()
        self.tagged = False
    def seeking(self): #Seeking towards player
        if self.rect.x < self.game.player.rect.x: #x position will equal that of the players
            self.rect.x +=1 
        if self.rect.x > self.game.player.rect.x: #x position will equal that of the players
            self.rect.x -=1
        if self.rect.y < self.game.player.rect.y: #y position will equal that of the players
            self.rect.y +=1
        if self.rect.y > self.game.player.rect.y: #y position will equal that of the players
            self.rect.y -=1
    def update(self):
        if self.game.player.rect.y < 850: #If the player is less then this y value then the mob will seek towards the player
            self.seeking()
        self.cd.ticking()
        if self.tagged:
            pg.transform.scale(self.image, (self.rect.w + 30, self.rect.h + 30))

        if self.cd.delta > 0.5 and self.tagged:
            self.kill()

class Koopa(Sprite):
    def __init__(self, game, x, y, w, h, kind):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.image = pg.image.load(os.path.join(img_folder, "Koopa.png")).convert() #Image of Koopa
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x #any possible x position
        self.rect.y = y #any possible y positon
        self.kind = kind #parameter
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.cd = Cooldown()
        self.tagged = False
    def seeking(self): #Seeking
        if self.rect.x < self.game.player.rect.x: #x position will equal that of the players
            self.rect.x +=1 
        if self.rect.x > self.game.player.rect.x: #x position will equal that of the players
            self.rect.x -=1
        if self.rect.y < self.game.player.rect.y: #y position will equal that of the players
            self.rect.y +=1
        if self.rect.y > self.game.player.rect.y: #y position will equal that of the players
            self.rect.y -=1
    def update(self):
        if self.game.player.rect.y < 800: #If the player is less then this y value then the mob will seek towards the player
            self.seeking()
        self.cd.ticking()
        if self.tagged:
            pg.transform.scale(self.image, (self.rect.w + 30, self.rect.h + 30))

        if self.cd.delta > 0.5 and self.tagged:
            self.kill()      
