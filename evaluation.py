import pygame, random, math
import numpy as np
import _2048
from _2048.game import Game2048
from _2048.manager import GameManager

# define evenets for movements
EVENTS = [ pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP}),
           pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT}),
           pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}),
           pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})]
