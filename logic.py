import pygame

class Game_Object:
    def __init__(self, angle, pos):
        self.angle = angle
        self.pos = pos

    def move(self, isForward, dt, speed):
        movement = pygame.Vector2()
        movement.from_polar((speed * dt, self.angle)) # 300 for player

        if isForward:
            self.pos += movement
        else:
            self.pos -= movement

    def rotate(self, isLeft, dt, speed):
        if isLeft: # vertical screen is inverted... why bruv
            self.angle -= dt * speed # 120 for player 
            # exclude for now, look if I'll make another function for updating the image: player.image = pygame.transform.rotate(player.image, -1 * (player.angle))
        
        else:
            self.angle += dt * speed
            # same with excluding here: player.image = pygame.transform.rotate(player.image, -1 * (player.angle))
    # transform the figure once we have one


class Player(Game_Object):
    def __init__(self, angle, pos, img):
        super().__init__(angle, pos)

        self.original_image = img # for game logic
        self.image = img
        self.rect = pygame.Surface.get_rect(self.image) #rect-based player movement

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

    def upd(self, screen, speed, dt):
        self.move(True, dt, speed)
        self.start_point = self.pos + self.initialization_vect
        self.end_point = self.pos + self.initialization_vect * 2
        
        if screen.get_rect().collidepoint(self.end_point.x, self.end_point.y):
            pygame.draw.line(screen, (255, 0, 0), self.start_point, self.end_point, 10)
            return False
        else:
            return True