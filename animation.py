import pygame

class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, name, width, height, nb_animations):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f"objects/{name}.png").convert_alpha()

        # Load all animation frames
        if name == "Hoops":
            print("Hoop")
            self.y_offset = 160
            self.x_offset = 40
            self.images = self.get_images(self.x_offset, self.y_offset, width, height, nb_animations)

        elif name == "Jellyfish":
            print("Jellyfish")
            self.y_offset = 100
            self.x_offset = 5
            self.images = self.get_images(self.x_offset, self.y_offset, width, height, nb_animations)

        # Animation state
        self.animation_index = 0
        # self.image = self.get_image(0,160, width, height) # say where the image is in the png file
        self.image = self.images[self.animation_index]
        # self.image.set_colorkey((128, 0, 128)) # remove purple background - get background with print(self.sprite_sheet.get_at((0, 0)))
        self.rect = self.image.get_rect()
        self.animation_speed = 0.1  # lower = slower animation
        self.clock = 0.0


    def get_images(self, x_offset, y_offset, width, height, nb_animations):
        """Extract nb_animations frames horizontally from sprite sheet."""
        images = []
        for i in range(nb_animations):
            x = x_offset + i * width
            image = self.get_image(x, y_offset, width, height)
            images.append(image)
        return images

    def get_image(self, x, y, width, height):
        """Extract one frame at (x, y) with given size."""
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Detect background color automatically (top-left pixel)
        bg_color = self.sprite_sheet.get_at((0, 0))[:3]

        # Apply color key to remove background
        image.set_colorkey(bg_color)

        return image

    def animate(self):
        """Update animation frame."""
        self.clock += self.animation_speed
        if self.clock >= 1:
            self.clock = 0
            self.animation_index = (self.animation_index + 1) % len(self.images)
            self.image = self.images[self.animation_index]
