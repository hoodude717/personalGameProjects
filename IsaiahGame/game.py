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
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)
PURPLE = (128, 0, 128)
BROWN = (139, 69, 19)

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


def remove_lamp_from_all_screens(idx: int):
    # Remove lamp index from all screen definitions
    for screen_idx in screens:
        if idx in screens[screen_idx]['lamp_indices']:
            screens[screen_idx]['lamp_indices'].remove(idx)


def add_lamp_to_current_screen(idx: int):
    if idx not in screens[current_screen]['lamp_indices']:
        screens[current_screen]['lamp_indices'].append(idx)


def remove_sheep_from_all_screens(idx: int):
    for screen_idx in screens:
        if idx in screens[screen_idx]['sheep_indices']:
            screens[screen_idx]['sheep_indices'].remove(idx)


def add_sheep_to_current_screen(idx: int):
    if idx not in screens[current_screen]['sheep_indices']:
        screens[current_screen]['sheep_indices'].append(idx)


# --- STARTING AREA: SHEEP PEN ---
# Define a fenced area on screen 0 where sheep can be dropped
pen_rect = pygame.Rect(20, SCREEN_HEIGHT - 220, 220, 200)
sheep_in_pen = [False for _ in sheep_rects]
sheep_in_pen_count = 0

# Title for the starting area
title_font = pygame.font.Font(None, 36)
title_text = title_font.render("Light in the Darkness", True, YELLOW)

# Win state
game_won = False
win_font = pygame.font.Font(None, 48)
win_text = win_font.render("You gathered all the sheep!", True, (20, 180, 20))
win_sub = title_font.render("Press R to restart", True, (200, 200, 200))


# # --- 2. THE HIDDEN CONTENT (The Revealed Truth) ---
# # Create the background/hidden layer
# hidden_text_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
# hidden_text_surface.fill(DARK_GRAY) # Dark background for high contrast with text

# # Add the key scripture quotes from Isaiah
font = pygame.font.Font(None, 15)
lamp_interact_text = font.render("Press Spacebar to Pickup Lamp", True, BLACK)
lamp_light_text = font.render("Press L to Light Lamp", True, BLACK)
sheep_interact_text = font.render("Press S to Pickup Sheep", True, BLACK)


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


def check_win():
    """Set the win state when all sheep are in the pen."""
    global game_won
    if sheep_in_pen_count == len(sheep_rects):
        game_won = True
        print("All sheep gathered! You win!")


def reset_game():
    """Reset game state to initial positions and counts."""
    global game_won, sheep_in_pen_count, sheep_in_pen, sheep_picked_up, screens, current_screen
    game_won = False
    sheep_in_pen = [False for _ in sheep_rects]
    sheep_in_pen_count = 0
    sheep_picked_up = [False for _ in sheep_rects]

    # Reset sheep positions
    rect_sheep.topleft = (100, SCREEN_HEIGHT - 150)
    rect_sheep2.topleft = (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150)

    # Reset screens membership (lamps remain where they were originally placed on screen 1)
    screens = {
        0: {'lamp_indices': [], 'sheep_indices': []},
        1: {'lamp_indices': [0, 1, 2, 3, 4], 'sheep_indices': [0, 1]}
    }
    current_screen = 0

