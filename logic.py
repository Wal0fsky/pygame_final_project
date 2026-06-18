import pygame

def move_player(isForward, player, dt):
    movement = pygame.Vector2()
    movement.from_polar((300 * dt, player.angle))

    if isForward:
        player.pos += movement
    else:
        player.pos -= movement

def rotate_player(isLeft, player, dt):
    if isLeft: # vertical screen is inverted... why bruv
        player.angle -= dt * 120 
        player.image = pygame.transform.rotate(player.original_image, -1 * (player.angle))
        
    else:
        player.angle += dt * 120
        player.image = pygame.transform.rotate(player.original_image, -1 * (player.angle))
    # transform the figure once we have one