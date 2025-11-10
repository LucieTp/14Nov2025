import pygame
import asyncio

from animation import AnimateSprite


class Player(AnimateSprite):

    def __init__(self, x, y):

        super().__init__("Hamtaro1", 32, 27, 4) # here we initiate all the variables associated with player (self.blabla)
        self.sprite_sheet = pygame.image.load("assets/objects/Hamtaro1.png")

        self.rect_height = 27
        self.rect_width = 32

        self.image = self.get_image_player(0,0, self.rect_width, self.rect_height) # say where the image is in the png file
        self.image.set_colorkey((0,0,0)) # remove background
        self.rect = self.image.get_rect() # create image rectangle
        self.position = [x, y] # player position

        self.feet = pygame.Rect(0,0, self.rect.width * 0.5, 12) # feet location for collisions
        self.old_position = self.position.copy() # keep in record the old position to replace the player in case of collision
        self.speed = 3 # number of pixels the player moves in one press
        self.track = {"time":[], "x":[], "y":[]} # where we will save timestep, x and y coords
        self.last_save_time = 0

    # then we create functions which take the variables as input and
    # changes their values
    def save_location(self): self.old_position = self.position.copy()

    def move_right(self): self.position[0] += self.speed
    def move_left(self): self.position[0] -= self.speed
    def move_up(self): self.position[1] -= self.speed
    def move_down(self): self.position[1] += self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position # replace player if it hits a boundary
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image_player(self, x, y, width, height):
        image = pygame.Surface([width, height])
        image.blit(self.sprite_sheet, (0,0), (x,y,width,height))
        return image

    def save_track(self, time):

        # only save every half a second
        current_time = pygame.time.get_ticks()  # in milliseconds
        if current_time - self.last_save_time >= 200:  # 200 ms = 0.2 sec
            self.last_save_time = current_time

            self.track["time"].append(current_time / 1000)
            self.track["x"].append(self.position[0])
            self.track["y"].append(self.position[1])


    async def plot_track(self, map_width, map_height, surface, bg_duration=10000, track_duration=3000):
        """Draw player's track directly with Pygame (no matplotlib, no PIL, works in pygbag)."""

        # Create a transparent surface to draw the track
        plot_surface = pygame.Surface((map_width, map_height), pygame.SRCALPHA)
        plot_surface.fill((0,0,0,0))  # fully transparent background

        # Extract track data
        x_points = self.track["x"]
        y_points = self.track["y"]
        points = list(zip(x_points, y_points))

        points = [(x/2.1 + 30, y/2 - 100) for (x, y) in points]

        # Draw connected lines with low opacity (alpha=40 out of 255)
        if len(points) > 1:
            pygame.draw.lines(plot_surface, (255, 165, 0, 100), False, points, 5)  # orange line


        # Center and blit to main screen
        rect = plot_surface.get_rect(topleft=(0,0))

        # Timing loop
        start_time = pygame.time.get_ticks()
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            elapsed = pygame.time.get_ticks() - start_time

            # Show track after track_duration ms
            if elapsed > track_duration:
                surface.blit(plot_surface, rect)

                if elapsed > bg_duration:
                    pygame.quit()
                    raise SystemExit

            pygame.display.flip()
            await asyncio.sleep(0)
            clock.tick(30)





