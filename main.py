import pygame
from pygame.locals import *

from minigames.interface import Interface
from minigames.snake import Snake
from minigames.velha import Velha

pygame.init()

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My First Game")

clock = pygame.time.Clock()

games = {
    "interface": Interface(pygame, screen, clock),
    "snake": Snake(pygame, screen, clock),
    "velha": Velha(pygame, screen, clock)
}

gameRunning = "velha"

running = True
is_key_pressed = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        if event.type == KEYDOWN:
            pressed_key = pygame.key.name(event.key)
            is_key_pressed = True
            print(pressed_key)
    
    screen.fill(WHITE)
    """
    pygame.draw.rect(screen, RED, [55, 200, 100, 70],0)
    pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)
    pygame.draw.ellipse(screen, BLACK, [20,20,250,100], 2)
    """

    games[gameRunning].run()

    pygame.display.flip()

    clock.tick(60)

     
pygame.quit()
