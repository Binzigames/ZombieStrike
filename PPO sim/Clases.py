import pygame
import config
import time
class  Button():
    def __init__(self , X, Y ,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (X, Y)


class ButtonUpgradeTurret:
    def __init__(self, x, y, image_normal, image_insufficient):
        self.image_normal = image_normal
        self.image_insufficient = image_insufficient
        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.last_update_time = 0
        self.update_interval = 1  # Time to show insufficient image in seconds

    def OnClick(self, config):
        if config.money >= 100:
            config.money -= 100
            config.bullet_speed += 1
            config.bullet_interval -= 3
            self.image = self.image_normal
        else:
            self.image = self.image_insufficient
            self.last_update_time = time.time()

    def update(self):
        if self.image == self.image_insufficient and (time.time() - self.last_update_time) > self.update_interval:
            self.image = self.image_normal

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)