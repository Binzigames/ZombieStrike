import pygame
import sys
import config

class Button:
    def __init__(self, text, x, y, font_path, text_size=24, button_width=None, button_height=None,
                 sprite=None, sfx=None, text_color=(255, 255, 255), hover_text_color=(255, 0, 0)):
        self.text = text
        self.x = x
        self.y = y
        self.font_path = font_path
        self.text_size = text_size
        self.text_color = text_color
        self.hover_text_color = hover_text_color
        self.sprite = sprite
        self.sfx = sfx
        self.is_hovered = False
        self.button_width = button_width
        self.button_height = button_height
        try:
            self.font = pygame.font.Font(self.font_path, self.text_size)
        except IOError:
            print(f"Error loading font: {self.font_path}")
            sys.exit(1)
        self.render_text()

    def render_text(self):
        text_surface = self.font.render(self.text, True, self.hover_text_color if self.is_hovered else self.text_color)
        if self.button_width is None:
            self.button_width = text_surface.get_width() + 20
        if self.button_height is None:
            self.button_height = text_surface.get_height() + 10
        self.rect = pygame.Rect(self.x, self.y, self.button_width, self.button_height)
        self.sprite = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.sprite.fill((255, 255, 255, 0))
        self.sprite.blit(text_surface, (10, 5))

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            self.render_text()  # Update text color on hover change
        elif event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            self.OnClick()

    def OnClick(self):
        pass  # Override in subclasses


class ExitButton(Button):
    def __init__(self, text, x, y, font_path, **kwargs):
        super().__init__(text, x, y, font_path, **kwargs)

    def OnClick(self):
        print("Exiting from game")
        if self.sfx:
            self.sfx.play()
        pygame.quit()
        sys.exit()


class PlayButton(Button):
    def __init__(self, text, x, y, font_path, **kwargs):
        super().__init__(text, x, y, font_path, **kwargs)

    def OnClick(self):
        print("Starting game")
        config.InMenu = False  # Example game state change
        if self.sfx:
            self.sfx.play()


def open_menu():
    pygame.init()
    screen = pygame.display.set_mode(config.WINDOW_SIZE)
    config.InMenu = True

    font_path = "prstart.ttf"
    font_size = 24

    button_exit = ExitButton("Exit", 10, 400, font_path, text_color=(255, 255, 255), hover_text_color=(255, 0, 0))
    button_play = PlayButton("Play", 10, 300, font_path, text_color=(255, 255, 255), hover_text_color=(0, 255, 0))

    # Load the header font
    try:
        header_font = config.heder_font
    except IOError:
        print(f"Error loading font: {font_path}")
        sys.exit(1)

    def draw_text(text, font, color, x, y):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    buttons = [button_exit, button_play]

    while config.InMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for button in buttons:
                button.handle_event(event)

        screen.fill((0, 0, 0))
        for button in buttons:
            button.draw(screen)

        # Draw the header text
        draw_text("ZombieStrike 0.9", header_font, (255, 255, 255), 10, 200)

        pygame.display.flip()


if __name__ == "__main__":
    config.InMenu = True
    config.WINDOW_SIZE = (800, 600)  # Example window size, replace with your actual config
    open_menu()
