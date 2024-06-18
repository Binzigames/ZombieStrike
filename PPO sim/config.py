import pygame
pygame.init()
T = True
F = False

#zombie sys

zomdie_kiled =0
celected_money = 50
interval_zombie = 5

#shop sys

money = 100
required_Up_Turet = 100

#bullet sys

bullet_speed= 5
bullet_interval = 6
# fonts
font_path = "prstart.ttf"
font_size = 10
basic_font = pygame.font.Font(font_path, font_size)

font_size_heder = 20
heder_font = pygame.font.Font(font_path, font_size_heder)
#player config
lives = 0
WINDOW_SIZE = (800, 600)
window = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
title = "ZombieStrike0.9"
paused = F
InMenu = T
#BGs
BG = pygame.image.load("img/BG.png")

#code
c = "YBkfjrkjfrjh9458023or_3049294foirgjeirgh"