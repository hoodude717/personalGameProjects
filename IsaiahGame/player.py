import pygame
# (Other imports remain the same)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # 1. Appearance (Replace with a proper image later)
        self.image = pygame.Surface([30, 40])
        self.image.fill((0, 255, 0)) # Green block for placeholder
        
        # 2. Position and Size (Rect)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # 3. Movement
        self.change_x = 0
        self.change_y = 0
        self.speed = 3

    def changespeed(self, x, y):
        # Function to change the speed vector (used by keyboard input)
        self.change_x += x
        self.change_y += y

    def update(self):
        # Function to update the player's position based on its current speed
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        
        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT