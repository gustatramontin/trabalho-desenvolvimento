import pygame
from pygame.locals import *

from minigames.interface import Interface
from minigames.snake import Snake
from minigames.obstacles import Obstacles
from minigames.velha import Velha
from minigames.paint import Paint
from minigames.shapes import Shapes

import cv2

pygame.init()

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Mini-Jeux")

CAP = cv2.VideoCapture(0)


clock = pygame.time.Clock()

def switch_game(game):
    global gameRunning
    if game in games.keys():
        gameRunning = game

games = {
    "interface": Interface(pygame, screen, clock, switch_game),
    "snake": Snake(pygame, screen, clock, CAP, switch_game),
    "obstacles": Obstacles(pygame, screen, clock, CAP),
    "velha": Velha(pygame, screen, clock),
    "paint": Paint(pygame, screen, clock, CAP),
    "shapes": Shapes(pygame, screen, clock)
}

gameRunning = "interface"

running = True
is_key_pressed = False
pressed_key = None
mouse_position = None

while running:

    time_delta = clock.tick(15) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            games[gameRunning].stop()
            running = False
        if event.type == KEYDOWN:
            pressed_key = pygame.key.name(event.key)
            is_key_pressed = True

            if (pressed_key == 'q'):
                if gameRunning != "interface":
                    switch_game("interface")
                else:
                    running = False

        if event.type == pygame.MOUSEMOTION:
            mouse_position = pygame.mouse.get_pos()

        if games[gameRunning].hasCustomEvent:
            games[gameRunning].customEvent(event)

        #ui_manager.process_events(event)
    
    screen.fill(WHITE)
    """
    pygame.draw.rect(screen, RED, [55, 200, 100, 70],0)
    pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)
    pygame.draw.ellipse(screen, BLACK, [20,20,250,100], 2)
    """

    games[gameRunning].run(pressed_key, mouse_position)

    """
    if gameRunning == "interface":
        ui_manager.update(time_delta)
        ui_manager.draw_ui(screen)
    """

    pygame.display.flip()

    pressed_key = None
    mouse_position = None

     
pygame.quit()
