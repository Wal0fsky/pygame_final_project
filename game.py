import pygame
import os
from logic import move_player, rotate_player

pygame.init() # source: https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ&start_radio=1
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

class Player:
    def __init__(self):
        self.angle = 0 # so it is vertical
        self.pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.original_image = pygame.image.load(os.path.join("player.png")).convert_alpha()
        self.original_image = pygame.transform.scale_by(self.original_image, 0.25)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.pos))
        self.hitbox = self.image.get_rect(center=(self.pos))

player = Player()

while running: # game loop cycle
    dt = clock.tick(60) / 1000
    
    
    for event in pygame.event.get(): # event listener
        if event.type == pygame.QUIT: # player pressed "X"
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    screen.blit(player.image, player.rect)
    player.rect = player.image.get_rect(center=(player.pos))
    player.hitbox.center = player.pos
    pygame.draw.rect(screen, (255, 0, 0), player.hitbox, 2) # for debugging

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        move_player(True, player, dt)
    if keys[pygame.K_s]:
        move_player(False, player, dt)
    if keys[pygame.K_a]:
        if keys[pygame.K_s]:
            rotate_player(False, player, dt)
        else:
            rotate_player(True, player, dt)
    if keys[pygame.K_d]:
        if keys[pygame.K_s]:
            rotate_player(True, player, dt)
        else:
            rotate_player(False, player, dt)

    pygame.display.flip() # pygame generates stuff on a hidden layer and then swaps it to the layer we see so it avoids screen flickering. This allows us to see the stuff after a frame

pygame.quit()

