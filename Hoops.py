import pygame

from animation import AnimateSprite


# make hoop class

class Hoop(AnimateSprite):

    def __init__(self, name, x, y, id, width, height, nb_animations):
        super().__init__("Hoops", 40, 70, 4)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.number = id
        self.width = width
        self.height = height

    def update(self, *args, **kwargs):
        self.animate()  # Do nothing

