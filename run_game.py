import pygame, os, time
from copy import deepcopy
import numpy as np
from pprint import pprint
import _2048
from _2048.game import Game2048
from _2048.manager import GameManager

import evaluation as ev

def run_game(game_class=Game2048, title='2048!', data_dir='save'):
  pygame.init()
  pygame.display.set_caption(title)
  pygame.display.set_icon(game_class.icon(32))
  clock = pygame.time.Clock()

  os.makedirs(data_dir, exist_ok=True)

  screen = pygame.display.set_mode((game_class.WIDTH, game_class.HEIGHT))
  manager = GameManager(Game2048, screen,
              os.path.join(data_dir, '2048.score'),
              os.path.join(data_dir, '2048.%d.state'))

  # game loop
  counter = 0
  running = True

  while running:
      clock.tick(100)
      counter += 1

      if counter % 5 == 0:
          new_grid = deepcopy(manager.game.grid)

          best_direction, best_score = ev.maximize(new_grid)

          if best_direction is None:
              print('Oooops!!! Maximum number made is %s' % np.max(manager.game.grid))
              break

          e = ev.EVENTS[best_direction]
          manager.dispatch(e)

      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              running = False
          elif event.type == pygame.MOUSEBUTTONUP:
              manager.dispatch(event)

      manager.draw()

  pygame.quit()
  manager.close()

run_game()
