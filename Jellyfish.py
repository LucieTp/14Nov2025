from animation import AnimateSprite


class Jellyfish(AnimateSprite):

    def __init__(self, name, x, y, id, width, height, nb_animations):
        super().__init__(name, width, height, nb_animations)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.number = id
        self.width = width
        self.height = height
        self.is_active = False

    def update(self):
        # active hoop is the hoop with smallest id number (the one that should be crossed next)
        self.animate("static")
