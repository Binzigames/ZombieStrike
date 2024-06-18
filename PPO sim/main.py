import sys
import pygame
import time
import config
import functions
import clases
import common

# Initialize Pygame
try:
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
except Exception as e:
    print(f"Failed to initialize Pygame: {e}")
    sys.exit(1)

# Load images
try:
    bullet_image = pygame.image.load("img/bullet-export.png").convert_alpha()
    bullet_update = pygame.image.load("img/BulletUpgradeCan.png").convert_alpha()
    bullet_update_cant = pygame.image.load("img/BulletUpgradeCant.png").convert_alpha()
    icon = pygame.image.load("img/icon.png").convert_alpha()
    pause_button_image = pygame.image.load("img/pause_button.png").convert_alpha()
    security_update = pygame.image.load("img/SecurityUpgradeCan.png").convert_alpha()
    security_update_cant = pygame.image.load("img/securityUpgradeCant.png").convert_alpha()
except pygame.error as e:
    print(f"Failed to load images: {e}")
    pygame.quit()
    sys.exit(1)

# Additional initialization
try:
    config.lives += 1
    functions.Window_name_Change(config.title)
    config.c = functions.c_r
except Exception as e:
    print(f"Failed to load scripts: {e}")
    pygame.quit()
    sys.exit(1)

# Load sounds
try:
    turret_shot_sfx = pygame.mixer.Sound("Sds/Turret_SFX_var1_MP3.mp3")
    purchase_sfx = pygame.mixer.Sound("Sds/Purchase_SFX_v2.mp3")
    pause_sfx = pygame.mixer.Sound("Sds/Menu_open_v2_LessVol.mp3")
except pygame.error as e:
    print(f"Failed to load sounds: {e}")
    pygame.quit()
    sys.exit(1)

# Set window icon
functions.Window_set_icon(icon)

# Import menu and open it
import menu
menu.open_menu()

# Calculate background position for centering
bg_rect = config.BG.get_rect(center=(config.WINDOW_SIZE[0] / 2, config.WINDOW_SIZE[1] / 2))

# Create button instances
upgrade_turret = clases.ButtonUpgradeTurret(0, 60, bullet_update, bullet_update_cant, purchase_sfx)
upgrade_protection = common.ButtonUpgradeSecurity(0, 100, security_update, security_update_cant, purchase_sfx)
pause_button = clases.PauseButton(710, 0, pause_button_image, (255, 255, 255), pause_button_image.get_width(), pause_button_image.get_height(), pause_sfx)

# Initialize groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
speder_enemy_group = pygame.sprite.Group()

# Define the Bullet class
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

# Define the Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 20])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = -0.5

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right <= 10:
            self.kill()
            config.lives -= 1
            if config.lives <= 0:
                game_over()

    @staticmethod
    def get_enemy_count():
        return len(enemy_group)

# Enemy spawning function
def spawn_enemy():
    new_enemy = Enemy(config.WINDOW_SIZE[0], 464)
    enemy_group.add(new_enemy)

# Define the Enemy_speder class
class Enemy_speder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 20])
        self.image.fill((255, 250, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = -2

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right <= 10:
            self.kill()
            config.lives -= 1
            if config.lives <= 0:
                game_over()

    @staticmethod
    def get_enemy_count():
        return len(speder_enemy_group)

def spawn_enemy_speder():
    new_enemy = Enemy_speder(config.WINDOW_SIZE[0], 464)
    speder_enemy_group.add(new_enemy)

# Enemy spawner class
class EnemySpawner:
    def __init__(self, interval):
        self.interval = interval
        self.last_spawn_time = time.time()

    def update(self):
        current_time = time.time()

        # Check if enough time has passed to spawn a new enemy
        if current_time - self.last_spawn_time >= self.interval:
            spawn_enemy()
            self.last_spawn_time = current_time
        if int(config.zomdie_kiled) == 100:
            spawn_enemy()


# Main game update function
def game_update():
    fps = 60
    clock = pygame.time.Clock()
    last_bullet_time = time.time()
    bullet_interval = config.bullet_interval

    enemy_spawner = EnemySpawner(config.interval_zombie)

    running = True
    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if upgrade_turret.check_click(event.pos):
                            upgrade_turret.OnClick(config)
                        if upgrade_protection.check_click(event.pos):
                            upgrade_protection.OnClick(config)
                        if pause_button.check_click(event.pos):
                            pause_button.OnClick(config)

            # Check if in menu
            if config.InMenu:
                continue

            config.window.fill((0, 0, 0))

            # Display background
            config.window.blit(config.BG, bg_rect.topleft)

            if not config.paused:
                current_time = time.time()
                if current_time - last_bullet_time >= bullet_interval:
                    turret_shot_sfx.play()
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

                # Update button states
                upgrade_turret.update()
                upgrade_protection.update()

                # Update enemy spawner
                enemy_spawner.update()

            else:
                pause_button.draw_pause_text(config.window)

            # Draw upgrade buttons and pause button
            upgrade_turret.draw(config.window)
            upgrade_protection.draw(config.window)
            pause_button.draw(config.window)

            # Display money and other info
            functions.Draw_text("money: " + str(config.money), config.basic_font, (255, 255, 255), 0, 10)
            functions.Draw_text("cost: 100", config.basic_font, (255, 255, 255), 50, 70)
            functions.Draw_text("name: Update Bullet", config.basic_font, (255, 255, 255), 50, 80)
            functions.Draw_text("cost: 50", config.basic_font, (255, 255, 255), 50, 110)
            functions.Draw_text("name: Update protection", config.basic_font, (255, 255, 255), 50, 120)
            functions.Draw_text("V 0.9", config.basic_font, (255, 255, 255), 0, 500)
            functions.Draw_text("killed zombie: " + str(config.zomdie_kiled), config.basic_font, (255, 255, 255), 0, 30)
            functions.Draw_text("Lives: " + str(config.lives), config.basic_font, (255, 255, 255), 0, 50)
            pygame.display.update()
            clock.tick(fps)
        except Exception as e:
            print(f"Error occurred: {e}")
            running = False

def game_over():
    # Remove all enemies
    enemy_group.empty()

    # Reset game variables
    config.lives = 1  # Adjust as per your initial lives count
    config.money = 0
    config.zomdie_kiled = 0
    config.InMenu = True
    menu.open_menu()

# Start
game_update()

# Clean up and exit
pygame.quit()
sys.exit()
