import pygame
import sys
from settings import *
from sprites import load_player_sprites
from jump_mechanics import JumpManager  # Add this import

# Initialize Pygame
pygame.init()

# Set up display
try:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    screen = pygame.display.set_mode((1280, 720))
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

pygame.display.set_caption("Platformer Game")
clock = pygame.time.Clock()

# Initialize game variables
floor_y = SCREEN_HEIGHT - FLOOR_HEIGHT
floor_scroll = 0
bg_scroll = [0, 0, 0, 0]  # Scroll positions for each background layer
bg_scroll_speed = [0.2, 0.4, 0.6, 0.8]  # Different speeds for each layer
player_pos = [375, floor_y - PLAYER_SIZE[1] + 30]
player_velocity = 0
player_alive = True
player_direction = 1
animation_index = 0
animation_cooldown = 5
animation_counter = 0
death_animation_complete = False

# Initialize jump manager
jump_manager = JumpManager(PLAYER_JUMP_STRENGTH, GRAVITY)

# Load sprites
player_sprites = load_player_sprites(PLAYER_SIZE)
background_layers = [
    pygame.image.load(r'c:\Users\hk\Desktop\tb\parallax_mountain_pack\layers\parallax-mountain-bg.png').convert_alpha(),
    pygame.image.load(r'c:\Users\hk\Desktop\tb\parallax_mountain_pack\layers\parallax-mountain-foreground-trees.png').convert_alpha(),
    pygame.image.load(r'c:\Users\hk\Desktop\tb\parallax_mountain_pack\layers\parallax-mountain-montain-far.png').convert_alpha(),
    pygame.image.load(r'c:\Users\hk\Desktop\tb\parallax_mountain_pack\layers\parallax-mountain-mountains.png').convert_alpha()
]
ground_image = pygame.image.load(r'c:\Users\hk\Desktop\tb\Sideview Sci-Fi - Patreon Collection\Environments\bulkhead-walls\PNG\floor.png').convert_alpha()
obstacle_image = pygame.image.load(r'c:\Users\hk\Desktop\tb\Sideview Sci-Fi - Patreon Collection\Environments\cyberpunk-detective-prop-files\PNG\hanging-terminal.png').convert_alpha()

# Define obstacles
obstacles = [
    pygame.Rect(screen.get_width() + x, floor_y - obstacle_image.get_height(), 
                obstacle_image.get_width(), obstacle_image.get_height())
    for x in [200, 600, 1000]
]

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_alive:
                player_velocity = jump_manager.jump()
            if event.key == pygame.K_r and not player_alive and death_animation_complete:
                # Reset game
                player_alive = True
                player_pos = [375, floor_y - PLAYER_SIZE[1] + 30]
                animation_index = 0
                jump_manager = JumpManager(PLAYER_JUMP_STRENGTH, GRAVITY)
                for obstacle in obstacles:
                    obstacle.x = screen.get_width() + 100 + pygame.time.get_ticks() % 500

    # Update game state
    if player_alive:
        # Handle movement
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_LEFT]:
            player_pos[0] -= PLAYER_SPEED
            player_direction = -1
            moving = True
        if keys[pygame.K_RIGHT]:
            player_pos[0] += PLAYER_SPEED
            player_direction = 1
            moving = True

        # Apply physics
        player_pos[1] += player_velocity
        if jump_manager.is_jumping:
            player_velocity += GRAVITY
        
        # Ground collision
        if player_pos[1] >= floor_y - PLAYER_SIZE[1] + 30:
            player_pos[1] = floor_y - PLAYER_SIZE[1] + 30
            player_velocity = 0
            jump_manager.land()

        # Update jump mechanics
        jump_manager.update()

        # Screen bounds
        player_pos[0] = max(0, min(player_pos[0], SCREEN_WIDTH - PLAYER_SIZE[0]))

        # Update obstacles
        floor_scroll = (floor_scroll + FLOOR_SPEED) % ground_image.get_width()
        for obstacle in obstacles:
            obstacle.x -= FLOOR_SPEED
            if obstacle.x < -obstacle.width:
                obstacle.x = screen.get_width() + 100 + pygame.time.get_ticks() % 500

        # Collision detection
        player_rect = pygame.Rect(player_pos[0] + 20, player_pos[1] + 20, 
                                PLAYER_SIZE[0] - 40, PLAYER_SIZE[1] - 40)
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                player_alive = False
                animation_index = 0
                death_animation_complete = False

    # Render game
    screen.fill((0, 128, 255))
    
    # Draw background with parallax effect
    for i, layer in enumerate(background_layers):
        # Update background scroll
        bg_scroll[i] = (bg_scroll[i] + bg_scroll_speed[i]) % SCREEN_WIDTH
        
        # Draw two copies of each layer for seamless scrolling
        scaled_layer = pygame.transform.scale(layer, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_layer, (-bg_scroll[i], 0))
        screen.blit(scaled_layer, (SCREEN_WIDTH - bg_scroll[i], 0))

    # Draw floor
    tiles_needed = SCREEN_WIDTH // ground_image.get_width() + 2
    for i in range(tiles_needed):
        screen.blit(ground_image, (i * ground_image.get_width() - floor_scroll, floor_y))

    # Draw obstacles
    for obstacle in obstacles:
        screen.blit(obstacle_image, obstacle.topleft)

    # Animation handling
    animation_counter += 1
    if animation_counter >= animation_cooldown:
        animation_counter = 0
        if player_alive:
            current_anim = (player_sprites['jump'] if jump_manager.is_jumping else 
                          player_sprites['run'] if moving else 
                          player_sprites['idle'])
            animation_index = (animation_index + 1) % len(current_anim)
        else:
            if animation_index < len(player_sprites['dead']) - 1:
                animation_index += 1
            else:
                death_animation_complete = True

    # Draw player
    current_anim = (player_sprites['dead'] if not player_alive else
                   player_sprites['jump'] if jump_manager.is_jumping else
                   player_sprites['run'] if moving else
                   player_sprites['idle'])
    current_frame = current_anim[min(animation_index, len(current_anim) - 1)]
    
    if player_direction == -1:
        current_frame = pygame.transform.flip(current_frame, True, False)
    
    screen.blit(current_frame, player_pos)

    # Game over text
    if not player_alive and death_animation_complete:
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("GAME OVER - Press R to restart", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                                   SCREEN_HEIGHT//2 - game_over_text.get_height()//2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()