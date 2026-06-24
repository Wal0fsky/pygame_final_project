import pygame
import os
import sys
import logic

pygame.init() # source: https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ&start_radio=1
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

cd_timer = pygame.time.Clock()
cd_timer.tick()
cd = 0
        
player_image = pygame.image.load(os.path.join("player.png")).convert_alpha()
player_image = pygame.transform.scale_by(player_image, 0.25)
player = logic.Player(0, pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), player_image)
projectiles = []

while running: # game loop cycle
    dt = clock.tick(60) / 1000
    
    for event in pygame.event.get(): # event listener
        if event.type == pygame.QUIT: # player pressed "X"
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.move(True, dt, 300)
    if keys[pygame.K_s]:
        player.move(False, dt, 300)
    if keys[pygame.K_a]:
        if keys[pygame.K_s]:
            player.rotate(False, dt, 120)
        else:
            player.rotate(True, dt, 120)
    if keys[pygame.K_d]:
        if keys[pygame.K_s]:
            player.rotate(True, dt, 120)
        else:
            player.rotate(False, dt, 120)
    if keys[pygame.K_SPACE]:
        cd_timer.tick()
        cd += cd_timer.get_time()
        if  cd > 250:
            cd = 0
            projectile = logic.Projectile(player.angle, player.pos, player)
            projectiles.append(projectile)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    for projectile in projectiles:
        delete = projectile.upd(screen, 900, dt)
        if delete:
            projectiles.remove(projectile)
    player.upd(screen)

    # for testing pygame.draw.polygon(screen, (255, 0, 0), player.upd_hitbox_points)
    # for testing pygame.draw.rect(screen, (255, 0, 0), player.rect, 2)
    
    pygame.display.flip() # pygame generates stuff on a hidden layer and then swaps it to the layer we see so it avoids screen flickering. This allows us to see the stuff after a frame

pygame.quit()

