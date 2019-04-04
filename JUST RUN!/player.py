from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.collision import *
from pygame.locals import *


# class name
class Player(object):
    def __init__(self):
        # Player
        self.img = Sprite("Sprites/sheet.png", 27)
        self.hud = GameImage("Sprites/hud_p1.png")
        self.hud.set_position(40, 50)
        self.heart_1 = Sprite("Sprites/heart_sheet.png", 2)
        self.heart_1.set_position(100, 50)
        self.player_speed = 0
        self.player_speedl = 0
        self.jump = 0
        self.jump_val = 0
        self.acel = 0.6
        self.max_speed = 5
        self.lives = 1
        self.jump_tick = True
        self.walking = False
        self.falling = True
        self.img.set_total_duration(1200)
        self.img.set_sequence(13, 23)
        self.img.set_sequence(0, 10)
        self.side = ""
        self.hurt = False
        self.dead = False
        self.img.set_position(30, 0)
        self.score = 0
        # Numeros do placar
        self.num_1 = Sprite("Sprites/spritenum.png", 10)
        self.num_2 = Sprite("Sprites/spritenum.png", 10)
        self.num_3 = Sprite("Sprites/spritenum.png", 10)

    def reset(self):
        # Player
        self.img = Sprite("Sprites/sheet.png", 27)
        self.hud = GameImage("Sprites/hud_p1.png")
        self.hud.set_position(40, 50)
        self.heart_1 = Sprite("Sprites/heart_sheet.png", 2)
        self.heart_1.set_position(100, 50)
        self.player_speed = 0
        self.player_speedl = 0
        self.jump = 0
        self.jump_val = 0
        self.acel = 0.6
        self.max_speed = 5
        self.lives = 1
        self.jump_tick = True
        self.walking = False
        self.falling = True
        self.img.set_total_duration(1200)
        self.img.set_sequence(13, 23)
        self.img.set_sequence(0, 10)
        self.side = ""
        self.hurt = False
        self.dead = False
        self.img.set_position(30, 0)
        self.score = 0

    def score_draw(self):
        num1 = int(self.score//100)
        num2 = int(self.score//10 - num1*10)
        num3 = int(self.score - (num1*100 + num2*10))
        self.num_1.set_position(480, 300)
        self.num_1.set_curr_frame(num1)
        self.num_2.set_position(500, 300)
        self.num_2.set_curr_frame(num2)
        self.num_3.set_position(520, 300)
        self.num_3.set_curr_frame(num3)
        self.num_1.draw()
        self.num_2.draw()
        self.num_3.draw()
        print(num1, num2, num3)

    # Gravity
    def gravity(self):
        self.img.y += 8
        self.img.y += self.jump
        if self.img.y - self.jump_val < -220:
            self.jump = 0
            self.falling = True

    # Solid object
    def solid(self, floor):
        if (self.img.y + self.img.height == floor.y) and (self.falling or self.walking) and \
                (self.img.x + self.img.width >= floor.x and self.img.x <= floor.x + 70) and not self.hurt:
            self.img.y -= 8
            self.jump_tick = True
            self.falling = False
            self.walking = True

    # Draw
    def draw(self):
        self.img.update()
        if self.lives == 0:
            self.heart_1.set_curr_frame(1)
        self.heart_1.draw()
        self.hud.draw()

    # Move
    def move(self, keyboard, map, swindow, camera):
        backgrounds = map.get_backgrounds()
        background1 = backgrounds[0]
        background2 = backgrounds[1]

        # Jump
        if keyboard.key_pressed("UP") and not self.hurt and self.jump_tick:
            self.jump_val = self.img.y
            self.jump = -15
            self.jump_tick = False
            self.falling = False
            self.walking = False
            self.draw()

        # Vector Movement
        self.img.x += self.player_speed
        self.img.x += self.player_speedl

        if self.img.x >= swindow.width/2:
            self.img.x = swindow.width/2
            if keyboard.key_pressed("RIGHT") and not self.hurt:
                self.player_speed += self.acel
                if self.player_speed > self.max_speed:
                    self.player_speed -= self.acel
                if not self.walking:
                    self.img.set_curr_frame(12)
                    self.img.draw()
                else:
                    if not self.img.get_curr_frame() in range(13, 23):
                        self.img.set_curr_frame(13)
                        self.img.draw()
                self.side = "R"
                self.score += 0.1
            camera.move_camera(-self.player_speed)

        # Right movement
        if keyboard.key_pressed("RIGHT")and not self.hurt:
            if not self.walking:
                self.img.set_curr_frame(12)
                self.img.draw()
            else:
                if not self.img.get_curr_frame() in range(13, 23):
                    self.img.set_curr_frame(13)
                self.img.draw()
            self.player_speed += self.acel
            if self.player_speed > self.max_speed:
                self.player_speed -= self.acel
            if self.img.x < 0:
                self.player_speed = 0
                self.img.x = 0
            self.side = "R"
        elif keyboard.key_pressed("LEFT") and self.img.x > 0 and not self.hurt:
            self.img.draw()
            self.player_speedl -= self.acel
            if self.player_speedl < -self.max_speed:
                self.player_speedl += self.acel
            if not self.walking:
                self.img.set_curr_frame(24)
                self.img.draw()
            else:
                if not self.img.get_curr_frame() in range(0, 10):
                    self.img.set_curr_frame(0)
                    self.img.draw()
            self.side = "L"

        if not keyboard.key_pressed("RIGHT") and not self.hurt:
            self.player_speed -= self.acel/2
            if self.player_speed < 0:
                self.player_speed = 0

        if not keyboard.key_pressed("LEFT") and not self.hurt:
            self.player_speedl += self.acel/2
            if self.player_speedl > 0:
                self.player_speedl = 0
        if self.img.x <= 0:
            if not self.walking:
                self.img.x = 0
            if self.img.x < 0:
                self.player_speed = 0
            self.img.draw()

        if not keyboard.key_pressed("LEFT") and not keyboard.key_pressed("RIGHT") and not self.hurt:
            if not self.walking:
                if self.side == "L":
                    self.img.set_curr_frame(24)
                    self.img.draw()
                else:
                    self.img.set_curr_frame(12)
                    self.img.draw()
            else:
                self.img.set_curr_frame(11)
                self.img.draw()

        if self.hurt:
            self.player_speedl = 0
            self.player_speed = 0

        # Rolling Background
        if background1.x <= 0:
            background2.x = 0
            background1.x = background2.width
        elif background2.x >= 0:
            background1.x = 0
            background2.x = -background1.width

        # Respawn
        if self.img.y > swindow.height:
            self.img.y = 0
            self.hurt = False
            self.lives -= 1
            print(self.score)

    def collision_mob(self, slime, slime_dead):
        if not slime_dead and not self.dead:
            if Collision.collided(self.img, slime) and not self.falling:
                self.img.set_curr_frame(12)
                self.img.draw()
                self.hurt = True
            elif Collision.collided(self.img, slime) and self.falling and not self.hurt:
                self.score += 10
                return True

    def collision_spike(self, sp):
        if not self.dead:
            if Collision.collided(self.img, sp):
                self.img.set_curr_frame(12)
                self.img.draw()
                self.hurt = True