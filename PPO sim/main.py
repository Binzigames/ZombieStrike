import sys
import pygame
import time
import config
import functions
import Clases

# Initialize Pygame
pygame.init()

# Load images
try:
    bullet_image = pygame.image.load("bullet-export.png").convert_alpha()
    bullet_update = pygame.image.load("BulletUpgradeCan.png").convert_alpha()
    bullet_update_cant = pygame.image.load("BulletUpgradeCant.png").convert_alpha()
    Bg_2 = pygame.image.load("bg_2.png").convert_alpha()
    icon = pygame.image.load("logo.ico").convert_alpha()
except pygame.error as e:
    print(f"Failed to load image: {e}")
    pygame.quit()
    sys.exit()

# Additional Initialization
try:
    config.lives += 1
    functions.Window_name_Change(config.title)
    config.c = functions.c_r  # Fixed the assignment operator
except Exception as e:
    print(f"Failed to load scripts: {e}")
    pygame.quit()
    sys.exit()

functions.Window_set_icon(icon)

# Calculate the position to center the background image
bg_rect = config.BG.get_rect(center=(config.WINDOW_SIZE[0] / 2, config.WINDOW_SIZE[1] / 2))
bg_2_rect = Bg_2.get_rect(center=(config.WINDOW_SIZE[0] / 2, config.WINDOW_SIZE[1] / 2))

# Create button instance
upgrade_turret = Clases.ButtonUpgradeTurret(0, 60, bullet_update, bullet_update_cant)

# Define Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_speed=5, direction=(1, 0)):
        super().__init__()
        self.image = pygame.transform.scale(bullet_image, (5, 5))
        self.rect = self.image.get_rect(center=(x, y))
        self.speedBullet = bullet_speed
        self.direction = pygame.math.Vector2(direction).normalize()
        bullet_group.add(self)

    def update(self):
        self.rect.x += self.direction.x * self.speedBullet
        self.rect.y += self.direction.y * self.speedBullet
        if self.rect.right < 0 or self.rect.left > config.WINDOW_SIZE[0]:
            self.kill()

# Define Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 20])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = -2

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right < 0:
            self.kill()
            config.lives -= 1
            if config.lives <= 0:
                pygame.quit()
                sys.exit("Game Over! No lives left.")

    @staticmethod
    def get_enemy_count():
        return len(enemy_group)

# Initialize groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

def spawn_enemy():
    new_enemy = Enemy(config.WINDOW_SIZE[0], 464)
    enemy_group.add(new_enemy)

# Main game update function
def game_update():
    fps = 60
    clock = pygame.time.Clock()
    last_bullet_time = time.time()
    bullet_interval = config.bullet_interval

    spawn_enemy()

    running = True
    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button click
                        if upgrade_turret.check_click(event.pos):
                            upgrade_turret.OnClick(config)

            config.window.fill((0, 0, 0))

            # Blit the backgrounds in the correct order
            config.window.blit(Bg_2, bg_2_rect.topleft)
            config.window.blit(config.BG, bg_rect.topleft)

            current_time = time.time()
            if current_time - last_bullet_time >= bullet_interval:
                # Create a bullet at the specified position (144, 468)
                Bullet(144, 468, bullet_speed=config.bullet_speed, direction=(1, 0))
                last_bullet_time = current_time

            bullet_group.update()
            enemy_group.update()

            for bullet in bullet_group:
                collided_enemies = pygame.sprite.spritecollide(bullet, enemy_group, True)
                if collided_enemies:
                    bullet.kill()
                    config.money += config.celected_money
                    config.zomdie_kiled += 1
                    if Enemy.get_enemy_count() == 0:
                        spawn_enemy()

            bullet_group.draw(config.window)
            enemy_group.draw(config.window)

            # Update the button state
            upgrade_turret.update()

            # Draw the upgrade turret button
            upgrade_turret.draw(config.window)

            # Update and display money
            functions.Draw_text("Money: " + str(config.money), config.basic_font, (255, 255, 255), 0, 10)
            # Update description
            functions.Draw_text("cost: 100", config.basic_font, (255, 255, 255), 50, 70)
            functions.Draw_text("name: Update Bullet", config.basic_font, (255, 255, 255), 50, 80)
            functions.Draw_text("V 0.5", config.basic_font, (255, 255, 255), 0, 500)
            functions.Draw_text("killed zombie: " + str(config.zomdie_kiled), config.basic_font, (255, 255, 255), 0, 30)
            functions.Draw_text("Lives: " + str(config.lives), config.basic_font, (255, 255, 255), 0, 50)
            pygame.display.update()
            clock.tick(fps)
        except Exception as e:
            print(f"An error occurred: {e}")
            running = False

# Start the game
game_update()
pygame.quit()
sys.exit()
