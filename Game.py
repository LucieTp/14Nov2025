import pygame
import pytmx
import pyscroll

from Player import Player
from Hoops import Hoop

class Game:
    def __init__(self):
        # create game window
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Objectif 28')

        # import map
        tmx_data = pytmx.util_pygame.load_pygame("maps/map.tmx")
        map_data = pyscroll.TiledMapData(tmx_data)
        map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2 # zoom x 2

        # make player group
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # hoop positions
        self.all_hoops = pygame.sprite.Group()

        for obj in tmx_data.objects:
            if obj.name == "Hoop":
                print(obj.id)
                hoop = Hoop(obj.x, obj.y, obj.id)
                self.all_hoops.add(hoop)



        # boundary rectangles
        self.walls = []

        for obj in tmx_data.objects:
            if obj.name == "boundary":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # make layer group (choose active layer so that the player doesn't end up under the background)
        self.group = pyscroll.PyscrollGroup(map_layer, default_layer=1)
        self.group.add(self.player)
        for hoop in self.all_hoops:
            self.group.add(hoop)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

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

    def update(self):
        self.group.update()

        # check boundary (for player only)
        if self.player.feet.collidelist(self.walls) > -1:
            self.player.move_back()

        # Detect collision between player and any hoop
        collided_hoop = pygame.sprite.spritecollideany(self.player, self.all_hoops)

        if collided_hoop:
            min_nb =  min(hoop.number for hoop in self.all_hoops) # this gives the order in which hoops should be crossed
            if collided_hoop.number == min_nb:
                self.all_hoops.remove(collided_hoop) # remove hoop from pyscroll all_hoops
                self.group.remove(collided_hoop)  # remove hoop from pyscroll group

    def run(self):

        clock = pygame.time.Clock()

        # boucle de jeu
        running = True # keep it running until the player presses exit

        while running:

            self.player.save_location() # save location to handle collisions
            self.handle_input() # to detect keys pressed
            self.update()
            self.group.update()
            self.group.center(self.player.rect) # make sure it zooms on the player
            self.group.draw(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: # if press exit on window
                    running = False

            clock.tick(60) # 60 images/sec

        pygame.quit()