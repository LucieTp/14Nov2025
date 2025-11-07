# /// script
# dependencies = [
# "numpy",
# "pygame",
# "pyscroll",
# "pytmx",
# ]
# ///

import pygame
from Game import Game
import asyncio # used for pygbag


async def main():
    pygame.init()
    game = Game()

    running = True
    while running:

        if game.is_playing:
            await game.run()
            await asyncio.sleep(0) # these are the commands for pygbag
        else:
            await game.intro()
            await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
