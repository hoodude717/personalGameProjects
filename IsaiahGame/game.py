import pygame

from lamp import Lamp
from player import Player

# --- 1. SETUP AND INITIALIZATION ---
pygame.init()

# Define screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Light in the Darkness (Isaiah Project)")

# Define Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (100, 100, 100)

# # Game loop control
running = True
clock = pygame.time.Clock()

shepherd = pygame.image.load("shepherd.png").convert_alpha()
sheep = pygame.image.load("sheep.png").convert_alpha()
sheep2 = pygame.image.load("sheep.png").convert_alpha()

lamp = pygame.image.load("lamp.png").convert_alpha()
rect_shepherd = shepherd.get_rect()
rect_sheep = sheep.get_rect()
rect_sheep2 = sheep2.get_rect()
rect_lamp = lamp.get_rect()


# # --- 2. THE HIDDEN CONTENT (The Revealed Truth) ---
# # Create the background/hidden layer
# hidden_text_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
# hidden_text_surface.fill(DARK_GRAY) # Dark background for high contrast with text

# # Add the key scripture quotes from Isaiah
# font = pygame.font.Font(None, 30)
# # Isaiah 9:2: The people that walked in darkness...
# quote1_text = font.render("Isaiah 9:2: The people that walked in darkness have seen a great light.", True, WHITE)
# # Isaiah 60:1: Arise, shine...
# quote2_text = font.render("Isaiah 60:1: Arise, shine; for thy light is come, and the glory of the LORD is risen upon thee.", True, WHITE)
# # Placement of quotes
# hidden_text_surface.blit(quote1_text, (50, 150))
# hidden_text_surface.blit(quote2_text, (50, 400))
# # Add a central symbolic image or text
# symbol_text = font.render("CHRIST: The Light of the World", True, WHITE)
# hidden_text_surface.blit(symbol_text, (SCREEN_WIDTH // 2 - symbol_text.get_width() // 2, SCREEN_HEIGHT // 2))


# # --- 3. THE DARKNESS LAYER AND LIGHT SOURCE ---
# # Create the Darkness Overlay with transparency (SRCALPHA)
# # The darkness starts fully opaque.
# darkness_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
# darkness_surface.fill(BLACK) 

# # Define the light properties
# LIGHT_RADIUS = 60

# # Create the circular light source (the "eraser")

# light_source_eraser = pygame.Surface((LIGHT_RADIUS * 2, LIGHT_RADIUS * 2), pygame.SRCALPHA)
# light_source_eraser.fill((0, 0, 0, 0))

# permanent_light_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
# permanent_light_surface.fill((0,0,0,255))


# for r in range(LIGHT_RADIUS, 0, -10):
#     # Calculate transparency (alpha): center should be fully transparent (0), edges more opaque
#     alpha = int((r / LIGHT_RADIUS) * 255)
    
#     # Draw a black circle with decreasing alpha (more transparent toward center)
#     pygame.draw.circle(light_source_eraser, (0, 0, 0, alpha), (LIGHT_RADIUS, LIGHT_RADIUS), r)
# player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# all_sprites = pygame.sprite.Group()
# all_sprites.add(player)
# # --- Initialization Section ---
# # ... (existing player and all_sprites setup) ...

# # Create Lamp Group
# lamp_group = pygame.sprite.Group()

# # Create Lamp Instances (place them around the room)
# lamp1 = Lamp(50, 50)          # Top-left corner
# lamp2 = Lamp(700, 500)        # Bottom-right corner

# lamp_group.add(lamp1, lamp2)
# all_sprites.add(lamp1, lamp2) # Add to the main group for drawing

