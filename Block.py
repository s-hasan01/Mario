# importing modules
import pygame
import random
from pygame.locals import *

pygame.init()

class Block(pygame.sprite.Sprite): # inherits from sprites class
    
    block_size = 30
    
    def __init__(self, x, y, image) -> None:
        super().__init__() 
        self.image = pygame.transform.scale(image,(self.block_size,self.block_size)) # scales the size of the image to one block size, so 30 by 30
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.dx, self.dy = 0, 0
        self.speed = 0
        
    def move(self, map_) -> None:
        raise NotImplementedError # abstract method; to be implemented in each subclass differently
 
# all subclasses inherit from parent class Block

class Brick(Block):
    
    def __init__(self, x, y, image=pygame.image.load("images/brick.png")) -> None:
        super().__init__(x,y,image)
    
    def move(self, map_) -> None:
        pass

class Goomba(Block):
    
    def __init__(self, x, y, image=pygame.image.load("images/goomba1.png")) -> None:
        super().__init__(x, y, image)
        self.image = pygame.transform.scale(self.image,(35,35))
        self.speed = random.choice([1,-1])
        self.squished = False
    
    def move(self, map_) -> None:
        if not map_.end and not map_.won:
            if not self.squished:
                self.rect.x += self.speed
                self.dx += 3
                
                # enables looped movement for Goomba enemies
                if self.dx > 70 or self.dx < -70 or self.rect.x > 600 or self.rect.x < 0:
                    self.speed *= -1
                    self.dx *= -1
    
    # adjusts the image and rectangle of Goomba, if Goomba has been squished (jumed on)    
    def squish(self) -> None:
        if not self.squished:
            self.image = pygame.transform.scale(pygame.image.load("images/goombaSquish.png"),(35,20))
            self.rect.top += 15
            self.squished = True

class Flag(Block):
    
    def __init__(self, x, y, image=pygame.image.load("images/flag.png")) -> None:
        super().__init__(x, y, image)
        self.image = pygame.transform.scale(self.image,(self.block_size,60))
    
    def move(self, map_) -> None:
        pass    

class Spikes(Block):
    
    def __init__(self, x, y, image=pygame.image.load("images/spikes.png")) -> None:
        super().__init__(x,y,image)
        self.image = pygame.transform.scale(self.image,(self.block_size,10))
    
    def move(self, map_) -> None:
        pass    

class Coin(Block):
    
    def __init__(self, x, y, image=pygame.image.load("images/coin.png")) -> None:
        
        super().__init__(x,y,image)
        self.image = pygame.transform.scale(self.image,(15,20))
        self.speed = 1
        self.rect.center = (x,y)
    
    # looped up and down movement of coins
    def move(self,map_) -> None:
        if not map_.end and not map_.won:
            self.rect.y += self.speed
            self.dy += self.speed
            if abs(self.dy) >= 7:
                self.speed *= -1

class PiranhaPlant(Block):
    
    def __init__(self, x, y, image=pygame.image.load("images/plant.png")) -> None:
        super().__init__(x,y,image)
        self.image = pygame.transform.scale(self.image,(24,40))
    
    def move(self, map_) -> None:
        pass    

class FloatingBrick(Block):
    
    def __init__(self, x, y, image=pygame.image.load("images/brick.png"),x_dir=0,y_dir=0) -> None:
        super().__init__(x, y, image)
        self.image = pygame.transform.scale(self.image,(self.block_size,15))
        self.x_dir = x_dir #
        self.y_dir = y_dir # represent which direction the movement of the object is (x direction or y direction)
        self.speed = 1
    
    def move(self, map_) -> None:
        
        # looped movement for floating bricks
        if not map_.end and not map_.won:
            self.rect.x += self.speed * self.x_dir
            self.rect.y += self.speed * self.y_dir
            self.dx += self.speed
            if abs(self.dx) >= 40:
                self.speed *= -1        