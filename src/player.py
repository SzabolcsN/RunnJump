import pygame
from settings import ORANGE, PLAYER_ACC, PLAYER_FRICTION, PLAYER_GRAVITY, PLAYER_JUMP

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.acc_x = 0.0
        self.on_ground = False
        self.jump_combo = 0
        self.last_jump_time = 0
        self.jump_combo_window = 250
        self.jump_pressed_last = False
        self.is_sliding = False
        self.slide_timer = 0
        self.slide_duration = 400
        self.normal_height = 60
        self.slide_height = 30

    def handle_input(self, keys):
        self.acc_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc_x = -PLAYER_ACC
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc_x = PLAYER_ACC
        jump_key = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
        if jump_key and self.on_ground and not self.jump_pressed_last and not self.is_sliding:
            self._jump()
        self.jump_pressed_last = jump_key
        slide_key = keys[pygame.K_DOWN] or keys[pygame.K_s]
        if slide_key and self.on_ground and abs(self.vel_x) > 2 and not self.is_sliding:
            self.slide()
        elif not slide_key and self.is_sliding:
            self.end_slide()

    def _jump(self):
        now = pygame.time.get_ticks()
        if self.on_ground:
            if now - self.last_jump_time < self.jump_combo_window:
                self.jump_combo += 1
            else:
                self.jump_combo = 1
            self.last_jump_time = now
            if self.jump_combo == 3:
                self.vel_y = -PLAYER_JUMP * 1.5
                self.jump_combo = 0
            else:
                self.vel_y = -PLAYER_JUMP
            self.on_ground = False

    def slide(self):
        self.is_sliding = True
        self.slide_timer = pygame.time.get_ticks()
        self.rect.height = self.slide_height
        self.rect.y += (self.normal_height - self.slide_height)
        if self.vel_x > 0:
            self.vel_x += 3
        elif self.vel_x < 0:
            self.vel_x -= 3

    def end_slide(self):
        if self.is_sliding:
            self.is_sliding = False
            self.rect.y -= (self.normal_height - self.slide_height)
            self.rect.height = self.normal_height

    def wall_jump(self):
        pass

    def update(self, platforms):
        if self.acc_x == 0:
            if abs(self.vel_x) < 0.5:
                self.vel_x = 0
            else:
                self.vel_x += PLAYER_FRICTION * self.vel_x
        else:
            self.vel_x += self.acc_x
            self.vel_x += PLAYER_FRICTION * self.vel_x * 0.2

        max_speed = 7.5
        if self.vel_x > max_speed:
            self.vel_x = max_speed
        if self.vel_x < -max_speed:
            self.vel_x = -max_speed

        self.rect.x += int(self.vel_x)

        self.vel_y += PLAYER_GRAVITY
        if self.vel_y > 20:
            self.vel_y = 20
        self.rect.y += int(self.vel_y)

        prev_on_ground = self.on_ground
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel_y > 0 and self.rect.bottom - self.vel_y <= plat.top:
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0 and self.rect.top - self.vel_y >= plat.bottom:
                    self.rect.top = plat.bottom
                    self.vel_y = 0
                elif self.vel_x > 0:
                    self.rect.right = plat.left
                    self.vel_x = 0
                elif self.vel_x < 0:
                    self.rect.left = plat.right
                    self.vel_x = 0
        if not self.on_ground:
            self.last_landed_time = pygame.time.get_ticks()
        elif not prev_on_ground and self.on_ground:
            pass

        if self.is_sliding:
            if pygame.time.get_ticks() - self.slide_timer > self.slide_duration or not self.on_ground:
                self.end_slide()

    def draw(self, surface):
        pygame.draw.rect(surface, ORANGE, self.rect) 