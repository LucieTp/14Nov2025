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

    def plot_track(self, surface):

        data = pd.DataFrame.from_dict(self.track)
        print(data)
        # plot
        plt.figure(figsize=(6, 6))
        sns.lineplot(x="x", y="y", sort=False, estimator=None, errorbar=None, data=data.sort_values(by = "time", ascending=False))
        plt.gca().invert_yaxis()  # flip to match Pygame coordinates
        plt.title("Player Track")
        plt.axis("off")

        # Save plot to an in-memory buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format="PNG", bbox_inches="tight", pad_inches=0)
        plt.close()  # close figure to free memory
        buffer.seek(0)

        image = Image.open(buffer)
        mode = image.mode
        size = image.size
        data = image.tobytes()
        plot_surface = pygame.image.fromstring(data, size, mode)

        # Center and blit on the screen
        rect = plot_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
        surface.blit(plot_surface, rect)


