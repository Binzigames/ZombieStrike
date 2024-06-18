import pygame
import config

class ButtonUpgradeTurret:
    def __init__(self, x, y, image_enabled, image_disabled, sfx):
        self.image_enabled = image_enabled
        self.image_disabled = image_disabled
        self.rect = self.image_enabled.get_rect(topleft=(x, y))
        self.sfx = sfx
        self.enabled = True

    def check_click(self, pos):
        return self.rect.collidepoint(pos)

    def OnClick(self, config):
        if self.enabled and config.money >= 100:
            config.money -= 100
            self.sfx.play()
            config.bullet_interval -= 1
            config.interval_zombie -= 0.1
            config.celected_money -= 1
            self.show_feedback(success=True)
        else:
            self.show_feedback(success=False)

    def update(self):
        self.enabled = config.money >= 100

    def draw(self, window):
        if self.enabled:
            window.blit(self.image_enabled, self.rect.topleft)
        else:
            window.blit(self.image_disabled, self.rect.topleft)

    def show_feedback(self, success):
        if success:
            print("Turret upgrade successful! Bullet speed increased and interval decreased.")
        else:
            print("Not enough money or button disabled.")

class PauseButton:
    def __init__(self, x, y, image,  color, width, height , sfx ):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.color = color
        self.width = width
        self.height = height
        self.enabled = True
        self.paused = False
        self.sfx = sfx
        self.font = config.basic_font


    def check_click(self, pos):
        return self.rect.collidepoint(pos)

    def OnClick(self, config):
        if self.enabled:
            self.paused = not self.paused
            config.paused = self.paused
            self.sfx.play()

    def draw(self, window):
        window.blit(self.image, self.rect.topleft)
    def draw_pause_text(self, window):
        if self.paused:
            pause_text = self.font.render("Game is paused, press the button to continue", True, (255, 255, 255))
            window.blit(pause_text, (config.WINDOW_SIZE[0] // 2 - pause_text.get_width() // 2, config.WINDOW_SIZE[1] // 2 - pause_text.get_height() // 2))

