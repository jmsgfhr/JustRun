from PPlay.window import *
from player import *
from map import *
from camera import *
from slimes import *
import pygame
from PPlay.mouse import *
from pygame.locals import *

# Window config
janela = Window(1024, 512)
janela.set_title("Just RUN.")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1024, 512))

# Keyboard
teclado = Window.get_keyboard()
mouse = Mouse()

# Player
player = Player()

# Game state
game_state = 0
menu_state = 0

# Ground
ground = Map()
ground.set_random_platforms()

# Enemies
mob = Slime()
mob.set_random_mobs(ground, 4, 2)

# Camera control
camera = Screen(janela, ground, player, mob)

while True:
    if game_state == 0:
        if menu_state == 0:
            camera.bg_menu.draw()
            if camera.bt_start.draw(mouse):
                game_state = 1
            if camera.bt_about.draw(mouse):
                menu_state = 2
            if camera.bt_exit.draw(mouse):
                exit()
        elif menu_state == 2:
            camera.bg_menu_about.draw()
            if camera.bt_exit.draw(mouse):
                exit()
            if camera.bt_back.draw(mouse):
                menu_state = 0
        elif menu_state == 3:
            camera.bg_game_over.draw()
            player.score_draw()
            if camera.bt_exit.draw(mouse):
                exit()
            if teclado.key_pressed("SPACE"):
                menu_state = 0
                game_state = 0
                player.reset()
                ground.reset()
                mob.reset(ground)
                camera.reset(ground, player, mob)
    elif game_state == 1:
        ground.draw_background()
        ground.draw(player, mob)
        mob.walk()
        mob.draw(player)
        player.gravity()
        player.move(teclado, ground, janela, camera)
        player.draw()
        if player.lives == 0:
            game_state = 0
            menu_state = 3
    time_passed = clock.tick(60)
    janela.update()
