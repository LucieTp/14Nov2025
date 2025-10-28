import pygame
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from PIL import Image
import io


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__() # here we initiate all the variables associated with player (self.blabla)
        self.sprite_sheet = pygame.image.load("player/Hamster-Sprite.png")
        self.image = self.get_image(0,0) # say where the image is in the png file
        self.image.set_colorkey((0,0,0)) # remove background
        self.rect = self.image.get_rect() # create image rectangle
        self.position = [x, y] # player position
        self.images = { # different image for different orientations
            "down":self.get_image(0,34),
            "left":self.get_image(0,70),
            "right":self.get_image(0,70),
            "up":self.get_image(0,34*5)
        }
        self.feet = pygame.Rect(0,0, self.rect.width * 0.5, 12) # feet location for collisions
        self.old_position = self.position.copy() # keep in record the old position to replace the player in case of collision
        self.speed = 3 # number of pixels the player moves in one press
        self.track = {"time":[], "x":[], "y":[]} # where we will save timestep, x and y coords
        self.last_save_time = 0

    # then we create functions which take the variables as input and
    # changes their values
    def save_location(self): self.old_position = self.position.copy()

    def change_orientation(self, name):
        self.image = self.images[name]
        self.image.set_colorkey((0,0,0)) # avoid having the background

    def move_right(self): self.position[0] += self.speed
    def move_left(self): self.position[0] -= self.speed
    def move_up(self): self.position[1] -= self.speed
    def move_down(self): self.position[1] += self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet   .midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position # replace player if it hits a boundary
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pygame.Surface([34,34])
        image.blit(self.sprite_sheet, (0,0), (x,y,34,34))
        return image

    def save_track(self, time):

        # only save every half a second
        current_time = pygame.time.get_ticks()  # in milliseconds
        if current_time - self.last_save_time >= 500:  # 500 ms = 0.5 sec
            self.last_save_time = current_time

            self.track["time"].append(current_time / 1000)
            self.track["x"].append(self.position[0])
            self.track["y"].append(self.position[1])

    def plot_track(self, map_width, map_height, surface, pause_duration=10000):

        data = pd.DataFrame.from_dict(self.track)

        # plot
        plt.figure(figsize=(10, 10))
        sns.lineplot(x="x", y="y", sort=False, linewidth = 10, color = "black", estimator=None, errorbar=None, data=data.sort_values(by = "time", ascending=False))
        plt.xlim(0, map_width)
        plt.ylim(0, map_height)
        plt.gca().invert_yaxis()  # flip to match Pygame coordinates (where 0,0 is at the top left and not bottom left like seaborn)
        plt.title("Triathlon dans l'après midi")
        plt.axis("off")

        # Save plot to an in-memory buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format="PNG", bbox_inches="tight", pad_inches=0, transparent=True)
        plt.close()  # close figure to free memory
        buffer.seek(0)

        # transform image into a pygame image
        image = Image.open(buffer)
        mode = image.mode
        size = image.size
        data = image.tobytes()
        plot_surface = pygame.image.fromstring(data, size, mode)

        # Scale plot up to fill the entire screen
        screen_width, screen_height = surface.get_size()
        plot_surface = pygame.transform.smoothscale(plot_surface, (screen_width, screen_height))

        # Center and blit on the screen
        rect = plot_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
        surface.blit(plot_surface, rect)

        # display before pausing
        pygame.display.flip()

        # Keep plot visible for a duration
        start_time = pygame.time.get_ticks()
        running = True
        while running:
            # still allow the player to quit the screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # pause until time out
            if pygame.time.get_ticks() - start_time > pause_duration:
                running = False

            pygame.time.Clock().tick(30)



