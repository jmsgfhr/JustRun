from PPlay.sprite import *
import random


class Slime:
    def __init__(self):
        self.img = Sprite("Sprites/bad.png", 4)
        self.spike_img = Sprite("Sprites/spikes.png")
        self.speed = 100
        self.slimes = []
        self.slime_platform = []
        self.slimes_limits_x = []
        self.slimes_x = []
        self.slimes_y = []
        self.slime_speed = []
        self.slime_dead = []
        self.plat_x = []
        self.plat_y = []
        self.spikes = []
        self.spikes_y = []
        self.spikes_x = []
        self.spike_plat = []

    def reset(self, ground):
        self.speed = 100
        self.slimes = []
        self.slime_platform = []
        self.slimes_limits_x = []
        self.slimes_x = []
        self.slimes_y = []
        self.slime_speed = []
        self.slime_dead = []
        self.plat_x = []
        self.plat_y = []
        self.spikes = []
        self.spikes_y = []
        self.spikes_x = []
        self.spike_plat = []
        self.set_random_mobs(ground, 4, 2)

    def set_random_mobs(self, platforms, n_mobs, n_spikes):
        for i in range(n_mobs):
            self.slimes.append(self.img)
            self.slimes_limits_x.append([])
            rand = random.randint(1, (len(platforms.platforms) - 2))
            while platforms.platforms[rand][0] == 0:
                rand = random.randint(1, (len(platforms.platforms) - 1))
            self.slime_platform.append(rand)
            self.slimes_limits_x[i].append(platforms.plat_x[rand][0])
            self.slimes_limits_x[i].append(platforms.plat_x[rand][-1])
            self.slimes_y.append(platforms.plat_y[rand][0] - self.img.height)
            self.plat_y = platforms.plat_y
            self.slime_speed.append(1)
            self.slimes_x.append(self.slimes_limits_x[i][0])
            self.slime_dead.append(False)
        for j in range(n_spikes):
            rand = random.randint(1, (len(platforms.platforms) - 2))
            while rand in self.slime_platform or rand in self.spike_plat  \
                    or platforms.platforms[rand][0] == 0:
                rand = random.randint(1, (len(platforms.platforms) - 1))
            if not len(platforms.plat_x) == 2:
                self.spikes.append(self.spike_img)
            else:
                self.spikes.append(0)
            self.spike_plat.append(rand)
            self.spikes_x.append(random.choice(platforms.plat_x[rand]))
            self.spikes_y.append(platforms.plat_y[rand][0] - self.spike_img.height)

    def set_spike(self):
        show_sp = [False, False, True]
        show_spike = random.choice(show_sp)
        if len(self.plat_x[-1]) > 2 and show_spike:
            self.spikes.append(self.spike_img)
            self.spike_plat.append(self.plat_x.index(self.plat_x[-1]))
            self.spikes_x.append(self.plat_x[-1][random.randint(1, len(self.plat_x[-1]) - 1)])
            self.spikes_y.append(self.plat_y[-1][-1] - self.spike_img.height)

    def set_mobs(self):
        show_sl = [True, True, False]
        show_slime = random.choice(show_sl)
        if show_slime:
            self.slimes_limits_x.append([])
            self.slimes.append(self.img)
            self.slime_platform.append(len(self.plat_x) - 1)
            self.slimes_limits_x[-1].append(self.plat_x[-1][0])
            self.slimes_limits_x[-1].append(self.plat_x[-1][-1])
            self.slime_speed.append(1)
            self.slimes_y.append(self.plat_y[-1][0] - self.img.height)
            self.slimes_x.append(self.slimes_limits_x[-1][0])
            self.slime_dead.append(False)
        else:
            self.set_spike()

    def update_limits(self, new_list_x):
        for i in range(len(self.slimes)):
            if not new_list_x[self.slime_platform[i]] == []:
                self.slimes_limits_x[i][0] = new_list_x[self.slime_platform[i]][0]
                self.slimes_limits_x[i][1] = new_list_x[self.slime_platform[i]][-1]
            else:
                self.slimes[i] == 0
        self.plat_x = new_list_x

    # Draw mob
    def draw(self, player):
        for i in range(len(self.slimes)):
            if not self.slimes[i] == 0:
                if self.slime_speed[i] > 0:
                    self.slimes[i].set_curr_frame(2)
                else:
                    self.slimes[i].set_curr_frame(1)
                self.slimes[i].x = self.slimes_x[i]
                self.slimes[i].y = self.slimes_y[i]
                if player.collision_mob(self.slimes[i], self.slime_dead[i]) or self.slime_dead[i]:
                    self.slime_dead[i] = True
                    self.slime_speed[i] = 0
                    self.slimes[i].set_curr_frame(0)
                self.slimes[i].draw()
        for i in range(len(self.spikes)):
            self.spikes[i].x = self.spikes_x[i]
            self.spikes[i].y = self.spikes_y[i]
            player.collision_spike(self.spikes[i])
            print(len(self.spikes))
            if len(self.spikes) == 3:
                print(self.spikes)
            self.spikes[i].draw()

    def walk(self):
        for i in range(len(self.slimes)):
            if self.slimes[i] != 0:
                self.slimes_x[i] += self.slime_speed[i]
                if self.slimes_x[i] > self.slimes_limits_x[i][1]:
                    self.slimes[i].x = self.slimes_limits_x[i][1] - 10
                    self.slime_speed[i] = -self.slime_speed[i]
                elif self.slimes_x[i] < self.slimes_limits_x[i][0]:
                    self.slimes[i].x = self.slimes_limits_x[i][0] + 10
                    self.slime_speed[i] = -self.slime_speed[i]

    def debug(self):
        print(self.slimes)
        print(self.slimes_x)
        print(self.slimes_y)
        print(self.slimes_limits_x)
