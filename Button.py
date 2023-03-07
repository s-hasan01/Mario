import pygame
from pygame.locals import *

pygame.init()

class Button():
    def __init__(self, x, y, image) -> None:
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.once = True
    
    def draw(self, screen) -> None:
        screen.blit(self.image,self.rect)
    
    def click(self) -> bool:
        mouse = pygame.mouse.get_pos() # gets the position of the cursor on the screen
        clicked = False # clicked is initially false
        
        if self.rect.collidepoint(mouse): # if the position of the mouse is over the button
            if pygame.mouse.get_pressed()[0]: # if the user has left clicked
                self.once = True
                clicked = True
        
        # clicked is set back to false once the button has been clicked
        if not pygame.mouse.get_pressed()[0] and self.once:
            self.once = False

        return clicked