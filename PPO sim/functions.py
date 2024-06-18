import pygame
import config
def Draw_text(text, font, color, X, Y):
    img = font.render(text, True, color)
    config.window.blit(img, (X, Y))
def  Window_name_Change(title):
    pygame.display.set_caption(title)

def Window_set_icon(icon):
    pygame.display.set_icon(icon)




c_r = "YBkfjrkjfrjh9458023or_3049294foirgjeirgh"