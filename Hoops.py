import pygame

# make hoop class

class Hoop(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load("objects/Hoops.png")
        self.image = self.get_image(0, 80*2) # location of the hoop on the png file
        self.image.set_colorkey((128, 0, 128)) # remove purple background - get background with print(self.sprite_sheet.get_at((0, 0)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def get_image(self, map_x, map_y, width=40, height=80):
        image = pygame.Surface([width,height])
        image.blit(self.sprite_sheet, (0,0), (map_x,map_y,80,80))
        return image

    def update(self, *args, **kwargs):
        pass  # Do nothing

