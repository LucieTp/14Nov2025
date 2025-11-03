import pygame
from Game import Game

if __name__ == '__main__':
    pygame.init()
    game = Game()

    running = True
    while running:

        if game.is_playing:
            game.run()
        else:
            game.intro()
