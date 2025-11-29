import pygame

from lamp import Lamp
from player import Player

# --- 1. SETUP AND INITIALIZATION ---
pygame.init()

# Define screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
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
lamp_lit = pygame.image.load("lamp_flame.png").convert_alpha()
lamp2 = pygame.image.load("lamp.png").convert_alpha()
lamp_lit2 = pygame.image.load("lamp_flame.png").convert_alpha()
lamp3 = pygame.image.load("lamp.png").convert_alpha()
lamp_lit3 = pygame.image.load("lamp_flame.png").convert_alpha()
lamp4 = pygame.image.load("lamp.png").convert_alpha()
lamp_lit4 = pygame.image.load("lamp_flame.png").convert_alpha()
lamp5 = pygame.image.load("lamp.png").convert_alpha()
lamp_lit5 = pygame.image.load("lamp_flame.png").convert_alpha()

rect_shepherd = shepherd.get_rect()
SHEPHERD_H = rect_shepherd.height
SHEPHERD_W = rect_shepherd.width
rect_sheep = sheep.get_rect()
rect_sheep2 = sheep2.get_rect()
rect_lamp = lamp.get_rect()
rect_lamp_lit = lamp_lit.get_rect()
rect_lamp2 = lamp.get_rect()
rect_lamp_lit2 = lamp_lit.get_rect()
rect_lamp3 = lamp.get_rect()
rect_lamp_lit3 = lamp_lit.get_rect()
rect_lamp4 = lamp.get_rect()
rect_lamp_lit4 = lamp_lit.get_rect()
rect_lamp5 = lamp.get_rect()
rect_lamp_lit5 = lamp_lit.get_rect()

# Set explicit starting positions for the sprites (customize these as you like)
# Place the shepherd near the center of the screen
rect_shepherd.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
# Place two sheep near the bottom left and bottom right
rect_sheep.topleft = (100, SCREEN_HEIGHT - 150)
rect_sheep2.topleft = (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150)
# Place the lamp near the top-left corner
rect_lamp.topleft = (50, 50)
rect_lamp2.topleft = (50, SCREEN_HEIGHT - 50)
rect_lamp3.topleft = (SCREEN_WIDTH - 50, 50)
rect_lamp4.topleft = (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)
rect_lamp5.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


sheep_rects = [rect_sheep, rect_sheep2]
sheep_images = [sheep, sheep2]
sheep_picked_up = [False, False]


lamp_list = [rect_lamp, rect_lamp2, rect_lamp3, rect_lamp4, rect_lamp5]
lamp_lit_list = [rect_lamp_lit, rect_lamp_lit2, rect_lamp_lit3, rect_lamp_lit4, rect_lamp_lit5]
lamp_images = [lamp, lamp2, lamp3, lamp4, lamp5]
lamp_lit_images = [lamp_lit, lamp_lit2, lamp_lit3, lamp_lit4, lamp_lit5]   
lamp_is_picked_up = [False, False, False, False, False]
lamp_is_lit = [False, False, False, False, False]

# --- LEVEL/SCREEN SYSTEM ---
# Track which screen the shepherd is on (screen 0 = starting area, screen 1 = main level)
current_screen = 0

# Define which objects belong to which screen
# Format: {lamp_indices: [...], sheep_indices: [...]}
screens = {
    0: {  # Starting area (empty for now)
        'lamp_indices': [],
        'sheep_indices': []
    },
    1: {  # Main level with lamps and sheep
        'lamp_indices': [0, 1, 2, 3, 4],  # All 5 lamps
        'sheep_indices': [0, 1]  # Both sheep
    }
}

# Helper function to get visible objects for current screen
def get_visible_lamps():
    return screens[current_screen]['lamp_indices']

def get_visible_sheep():
    return screens[current_screen]['sheep_indices']


# # --- 2. THE HIDDEN CONTENT (The Revealed Truth) ---
# # Create the background/hidden layer
# hidden_text_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
# hidden_text_surface.fill(DARK_GRAY) # Dark background for high contrast with text

