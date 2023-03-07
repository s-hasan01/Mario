import pygame
from Block import *
from pygame.locals import *

pygame.init()

class Map():
    def __init__(self, grid_data) -> None:
        self.blocks = []
        block_size = 30
        self.end = False
        self.won = False
        self.coins = pygame.sprite.Group() # sprite group of all the coins in a map
        self.enemies = pygame.sprite.Group() # group of all enemies in a map
        self.die = pygame.sprite.Group() # group of all things that kill the player by a single touch in the map
        self.flags = pygame.sprite.Group() # group of all the flags in the map (one per map)
        
        # iterates through all rows, columns of the grid
        # creating the appropriate block, depending on the integer in the grid
        rows = 0
        for row in grid_data:
            columns = 0
            for block in row:
                if block == 1:
                    brick = Brick(columns*block_size,rows*block_size)
                    block = (brick.image,brick.rect,brick)
                    self.blocks.append(block)
                if block == 2:
                    goomba = Goomba(columns*block_size,rows*block_size-5)
                    self.enemies.add(goomba)
                if block == 3:
                    flag = Flag(columns*block_size,rows*block_size-30)
                    self.flags.add(flag)
                if block == 4:
                    spikes = Spikes(columns*block_size,rows*block_size+20)
                    self.die.add(spikes)
                if block == 5:
                    coin = Coin(columns*block_size+20,rows*block_size)
                    self.coins.add(coin)
                if block == 6:
                    plant = PiranhaPlant(columns*block_size,rows*block_size-10)
                    self.die.add(plant)
                if block == 7:
                    float_brick = FloatingBrick(columns*block_size,rows*block_size,x_dir=1,y_dir=0)
                    block = (float_brick.image,float_brick.rect,float_brick)
                    self.blocks.append(block)
                if block == 8:
                    float_brick = FloatingBrick(columns*block_size,rows*block_size,x_dir=0,y_dir=1)
                    block = (float_brick.image,float_brick.rect,float_brick)
                    self.blocks.append(block)                
                columns += 1
            rows += 1
    
    # method for drawing blocks onto the grid
    def draw(self, screen) -> None:
        for block in self.blocks:
            screen.blit(block[0],block[1]) #block[0] is the image, block[1] is the rect
    
    # resets the player by calling the initializer again
    def restart(self,grid_data) -> None:
        self.__init__(grid_data)