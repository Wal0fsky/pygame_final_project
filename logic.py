import pygame
import matplotlib.path as mpath

class Game_Object:
    def __init__(self, angle, pos):
        self.angle = angle
        self.pos = pos

    def move(self, isForward, dt, speed):
        movement = pygame.Vector2()
        movement.from_polar((speed * dt, self.angle))

        if isForward:
            self.pos += movement
        else:
            self.pos -= movement

    def rotate(self, isLeft, dt, speed):
        if isLeft:
            self.angle -= dt * speed
        
        else:
            self.angle += dt * speed


class Player(Game_Object):
    def __init__(self, angle, pos, img):
        super().__init__(angle, pos)

        self.original_image = img # for game logic
        self.image = img
        self.rect = pygame.Surface.get_rect(self.image) # rect-based player movement

        hh = self.image.get_height() / 2
        hw = self.image.get_width() / 2

        self.HITBOX_POINTS = [
            pygame.Vector2(hw, hh), 
            pygame.Vector2(-hw, hh), 
            pygame.Vector2(-hw, -hh), 
            pygame.Vector2(hw, -hh)] # sadly, rects are axis-aligned

        self.upd_hitbox_points = [0, 0, 0, 0]

    def upd(self, screen):
        self.image = pygame.transform.rotate(self.original_image, -self.angle) # center based alignment
        self.rect = self.image.get_rect(center=(self.pos))

        for i in range(len(self.HITBOX_POINTS)):
            self.upd_hitbox_points[i] = self.pos + self.HITBOX_POINTS[i].rotate(self.angle)
            
        screen.blit(self.image, self.rect)

class Projectile(Game_Object):
    def __init__(self, angle, pos, player):
        super().__init__(angle, pos.copy())
        self.initialization_vect = pygame.Vector2()
        self.initialization_vect.from_polar(((player.HITBOX_POINTS[0] - player.HITBOX_POINTS[3]).y, self.angle))
        self.start_point = self.pos + self.initialization_vect
        self.end_point = self.pos + self.initialization_vect * 2

    def upd(self, screen, speed, dt):
        self.move(True, dt, speed)
        self.start_point = self.pos + self.initialization_vect
        self.end_point = self.pos + self.initialization_vect * 2
        
        if screen.get_rect().collidepoint(self.end_point.x, self.end_point.y):
            pygame.draw.line(screen, (255, 0, 0), self.start_point, self.end_point, 10)
            return False
        else:
            return True

class Enemy(Player):
    def __init__(self, angle, pos, img):
        super().__init__(angle, pos, img)

    def check_contact(self, polygon2_points):
        enemy_polygon = mpath.Path(self.upd_hitbox_points)
        polygon2 = mpath.Path(polygon2_points)
        if enemy_polygon.intersects_path(polygon2):
            return True
        else: 
            return False