# # Add the key scripture quotes from Isaiah
font = pygame.font.Font(None, 15)
lamp_interact_text = font.render("Press Spacebar to Pickup Lamp", True, BLACK)
lamp_light_text = font.render("Press L to Light Lamp", True, BLACK)
sheep_interact_text = font.render("Press S to Pickup Sheep", True, BLACK)
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
darkness_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
darkness_surface.fill((0, 0, 0, 250))  # Black with some transparency

# Define the light properties
LIGHT_RADIUS = 100
LAMP_RADIUS = 500
# Create the circular light source (the "eraser")
light_source_eraser = pygame.Surface((LIGHT_RADIUS * 2, LIGHT_RADIUS * 2), pygame.SRCALPHA)
lamp_source_eraser = pygame.Surface((LAMP_RADIUS * 2, LAMP_RADIUS * 2), pygame.SRCALPHA)


# Create a gradient light effect - fully opaque black in corners, fading to transparent at center
for r in range(LIGHT_RADIUS * 2, 0, -5):
    # Invert: corners are opaque (255), center is transparent (0)
    if r >= LIGHT_RADIUS:
        # Outer part: opaque black
        alpha = 250
    else:
        # Inner part: fade from opaque to transparent
        alpha = int((r / LIGHT_RADIUS) * 250)
    
    # Draw a black circle with this alpha value
    pygame.draw.circle(light_source_eraser, (0, 0, 0, alpha), (LIGHT_RADIUS, LIGHT_RADIUS), r)

# Create a gradient light effect - fully opaque black in corners, fading to transparent at center
for r in range(LAMP_RADIUS * 2, 0, -5):
    # Invert: corners are opaque (255), center is transparent (0)
    if r >= LAMP_RADIUS:
        # Outer part: opaque black
        alpha = 250
    else:
        # Inner part: fade from opaque to transparent
        alpha = int((r / LAMP_RADIUS) * 250)
    
    # Draw a black circle with this alpha value
    pygame.draw.circle(lamp_source_eraser, (0, 0, 0, alpha), (LAMP_RADIUS, LAMP_RADIUS), r)


def close_to_sheep() -> tuple[int, bool]:
    sheep_indices = get_visible_sheep()
    
    for i in sheep_indices:
        distance = ((rect_shepherd.centerx - sheep_rects[i].centerx)**2 + 
                (rect_shepherd.centery - sheep_rects[i].centery)**2)**0.5
        if distance < 50:
            return i, True
    return -1, False

def close_to_lamp() -> tuple[int, bool]:
    lamp_indices = get_visible_lamps()
    
    for i in lamp_indices:
        distance = ((rect_shepherd.centerx - lamp_list[i].centerx)**2 + 
                (rect_shepherd.centery - lamp_list[i].centery)**2)**0.5
        if distance < 50:
            return i, True
    return -1, False

