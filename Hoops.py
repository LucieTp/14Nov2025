import pygame

from animation import AnimateSprite


# make hoop class

class Hoop(AnimateSprite):

    def __init__(self, name, x, y, id, width, height, nb_animations):
        super().__init__("Hoops", 37.5, 70, 9)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.number = id
        self.width = width
        self.height = height
        self.is_active = False

    def update(self, *args, **kwargs):
        # active hoop is the hoop with smallest id number (the one that should be crossed next)
        if self.is_active:
            self.animate()
        else:
            # Other hoops are static
            self.image = self.images[0]


