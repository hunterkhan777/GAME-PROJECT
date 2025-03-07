class JumpManager:
    def __init__(self, jump_strength, gravity):
        self.jump_strength = jump_strength
        self.gravity = gravity
        self.jumps_left = 2
        self.max_jumps = 2
        self.jump_cooldown = 0
        self.cooldown_time = 60  # frames (1 second at 60 FPS)
        self.is_jumping = False
        self.is_on_ground = True

    def update(self):
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1
        
        if self.is_on_ground:
            self.jumps_left = self.max_jumps

    def can_jump(self):
        return (self.jumps_left > 0 and self.jump_cooldown == 0)

    def jump(self):
        if self.can_jump():
            self.jumps_left -= 1
            self.is_jumping = True
            self.is_on_ground = False
            if self.jumps_left == 0:
                self.jump_cooldown = self.cooldown_time
            return -self.jump_strength
        return 0

    def land(self):
        self.is_jumping = False
        self.is_on_ground = True
        self.jumps_left = self.max_jumps