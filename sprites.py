import pygame

def load_animation(prefix, count, size):
    """Load animation frames from files"""
    animation = []
    for i in range(1, count + 1):
        img_path = f"c:\\Users\\hk\\Desktop\\tb\\main char\\{prefix} ({i}).png"
        try:
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, size)
            animation.append(img)
        except pygame.error:
            print(f"Error loading: {img_path}")
            # Create fallback surface
            surface = pygame.Surface(size)
            surface.fill((255, 0, 0))
            animation.append(surface)
    return animation

def load_player_sprites(player_size):
    """Load all player sprites"""
    return {
        'idle': load_animation("Idle", 10, player_size),
        'run': load_animation("Run", 8, player_size),
        'jump': load_animation("Jump", 12, player_size),
        'hurt': load_animation("Hurt", 8, player_size),
        'dead': load_animation("Dead", 10, player_size),
        'slide': load_animation("Slide", 5, player_size)
    }