# --- 4. THE GAME LOOP ---
while running:

    screen.fill((255, 255, 255))

    screen.blit(shepherd, rect_shepherd)
    screen.blit(sheep, rect_sheep)
    screen.blit(sheep, rect_sheep2)
    screen.blit(lamp, rect_lamp)

    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        rect_shepherd.move_ip(0, -5)
    if key[pygame.K_DOWN]:
        rect_shepherd.move_ip(0, 5)
    if key[pygame.K_LEFT]:
        rect_shepherd.move_ip(-5, 0)
    if key[pygame.K_RIGHT]:
        rect_shepherd.move_ip(5,0) 
    # match key:
    #     case pygame.K_SPACE:
    #     # Loop through all lamps to see if the player is near one
    #     # for lamp in lamp_group:
    #     #     # Calculate the distance between the player's center and the lamp's center
    #     #     distance = ((player.rect.centerx - lamp.rect.centerx)**2 + 
    #     #                 (player.rect.centery - lamp.rect.centery)**2)**0.5
            
    #     #     if distance < lamp.interact_radius:
    #     #         # Player is close enough, so toggle the lamp state
    #         pass
    #     #         lamp.toggle()
    #     case pygame.K_LEFT:
    #         rect_shepherd.move_ip(-5, 0)
    #     case pygame.K_RIGHT:
    #         rect_shepherd.move_ip(5, 0)
    #     case pygame.K_UP:
    #         rect_shepherd.move_ip(0, -5)
    #     case pygame.K_DOWN:
    #         rect_shepherd.move_ip(0, 5)

    # # 4.1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #     #     # --- KEY PRESS EVENTS ---
    #     if event.type == pygame.KEYDOWN:
    #         match event.key:
    #             case pygame.K_SPACE:
    #             # Loop through all lamps to see if the player is near one
    #             # for lamp in lamp_group:
    #             #     # Calculate the distance between the player's center and the lamp's center
    #             #     distance = ((player.rect.centerx - lamp.rect.centerx)**2 + 
    #             #                 (player.rect.centery - lamp.rect.centery)**2)**0.5
                    
    #             #     if distance < lamp.interact_radius:
    #             #         # Player is close enough, so toggle the lamp state
    #                 pass
    #             #         lamp.toggle()
    #             case pygame.K_LEFT:
    #                 rect_shepherd.move_ip(-5, 0)
    #             case pygame.K_RIGHT:
    #                 rect_shepherd.move_ip(5, 0)
    #             case pygame.K_UP:
    #                 rect_shepherd.move_ip(0, -5)
    #             case pygame.K_DOWN:
    #                 rect_shepherd.move_ip(0, 5)

        # # --- KEY RELEASE EVENTS (Stop movement) ---
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_LEFT:
        #         player.changespeed(player.speed, 0) # Add back to cancel the minus
        #     if event.key == pygame.K_RIGHT:
        #         player.changespeed(-player.speed, 0) # Subtract to cancel the plus
        #     if event.key == pygame.K_UP:
        #         player.changespeed(0, player.speed)
        #     if event.key == pygame.K_DOWN:
        #         player.changespeed(0, -player.speed)
# # 4.2. Game Logic
#     all_sprites.update() 
    
#     # --- Permanent Lamp Light Logic ---
#     for lamp in lamp_group:
#         if lamp.is_on:
#             print(lamp.is_on)
#             # Calculate the lamp's center position for the light source
#             lamp_light_x = lamp.rect.centerx - LIGHT_RADIUS
#             lamp_light_y = lamp.rect.centery - LIGHT_RADIUS
            
#             # Blit the 'light_source' (transparent hole) onto the permanent light surface
#             # This creates a permanent, revealed area on the map.
#             permanent_light_surface.blit(light_source_eraser, 
#                                                 (lamp_light_x, lamp_light_y), 
#                                                 special_flags=pygame.BLEND_RGBA_MIN)


#     # --- Player Flashlight Position ---
#     light_pos_x = player.rect.centerx - LIGHT_RADIUS
#     light_pos_y = player.rect.centery - LIGHT_RADIUS

#     # 4.3. Drawing
#     # 1. Draw the hidden content
#     screen.blit(hidden_text_surface, (0, 0))
    
#     # 2. Draw the permanent light areas (already revealed by lamps)
#     # The permanent_light_surface now contains the holes created by the lamps.
#     screen.blit(permanent_light_surface, (0, 0))

#     # 3. Reset and Draw the darkness overlay
#     darkness_surface.fill(BLACK) 
    
#     # 4. Create the transient "hole" (the flashlight beam)
#     darkness_surface.blit(light_source_eraser, (light_pos_x, light_pos_y), special_flags=pygame.BLEND_RGBA_MIN)
#     # 5. Draw the darkness overlay on the screen (covering everything that isn't permanent light or player light)
#     screen.blit(darkness_surface, (0, 0))
    
#     # 6. Draw the sprites (player and lamps) on top
#     all_sprites.draw(screen) 
    
    # Update the display

    pygame.display.flip()
    # Limit frame rate
    clock.tick(60)

pygame.quit()