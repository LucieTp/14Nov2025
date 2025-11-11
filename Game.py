import pygame
import pytmx
import pyscroll
import asyncio

from Jellyfish import Jellyfish
from Player import Player
from Hoops import Hoop
from Timer import Timer
from Walls import Wall


class Game:
    def __init__(self):

        # tells us if the player has pressed play yet or not
        self.is_playing = False

        self.timer = Timer(73000) # 80 secs

        # create game window
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Road to 28')

        # import map
        tmx_data = pytmx.util_pygame.load_pygame("assets/maps/cake_map.tmx", pixelalpha=True)
        map_data = pyscroll.TiledMapData(tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 2 # zoom x 2

        self.map_width = tmx_data.width * tmx_data.tilewidth
        self.map_height = tmx_data.height * tmx_data.tileheight


        # make player group
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # hoop positions
        self.all_hoops = pygame.sprite.Group()
        hoop_width = 100
        hoop_height = 100

        for obj in tmx_data.objects:
            if obj.name == "Hoop":
                hoop = Hoop(name = "Hoops", x = obj.x, y = obj.y,
                            id = obj.id, width = hoop_width, height = hoop_height, nb_animations = 9)
                self.all_hoops.add(hoop)

        self.all_jellyfish = pygame.sprite.Group()
        jelly_width = 57
        jelly_height = 50
        for obj in tmx_data.objects:
            if obj.name == "Jellyfish":
                jellyfish = Jellyfish(name = "Jellyfish", x = obj.x, y = obj.y,
                            id = obj.id, width = jelly_width, height = jelly_height, nb_animations = 8)
                self.all_jellyfish.add(jellyfish)


        # boundary rectangles
        self.all_walls = pygame.sprite.Group()

        for obj in tmx_data.objects:
            if obj.name in ["Boundary", "Tree", "Jellyfish"]:
                wall = Wall(obj.x, obj.y, obj.width, obj.height)
                self.all_walls.add(wall)

        # make layer group (choose active layer so that the player doesn't end up under the background)
        self.group = pyscroll.PyscrollGroup(self.map_layer, default_layer=3)
        self.group.add(self.player)
        for hoop in self.all_hoops:
            self.group.add(hoop)
        for jellyfish in self.all_jellyfish:
            self.group.add(jellyfish)

        self.total_hoops = len(self.all_hoops) # nb of hoops

    async def intro(self):

        image = pygame.image.load("assets/maps/Intro.png")
        clock = pygame.time.Clock()
        running = True

        while running:

            # Draw map
            self.screen.blit(image, (0, 0))
            pygame.display.flip()
            clock.tick(60) # keep display showing

            for event in pygame.event.get():
                # allow to exit if needed
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                # click play button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = 250.165 # got these coordinates by printing obj.x etc
                    y = 352.345
                    w = 318.872
                    h = 167.364

                    # 250.165 352.345 318.872 167.364
                    button = pygame.Rect(x, y, w, h)
                    if button.collidepoint(event.pos):
                        self.is_playing = True # start the game
                        running = False # stop the display loop

            await asyncio.sleep(0)


    def handle_input(self):
        pressed = pygame.key.get_pressed()
        player_rect = self.player.rect  # assuming your player has a rect

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_orientation("up")
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_orientation("down")
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_orientation("left")
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_orientation("right")



    def draw_progress_bar(self):

        # Constants
        bar_color = (111, 210, 46)
        bar_border_color = (255, 255, 255)
        bar_position = (10, 60)  # top-left corner
        bar_size = (200, 20)  # width, height

        # Compute progress
        hoops_remaining = len(self.all_hoops)
        progress = 1 - (hoops_remaining / self.total_hoops)  # fraction completed

        # Draw background (empty bar)
        pygame.draw.rect(self.screen, bar_border_color, (*bar_position, *bar_size), 2)

        # Draw filled portion
        filled_width = int(bar_size[0] * progress)
        pygame.draw.rect(self.screen, bar_color, (bar_position[0], bar_position[1], filled_width, bar_size[1]))

    async def zoom_out(self, map_width, map_height, target_zoom=0.45, duration=1500):
        """Smoothly zoom out over time (in ms)"""

        start_zoom = self.map_layer.zoom
        start_time = pygame.time.get_ticks()

        while True:
            elapsed = pygame.time.get_ticks() - start_time
            t = min(elapsed / duration, 1.0)  # 0 → 1 over 'duration'
            current_zoom = start_zoom + (target_zoom - start_zoom) * t
            self.map_layer.zoom = current_zoom

            # Recenter on map center instead of player
            center_x = self.map_layer.map_rect.width / 2
            center_y = self.map_layer.map_rect.height / 2
            self.group.center((center_x, center_y))

            # Redraw
            self.group.draw(self.screen)
            pygame.display.flip()
            await asyncio.sleep(0)

            if t >= 1.0:
                break

            pygame.time.Clock().tick(60)

        # once zoomed out, we plot the track
        await self.player.plot_track(map_width, map_height, self.screen)

    async def check_progress(self, map_width, map_height):
        # this is the function that puts an end to the game when all hoops have been crossed
        if len(self.all_hoops) == 0:

            self.timer.pause()
            await self.zoom_out(map_width, map_height)
            self.timer.deactivate()


    def update(self):
        self.group.update()

        # make sure only one hoop is animated (the next one that will need to be crossed)
        if self.all_hoops:
            # Find the hoop with the smallest ID
            min_nb = min(hoop.number for hoop in self.all_hoops)

            # Activate only that hoop
            for hoop in self.all_hoops:
                hoop.is_active = (hoop.number == min_nb)

        # check boundary (for player only)
        collided_jellyfish = pygame.sprite.spritecollideany(self.player, self.all_jellyfish)
        collided_walls = pygame.sprite.spritecollideany(self.player, self.all_walls)

        if collided_jellyfish or collided_walls:
            self.player.move_back()

        # Detect collision between player and any hoop
        collided_hoop = pygame.sprite.spritecollideany(self.player, self.all_hoops)

        if collided_hoop:
            min_nb =  min(hoop.number for hoop in self.all_hoops) # this gives the order in which hoops should be crossed
            if collided_hoop.number == min_nb:
                self.all_hoops.remove(collided_hoop) # remove hoop from pyscroll all_hoops
                self.group.remove(collided_hoop)  # remove hoop from pyscroll group

    async def run(self):

        clock = pygame.time.Clock()

        # boucle de jeu
        running = True # keep it running until the player presses exit
        self.timer.activate()

        while running:

            self.timer.update()
            self.player.save_location() # save location to handle collisions
            self.handle_input() # to detect keys pressed
            self.update()
            self.group.update()
            self.group.center(self.player.rect) # make sure it zooms on the player
            self.player.save_track(self.timer.get_time_left())
            # draw elements on screen
            self.group.draw(self.screen)
            self.timer.display_timer(self.screen)
            self.draw_progress_bar()
            await self.check_progress(self.map_width, self.map_height)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: # if press exit on window
                    pygame.quit()
                    raise SystemExit

            # game over
            if not self.timer.active:
                self.timer.game_over(self.screen)
                pygame.display.flip()
                pygame.time.delay(2000)  # pause for 2 seconds
                self.is_playing = False
                pygame.quit()
                raise SystemExit

            await asyncio.sleep(0)

            clock.tick(60) # 60 images/sec

        pygame.quit()