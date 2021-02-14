import pygame

from presentation.gui.constants import Colors
from presentation.gui.gradient_generator import GradientGenerator


class Button(pygame.sprite.Sprite):
    def __init__(self, text, font, width, height, x=0, y=0, bg=Colors.BLACK1.value, text_color=Colors.WHITE.value):
        super().__init__()
        self.__x = x
        self.__y = y
        self.__height = height
        self.__width = width
        self.change_text(text, font, bg, Colors.GRAY.value, text_color)

    def change_text(self, text, font, bg=Colors.BLACK1.value, gradient=None, text_color=Colors.WHITE.value):
        self.__text = font.render(text, 1, text_color)
        text_size = self.__text.get_size()

        self.__rectangle = pygame.Rect(self.__x, self.__y, self.__width, self.__height)
        text_x = self.__rectangle.centerx - text_size[0] / 2
        text_y = self.__rectangle.centery - text_size[1] / 2

        self.__surface = pygame.Surface((self.__width, self.__height))
        self.__surface.fill(bg)

        if gradient is not None:
            GradientGenerator(self.__surface, bg, gradient).fill_gradient(True)

        self.__surface.blit(self.__text, (text_x, text_y))

    def draw(self, surface):
        surface.blit(self.__surface, (self.__x, self.__y))


class TextButton(pygame.sprite.Sprite):
    def __init__(self, text, font, x=0, y=0, text_color=Colors.WHITE.value):
        super().__init__()
        self.__x = x
        self.__y = y
        self.change_text(text, font, text_color)

    def change_text(self, text, font, text_color=Colors.WHITE.value):
        self.__text = font.render(text, 1, text_color)
        text_size = self.__text.get_size()
        self.__rectangle = pygame.Rect(self.__x, self.__y, text_size[0], text_size[1])

    def draw(self, surface):
        text_size = self.__text.get_size()
        surface.blit(self.__text, (text_size[0], text_size[1]))


COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')


class TextBox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text='', font=None, text_color=Colors.WHITE.value):
        super().__init__()

        if font is None:
            font = pygame.font.Font(None, 20)

        self.__rectangle = pygame.Rect(x, y, width, height)
        self.__color = COLOR_INACTIVE
        self.__text = text
        self.__font = font
        self.__text_surface = self.__font.render(text, 1, self.__color)
        self.__active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the textBox rectangle
            if self.__rectangle.collidepoint(event.pos):
                # Toggle the active variable.
                self.__active = not self.__active
            else:
                self.__active = False
            # Change the current color of the textBox
            self.__color = COLOR_ACTIVE if self.__active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.__active:
                if event.key == pygame.K_RETURN:
                    self.__color = COLOR_INACTIVE
                elif event.key == pygame.K_BACKSPACE:
                    self.__text = self.__text[:-1]
                else:
                    self.__text += event.unicode
                # Re-render the text
                self.__text_surface = self.__font.render(self.__text, 1, self.__color)

    def update(self):
        # Resize the box if the text is too long
        width = max(200, self.__text_surface.get_width() + 10)
        self.__rectangle.w = width

    def draw(self, surface):
        text_size = self.__text_surface.get_size()
        surface.blit(self.__text_surface, (self.__rectangle.x + 5, self.__rectangle.centery - text_size[1] / 2))
        pygame.draw.rect(surface, self.__color, self.__rectangle, 1)
