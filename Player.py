import pygame
from Block import *
from pygame.locals import *

pygame.init()

class Player():
    
    def __init__(self,x,y,coins=0) -> None:
        self.right_pics = []
        self.left_pics = []
        self.jump_pics = []
        self.jump_pics.append(pygame.transform.scale(pygame.image.load(f"images/marioRJ.png"),(25,50))) # 
        self.jump_pics.append(pygame.transform.scale(pygame.image.load(f"images/marioLJ.png"),(25,50))) # loads in sprites for jumping
        self.index = 0
        self.frame_count = 0
        
        # loads in all images for running motion (facing left and facing right)
        for pic in range(1,5):
            image_R = pygame.image.load(f"images/marioR{pic}.png")
            image_R = pygame.transform.scale(image_R,(25,50))
            image_L = pygame.image.load(f"images/marioL{pic}.png")
            image_L = pygame.transform.scale(image_L,(25,50))
            self.right_pics.append(image_R)
            self.left_pics.append(image_L)  
        self.image = self.right_pics[self.index] # sets the starting image 
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.x_speed, self.y_speed = 0, 0
        self.direction = 1 # represents the direction the player is facing (1 is right, -1 is left)
        self.jumped = False 
        self.on_ground = True # checks if the player is on ground (on a block)
        self.coins = coins
    
    def move(self, screen, map_, key) -> None:
        dx = 0
        dy = 0
        
        if not map_.won and not map_.end: # runs as long as player hasnt reached flag or player has died
            
            # runs when user presses space key
            # players single jump is recorded
            if key[pygame.K_SPACE] and self.jumped == False:
                if self.on_ground:
                    self.y_speed -= 42
                    self.jumped = True
                    self.on_ground = False
                    
            # sets jump back to False when player lands on a block again
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            
            if key[pygame.K_LEFT]:
                self.frame_count += 1
                dx -= 3 # my computer is quite slow, so 5 seemed slow but is a little fast on a faster laptop. If its running a little fas on your computer, feel free to change this when grading
                self.direction = -1
            if key[pygame.K_RIGHT]:
                self.frame_count += 1
                dx += 3 # my computer is quite slow, so 5 seemed slow but is a little fast on a faster laptop. If its running a little fas on your computer, feel free to change this when grading
                self.direction = 1
            
            # sets the images back to still when the player is not running
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.frame_count = 0
                if self.direction == 1:
                    self.image = self.right_pics[0]
                else:
                    self.image = self.left_pics[0]
            
            # creates a bit of frame delay, so movement sprites dont play so fast
            # delay of 3 frames
            if self.frame_count > 2:
                self.index += 1
                if self.index >= len(self.right_pics): # creates a cycle oif images
                    self.index = 1 
                if self.direction == 1: 
                    self.image = self.right_pics[self.index]
                    if self.jumped:
                        self.image = self.jump_pics[0]
                else:
                    self.image = self.left_pics[self.index]
                    if self.jumped:
                        self.image = self.jump_pics[1]
                self.frame_count = 0
            
            # creates the effect of gravity
            self.y_speed += 6 #
            if self.y_speed > 10: # These values for gravity work well for mine, but may be a little fast for your computer
                self.y_speed = 10 # Edit them if that's the case
            dy += self.y_speed
            
            for block in map_.blocks:
                if block[1].colliderect(self.rect.x+dx, self.rect.y,
                                        self.image.get_width(),self.image.get_height()): #checks for collision between player and block, in the x axis
                    
                    if not isinstance(block[2], FloatingBrick): 
                        dx = 0

                if block[1].colliderect(self.rect.x, self.rect.y+dy,
                                        self.image.get_width(),self.image.get_height()): # checks for collition with block in the y axis
                    
                    if self.y_speed < 0: # checks for collision with block from above the player
                        dy = block[1].bottom - self.rect.top
                        self.y_speed = 0 # creates a bounce back effect
                        
                    elif self.y_speed >= 0: # checks for collision with block from below the player
                        dy = block[1].top - self.rect.bottom
                        self.on_ground = True # since player is standing on the block, on_ground is True again 
                        
                        if not isinstance(block[2], Brick): # checks if the player is standing on a moving surface
                            self.rect.x += block[2].speed*block[2].x_dir # moves along with the moving surface
                        else:
                            self.rect.x += block[2].speed # is 0 for stationary blocks
                        self.y_speed = 0     
            
            # checks if the player has collided with the flag           
            if pygame.sprite.spritecollide(self, map_.flags, False):
                map_.won = True # user has won in this map
            
            # checks if the user has collided with any coins
            elif pygame.sprite.spritecollide(self, map_.coins, True):
                self.coins += 1 # coin counter goes up, and coin disappears once it's collected
            
            # checks to see if the user has collided with any insta kill blocks (plant, spikes)
            elif pygame.sprite.spritecollide(self, map_.die, False):
                map_.end = True # user has lost the level
            
            # checks to see if the user has collided with any goombas
            elif pygame.sprite.spritecollide(self, map_.enemies, False):
                for enemy in map_.enemies:
                    if not enemy.squished: # only interacts with the goomba if it is not squished
                        if enemy.rect.colliderect(self.rect.x, self.rect.y+dy,
                                                  self.image.get_width(),self.image.get_height()):
                            
                            # checks if the player has jumped onto the enemy, in which case the goomba is squished
                            if self.rect.bottom < enemy.rect.bottom:
                                enemy.squish()
                                self.on_ground = False
                                dy = enemy.rect.top - self.rect.bottom
                                
                                # creates a bit of a bounce effect when squsihed
                                self.y_speed = 0
                                for x in range(8):
                                    self.y_speed -= x
                        
                        # checks if the user has collided with the goomba, but whislt on the ground
                        if ((self.rect.x < enemy.rect.left and self.rect.right >= enemy.rect.left) or 
                            (self.rect.left > enemy.rect.left and self.rect.left <= enemy.rect.right)) and self.on_ground:
                            map_.end = True # the player cannot collide with the goomba from the side, so they're dead
                
                
            # makes sure the user stays within the bounds of the screen
            if self.rect.right + dx > screen.get_width() or self.rect.x + dx < 0:
                dx = 0
            if self.rect.y + dy < 0:
                dy = 0 - self.rect.top
                self.y_speed = 0
            if self.y_speed > 0:
                self.on_ground = False
            
            # makes changes to the players' position based on dx, dy
            self.rect.x += dx
            self.rect.y += dy
        
        # if the user has died, changes the image to the death image of mario
        elif map_.end:
            self.image = pygame.transform.scale(pygame.image.load("images/mario death.png"),(35,35))
        
        screen.blit(self.image,self.rect)
    
    # re-initializes the player (used for restart)
    def restart(self,x,y,coins=0) -> None:
        self.__init__(x,y,coins)