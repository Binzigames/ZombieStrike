# common.py
import pygame
import config

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_image, bullet_speed=5, direction=(1, 0)):
        super().__init__()
        self.image = pygame.transform.scale(bullet_image, (5, 5))
        self.rect = self.image.get_rect(center=(x, y))
        self.speedBullet = bullet_speed
        self.direction = pygame.math.Vector2(direction).normalize()

    def update(self):
        self.rect.x += self.direction.x * self.speedBullet
        self.rect.y += self.direction.y * self.speedBullet
        if self.rect.right < 0 or self.rect.left > 800:  # Assuming 800 is window width
            self.kill()

class ButtonUpgradeSecurity:
    def __init__(self, x, y, image_enabled, image_disabled, sfx):
        self.image_enabled = image_enabled
        self.image_disabled = image_disabled
        self.rect = self.image_enabled.get_rect(topleft=(x, y))
        self.sfx = sfx
        self.enabled = True

    def check_click(self, pos):
        return self.rect.collidepoint(pos)

    def OnClick(self, event):
        if self.enabled:
            if self.try_upgrade():
                self.show_feedback(success=True)
            else:
                self.show_feedback(success=False)
        else:
            self.show_feedback(success=False)

    def try_upgrade(self):
        if config.money >= 50:
            config.money -= 50
            config.interval_zombie -= 0.1
            config.celected_money -= 1
            self.sfx.play()
            config.lives += 1
            return True
        return False

    def update(self):
        self.enabled = config.money >= 50

    def draw(self, window):
        if self.enabled:
            window.blit(self.image_enabled, self.rect.topleft)
        else:
            window.blit(self.image_disabled, self.rect.topleft)

    def show_feedback(self, success):
        if success:
            print("Upgrade successful!")  # Replace with actual feedback mechanism
        else:
            print("Upgrade failed!")  # Replace with actual feedback mechanism