# --- 4. THE GAME LOOP ---
while running:
    screen.fill((255, 255, 255))
    
        #Checking input
    key = pygame.key.get_pressed()
    # Disable movement when the game is won
    if not game_won:
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
    if rect_shepherd.centerx > SCREEN_WIDTH:
        current_screen += 1
        if current_screen > 1:  
            current_screen = 1
            rect_shepherd.centerx = SCREEN_WIDTH
        # Move shepherd to left side of new screen
        else:
            rect_shepherd.centerx = 10
    
    # Check if shepherd goes off the left edge of screen
    if rect_shepherd.right < 0:
        current_screen -= 1
        if current_screen < 0:
            rect_shepherd.right = 0
            current_screen = 0
        else:
            rect_shepherd.centerx = SCREEN_WIDTH - 10 


    lamp_idx, is_close_lamp = close_to_lamp()
    sheep_idx, is_close_sheep = close_to_sheep()

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


    # If on starting screen, draw the title and pen area
    if current_screen == 0:
        # Draw fenced pen area
        pygame.draw.rect(screen, (139, 69, 19), pen_rect)  # brown fill
        pygame.draw.rect(screen, WHITE, pen_rect, 2)  # white border
        # Sheep count in pen

    # Draw sheep: show if on current screen or picked up
    visible_sheep_indices = get_visible_sheep()
    for i in range(len(sheep_rects)):
        if i in visible_sheep_indices or sheep_picked_up[i]:
            screen.blit(sheep_images[i], sheep_rects[i])
    
    # Draw lamps: show if on current screen or picked up
    visible_lamp_indices = get_visible_lamps()
    for i in range(len(lamp_list)):
        if i in visible_lamp_indices or lamp_is_picked_up[i]:
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
        


    # # 4.1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle space key press for picking up/dropping lamp
        if event.type == pygame.KEYDOWN:
            # If we've already won, only allow restart
            if game_won:
                if event.key == pygame.K_r:
                    reset_game()
                # ignore other keys
                continue
            if event.key == pygame.K_SPACE:
                # If near a visible lamp, toggle pick/drop for that lamp
                if is_close_lamp and lamp_idx != -1:
                    # If picking up, remove it from screens; if dropping, add to current screen
                    if not lamp_is_picked_up[lamp_idx]:
                        lamp_is_picked_up[lamp_idx] = True
                        remove_lamp_from_all_screens(lamp_idx)
                        print(f"Lamp {lamp_idx} picked up: {lamp_is_picked_up[lamp_idx]}")
                    else:
                        lamp_is_picked_up[lamp_idx] = False
                        add_lamp_to_current_screen(lamp_idx)
                        lamp_list[lamp_idx].center = rect_shepherd.center
                        print(f"Lamp {lamp_idx} dropped on screen {current_screen}")
                else:
                    # If not near any visible lamp, drop the first picked up lamp (if any)
                    for i, picked in enumerate(lamp_is_picked_up):
                        if picked:
                            lamp_is_picked_up[i] = False
                            add_lamp_to_current_screen(i)
                            lamp_list[i].center = rect_shepherd.center
                            print(f"Lamp {i} dropped on screen {current_screen}")
                            break
            
            # Handle 'L' key press for lighting/extinguishing lamp
            if event.key == pygame.K_l:
                if is_close_lamp and lamp_idx != -1:
                    lamp_is_lit[lamp_idx] = not lamp_is_lit[lamp_idx]
                    print(f"Lamp {lamp_idx} lit: {lamp_is_lit[lamp_idx]}")
                else:
                    # Toggle the first picked-up lamp's lit state if none nearby
                    for i, picked in enumerate(lamp_is_picked_up):
                        if picked:
                            lamp_is_lit[i] = not lamp_is_lit[i]
                            print(f"Lamp {i} lit: {lamp_is_lit[i]}")
                            break
                    
            if event.key == pygame.K_s:
                current_sheep_idx, current_is_close = close_to_sheep()
                if current_is_close and current_sheep_idx != -1:
                    if not sheep_picked_up[current_sheep_idx]:
                        # Picking up: if in pen, decrement pen count
                        if sheep_in_pen[current_sheep_idx]:
                            sheep_in_pen[current_sheep_idx] = False
                            sheep_in_pen_count -= 1
                        sheep_picked_up[current_sheep_idx] = True
                        remove_sheep_from_all_screens(current_sheep_idx)
                        print(f"Sheep {current_sheep_idx} picked up: {sheep_picked_up[current_sheep_idx]}")
                    else:
                        sheep_picked_up[current_sheep_idx] = False
                        add_sheep_to_current_screen(current_sheep_idx)
                        sheep_rects[current_sheep_idx].bottomleft = (
                            rect_shepherd.x + (SHEPHERD_W // 2) + ((current_sheep_idx * 5)), rect_shepherd.y + SHEPHERD_H)
                        # If dropped in pen area and we're on the starting screen, increment pen count
                        if current_screen == 0 and pen_rect.colliderect(sheep_rects[current_sheep_idx]):
                            if not sheep_in_pen[current_sheep_idx]:
                                sheep_in_pen[current_sheep_idx] = True
                                sheep_in_pen_count += 1
                                check_win()
                        print(f"Sheep {current_sheep_idx} dropped on screen {current_screen}")
                else:
                    # Drop the first picked up sheep (if any)
                    for i, picked in enumerate(sheep_picked_up):
                        if picked:
                            sheep_picked_up[i] = False
                            add_sheep_to_current_screen(i)
                            sheep_rects[i].bottomleft = (
                                rect_shepherd.x + (SHEPHERD_W // 2) + ((i * 5)), rect_shepherd.y + SHEPHERD_H)
                            if current_screen == 0 and pen_rect.colliderect(sheep_rects[i]):
                                if not sheep_in_pen[i]:
                                    sheep_in_pen[i] = True
                                    sheep_in_pen_count += 1
                                    check_win()
                            print(f"Sheep {i} dropped on screen {current_screen}")
                            break


    
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
    # Also create light around lit lamps (only visible or picked-up ones)
    for i in range(len(lamp_list)):
        if lamp_is_lit[i] and (i in visible_lamp_indices or lamp_is_picked_up[i]):
            lamp_light_x = lamp_list[i].centerx - LAMP_RADIUS
            lamp_light_y = lamp_list[i].centery - LAMP_RADIUS
            darkness_surface.blit(lamp_source_eraser, (lamp_light_x, lamp_light_y), 
                                special_flags=pygame.BLEND_RGBA_MIN)
    
    # Draw the darkness overlay on top of everything
    # Draw shepherd on top of the pen/sprites (but still under darkness overlay)
    screen.blit(shepherd, rect_shepherd)

    screen.blit(darkness_surface, (0, 0))
    if current_screen == 0:
        # Draw title centered at top
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
        sheep_count_surface = font.render(f"Sheep: {sheep_in_pen_count}/{len(sheep_rects)}", True, WHITE)
        screen.blit(sheep_count_surface, (SCREEN_WIDTH // 2 - sheep_count_surface.get_width() // 2, 50))

    # If player has won, draw a win overlay and hint to restart
    if game_won:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        # Draw win box
        box_w, box_h = 600, 200
        box_x = SCREEN_WIDTH // 2 - box_w // 2
        box_y = SCREEN_HEIGHT // 2 - box_h // 2
        pygame.draw.rect(screen, (30, 30, 30), (box_x, box_y, box_w, box_h))
        pygame.draw.rect(screen, WHITE, (box_x, box_y, box_w, box_h), 3)
        # Blit win text centered
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, box_y + 40))
        screen.blit(win_sub, (SCREEN_WIDTH // 2 - win_sub.get_width() // 2, box_y + 120))

    
    # Update the display

    pygame.display.flip()
    # Limit frame rate
    clock.tick(60)

pygame.quit()