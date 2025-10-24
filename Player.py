import pygame

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
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position # replace player if it hits a boundary
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pygame.Surface([34,34])
        image.blit(self.sprite_sheet, (0,0), (x,y,34,34))
        return image