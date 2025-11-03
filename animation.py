import pygame

class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, name, width, height, nb_animations):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f"objects/{name}.png").convert_alpha()

        # Load all animation frames
        if name == "Hoops":
            self.y_offset = 160
            self.x_offset = 40
            self.images = {"static":self.get_images(self.x_offset, self.y_offset, width, height, nb_animations, 1)}

        elif name == "Jellyfish":
            self.y_offset = 100
            self.x_offset = 5
            self.images = {"static":self.get_images(self.x_offset, self.y_offset, width, height, nb_animations, 0.5)}

        elif name == "Hamtaro1":
            self.y_offset = 0
            self.x_offset = 0
            self.images = {  # different image for different orientations
                "down": self.get_images(width + self.x_offset, height + self.y_offset, width, height, 4, 1),
                "left": self.get_images(width + self.x_offset, height * 3 + self.y_offset, width, height, 4, 1),
                "right": self.get_images(width + self.x_offset, height * 4 + 2, width, height, 4, 1),
                "up": self.get_images(width + self.x_offset, height * 2 + self.y_offset, width, height, 4, 1)
            }

        # Animation state
        self.animation_index = 0
        # self.image = self.get_image(0,160, width, height) # say where the image is in the png file
        self.image = self.images[list(self.images.keys())[0]][self.animation_index]
        # self.image.set_colorkey((128, 0, 128)) # remove purple background - get background with print(self.sprite_sheet.get_at((0, 0)))
        self.rect = self.image.get_rect()
        self.animation_speed = 0.1  # lower = slower animation
        self.clock = 0.0


    def change_orientation(self, name):
        self.animate(name)
        # self.image.set_colorkey((0,0,0)) # avoid having the background


    def get_image(self, x, y, width, height, scale):
        """Extract one frame at (x, y) with given size."""
        image = pygame.Surface((width, height), pygame.SRCALPHA)

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        # rescale image (make jellyfish smaller)
        size = image.get_size()
        image = pygame.transform.scale(image, (int(size[0] * scale), int(size[1] * scale)))

        # Detect background color automatically (top-left pixel)
        bg_color = self.sprite_sheet.get_at((0, 0))[:3]
        image.set_colorkey(bg_color)

        return image

    def get_images(self, x_offset, y_offset, width, height, nb_animations, scale):
        """Extract nb_animations frames horizontally from sprite sheet."""
        images = []
        for i in range(nb_animations):
            x = x_offset + i * width
            image = self.get_image(x, y_offset, width, height, scale)
            images.append(image)
        return images

    def animate(self, name):
        """Update animation frame."""
        self.clock += self.animation_speed
        if self.clock >= 1:
            self.clock = 0
            self.animation_index = (self.animation_index + 1) % len(self.images[name])
            self.image = self.images[name][self.animation_index]
