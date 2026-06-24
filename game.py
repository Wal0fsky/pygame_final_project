import pygame
import os
import sys
import logic
import random

pygame.init() # source: https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ&start_radio=1
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
score = 0

cd_timer = pygame.time.Clock()
cd_timer.tick()
cd = 0

enemy_timer = pygame.time.Clock()
enemy_timer.tick()
enemy_cooldown = random.randint(2000, 5000)
enemy_time = 0
enemies = []
enemy_image = pygame.image.load(os.path.join("enemy.png")).convert_alpha()
enemy_image = pygame.transform.scale_by(enemy_image, 0.1875)

player_image = pygame.image.load(os.path.join("player.png")).convert_alpha()
player_image = pygame.transform.scale_by(player_image, 0.1875)
player = logic.Player(0, pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), player_image)
projectiles = []

while running: # game loop cycle
        
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    dt = clock.tick(60) / 1000
    enemy_time += enemy_timer.tick()
    
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

    for projectile in projectiles:
        delete = projectile.upd(screen, 900, dt)
        if delete:
            projectiles.remove(projectile)

    if enemy_time >= enemy_cooldown:
        enemy_cooldown = random.randint(2000, 5000)
        enemy_time = 0

        is_y = random.randint(0, 1)
        if is_y == 1:
            x_pos = 0
            y_pos = random.randint(0, screen.get_height())
        else:
            y_pos = 0
            x_pos = random.randint(0, screen.get_width())

        enemy = logic.Enemy(0, pygame.Vector2(x_pos, y_pos), enemy_image)
        enemies.append(enemy)
    
    for enemy in enemies:
        enemy.pos.move_towards_ip(player.pos, random.randint(2, 4))
        enemy.upd(screen)

        for projectile in projectiles:
            projectile_points = [projectile.start_point, projectile.end_point]
            if enemy.check_contact(projectile_points):
                enemies.remove(enemy)
                projectiles.remove(projectile)
                score += 1

        if enemy.check_contact(player.upd_hitbox_points):
            print("you reached a score of:", score)
            running = False

    player.upd(screen)

    # for testing pygame.draw.polygon(screen, (255, 0, 0), player.upd_hitbox_points)
    # for testing pygame.draw.rect(screen, (255, 0, 0), player.rect, 2)
    
    pygame.display.flip() # pygame generates stuff on a hidden layer and then swaps it to the layer we see so it avoids screen flickering. This allows us to see the stuff after a frame

pygame.quit()