# --- 4. THE GAME LOOP ---
while running:
    screen.fill((255, 255, 255))

    lamp_idx, is_close_lamp = close_to_lamp()
    sheep_idx, is_close_sheep = close_to_sheep()
    print(sheep_idx)

    # Make lamps follow shepherd if picked up
    for i in range(len(lamp_list)):
        if lamp_is_picked_up[i]:
            lamp_list[i].center = rect_shepherd.center
            if not lamp_is_lit[i]:
                screen.blit(lamp_light_text, (rect_shepherd.x, rect_shepherd.y-15))

    #Make Sheep Follow Shepherd if picked up
    for i in range(len(sheep_rects)):
        if sheep_picked_up[i]:
            sheep_rects[i].bottomleft =( rect_shepherd.x + (SHEPHERD_W//2) + ((i*5)), rect_shepherd.y+SHEPHERD_H)


    screen.blit(shepherd, rect_shepherd)
    
    # Draw sheep only if they're on the current screen
    visible_sheep_indices = get_visible_sheep()
    for sheep_idx in visible_sheep_indices:
        screen.blit(sheep_images[sheep_idx], sheep_rects[sheep_idx])
    
    # Draw lamps only if they're on the current screen
    visible_lamp_indices = get_visible_lamps()
    for i in visible_lamp_indices:
        if lamp_is_lit[i]:
            lamp_lit_list[i].center = lamp_list[i].center
            screen.blit(lamp_lit_images[i], lamp_lit_list[i])
        else:
            screen.blit(lamp_images[i], lamp_list[i])
            
            
    if (is_close_sheep and not sheep_picked_up[sheep_idx]):
        screen.blit(sheep_interact_text, (rect_shepherd.x, rect_shepherd.y-15))
            
    if (is_close_lamp and not lamp_is_picked_up[lamp_idx]):
        if not lamp_is_lit[lamp_idx]:
            screen.blit(lamp_light_text, (rect_shepherd.x, rect_shepherd.y-5))
        screen.blit(lamp_interact_text, (rect_shepherd.x, rect_shepherd.y-15))
        
    #Checking input
    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        rect_shepherd.move_ip(0, -5)
    if key[pygame.K_DOWN]:
        rect_shepherd.move_ip(0, 5)
    if key[pygame.K_LEFT]:
        rect_shepherd.move_ip(-5, 0)
    if key[pygame.K_RIGHT]:
        rect_shepherd.move_ip(5,0)
    
    # --- SCREEN TRANSITIONS ---
    # Check if shepherd goes off the right edge of screen
    if rect_shepherd.left > SCREEN_WIDTH:
        current_screen += 1
        if current_screen > 1:  # Wrap back or limit to available screens
            current_screen = 1
        # Move shepherd to left side of new screen
        rect_shepherd.centerx = 10
    
    # Check if shepherd goes off the left edge of screen
    if rect_shepherd.right < 0:
        current_screen -= 1
        if current_screen < 0:
            rect_shepherd.right = 0
            current_screen = 0
        else:
            rect_shepherd.centerx = SCREEN_WIDTH - 10 

        # Move shepherd to right side of new screen
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
        
        # Handle space key press for picking up/dropping lamp
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if is_close_lamp:
                    lamp_is_picked_up[lamp_idx] = not lamp_is_picked_up[lamp_idx]
                    print(f"Lamp {lamp_idx} picked up: {lamp_is_picked_up[lamp_idx]}")
            
            # Handle 'L' key press for lighting/extinguishing lamp
            if event.key == pygame.K_l:
                if is_close_lamp:
                    lamp_is_lit[lamp_idx] = not lamp_is_lit[lamp_idx]
                    print(f"Lamp {lamp_idx} lit: {lamp_is_lit[lamp_idx]}")
                    
            if event.key == pygame.K_s:
                print(sheep_idx)
                if is_close_sheep:
                    sheep_picked_up[sheep_idx] = not sheep_picked_up[sheep_idx]
                    print(f"Sheep {sheep_idx} picked up: {sheep_picked_up[sheep_idx]}")

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
    
    # --- 4.3. DRAWING THE DARKNESS AND LIGHT ---
    # Fill the darkness surface fresh each frame
    darkness_surface.fill((0, 0, 0, 250))
    
    # Create the light effect around the shepherd
    light_pos_x = rect_shepherd.centerx - LIGHT_RADIUS
    light_pos_y = rect_shepherd.centery - LIGHT_RADIUS
    
    # Blit the light eraser (creates a glowing circle) onto the darkness surface
    darkness_surface.blit(light_source_eraser, (light_pos_x, light_pos_y), 
                          special_flags=pygame.BLEND_RGBA_MIN)
    
    # Also create light around lit lamps
    for i in range(len(lamp_list)):
        if lamp_is_lit[i]:
            lamp_light_x = lamp_list[i].centerx - LAMP_RADIUS
            lamp_light_y = lamp_list[i].centery - LAMP_RADIUS
            darkness_surface.blit(lamp_source_eraser, (lamp_light_x, lamp_light_y), 
                                special_flags=pygame.BLEND_RGBA_MIN)
    
    # Draw the darkness overlay on top of everything
    screen.blit(darkness_surface, (0, 0))
    
    # Update the display

    pygame.display.flip()
    # Limit frame rate
    clock.tick(60)

pygame.quit()