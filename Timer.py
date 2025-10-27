import pygame





class Timer:
    def __init__(self, duration, font_size=30, position=(10, 10), color=(255, 255, 255)):
        self.duration = duration              # in milliseconds
        self.start_time = 0
        self.active = False
        self.font = pygame.font.Font(None, font_size)
        self.position = position
        self.color = color

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        if self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.duration:
                self.deactivate()

    def get_time_left(self):
        """Return remaining time in seconds."""
        if not self.active:
            return 0
        elapsed = pygame.time.get_ticks() - self.start_time
        return max(0, (self.duration - elapsed) // 1000)

    def display_timer(self, surface):
        """Draw the timer on the given surface (e.g. the game screen)."""
        if self.active:
            time_left = self.get_time_left()
            text = self.font.render(f"Time left: {time_left}", True, self.color)
            surface.blit(text, self.position)

    def game_over(self, surface):
        big_font = pygame.font.Font(None, 80)
        text = big_font.render("GAME OVER", True, (255, 50, 50))
        text_rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
        surface.blit(text, text_rect)