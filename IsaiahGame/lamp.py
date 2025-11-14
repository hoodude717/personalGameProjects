import pygame


class Lamp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Appearance: Placeholder colors for demonstration
        self.image_off = pygame.Surface([20, 50])
        self.image_off.fill((100, 100, 100)) # Gray for 'off'
        self.image_on = pygame.Surface([20, 50])
        self.image_on.fill((255, 255, 0))    # Yellow for 'on'
        
        self.image = self.image_off # Start in the 'off' state
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.is_on = False
        self.interact_radius = 100 # How close the player needs to be (in pixels)

    def toggle(self):
        # Change the lamp's state
        self.is_on = not self.is_on
        if self.is_on:
            self.image = self.image_on
        else:
            self.image = self.image_off