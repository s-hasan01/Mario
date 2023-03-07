import pygame
from Map import Map
from Grids import grids
from Player import Player
from Button import Button
from pygame.locals import *

pygame.init()

# Function used for blitting text onto the screen
def display_text(text: str, size, x: int, y: int) -> None:
    pygame.font.init()
    font = pygame.font.SysFont('Nirmala UI', size)
    textsurface = font.render(text, False, (255, 255, 255))
    screen.blit(textsurface,(x,y))

clock = pygame.time.Clock() # the pygame clock
fps = 60
width, height = 600,600
screen = pygame.display.set_mode((width,height)) # creates a 600 x 600 screen
pygame.display.set_caption("B-Tech Mario") # sets the window caption

# loading and scaling all the display images
bg = pygame.image.load("images/bg1.png")
title = pygame.transform.scale(pygame.image.load("images/title.png"),(420,180))
you_lose = pygame.transform.scale(pygame.image.load("images/lose.png"),(300,100))
you_win = pygame.transform.scale(pygame.image.load("images/win.png"),(300,100))
start = Button(50,height//2+120,pygame.transform.scale(pygame.image.load("images/start.png"),(80,30)))
again = Button(50,height//2+120,pygame.transform.scale(pygame.image.load("images/again.png"),(80,30)))

# initializing important variables for game control
level = 0
grid_data = grids[level]
start_game = False
map_ = Map(grid_data)
player = Player(50,height-90)


run = True
while run:
    clock.tick(fps) # starts the pygame clock
    screen.blit(bg,(0,0)) # blits the background image
    
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # displays the title screen until the user has pressed start button
    if not start_game:
        screen.blit(title,(20,140))
        start.draw(screen)
        if start.click():
            start_game = True
        
    else:
        # draws sprite objects in their respective positions on the grid
        map_.draw(screen)
        map_.enemies.draw(screen)
        map_.flags.draw(screen)
        map_.die.draw(screen)
        map_.coins.draw(screen)
        display_text(f"Coins: {player.coins}", 15, 540,550)
        display_text(f"Level: {level+1}", 15, 540,570)
        
        # creates movement for blocks, enemies and coins
        for block in map_.blocks:
            block[2].move(map_)
        for enemy in map_.enemies:
            enemy.move(map_)
        for coin in map_.coins:
            coin.move(map_)
        
        # handles the players movement and interaction based on the keys pressed
        player.move(screen,map_,key)
        
        # if user has reached the flag without dying
        # increments the level, and generates the new map and resets player
        if map_.won:
            if level <= 2:
                level += 1
                coins = player.coins
                grid_data = grids[level]
                player.restart(50,height-90,coins)
                map_.restart(grid_data)
            
            # if the user has passed all levels successfully
            # displays a win message
            # asks user if they want to start again from level 1
            else:
                screen.blit(you_win,(20,240))
                display_text(f"Would you Like to Play Again?", 22, 35,370)
                again.draw(screen)
                if again.click():
                    level = 0
                    grid_data = grids[level] # resets the grid to level 1 
                    player.restart(50,height-90) # resets player
                    map_.restart(grid_data) # resets map
        
        # if the user dies in the current level
        # prints a lose message
        elif map_.end:
            screen.blit(you_lose,(20,240))
            display_text(f"Would you Like to Restart the Level?", 22, 35,370)
            again.draw(screen)
            
            # if user decides to play again
            if again.click():
                player.restart(50,height-90) # resets player
                map_.restart(grid_data) # resets map
    
    pygame.display.update()

pygame.quit()