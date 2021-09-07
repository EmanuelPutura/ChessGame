import os

import pygame

from errors.exceptions import UserInputError
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


class ImageButton(pygame.sprite.Sprite):
    def __init__(self, parent, file_name, width, height, x=0, y=0):
        super().__init__()
        self.__parent = parent
        self.__file_name = file_name
        self.__width = width
        self.__height = height
        self.__x = x
        self.__y = y
        self.__rectangle = pygame.Rect(x, y, width, height)

    @property
    def parent(self):
        return self.__parent

    @property
    def rectangle(self):
        return self.__rectangle

    def update(self, event):
        return True

    def draw(self, surface):
        relative_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        image = pygame.image.load(relative_path + self.__file_name)
        image = pygame.transform.scale(image, (int(self.__width), int(self.__height)))
        image.convert()

        surface.blit(image, (self.__x, self.__y))


class BackImageButton(ImageButton):
    def __init__(self, parent, file_name, width, height, x=0, y=0):
        super().__init__(parent, file_name, width, height, x, y)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the image rectangle
            if self.rectangle.collidepoint(event.pos):
                self.parent.widgets_group.empty()
                self.parent.init_widgets()
        return True


class LoginImageButton(ImageButton):
    def __init__(self, parent, file_name, width, height, x=0, y=0):
        super().__init__(parent, file_name, width, height, x, y)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the image rectangle
            if self.rectangle.collidepoint(event.pos):
                self.parent.widgets_group.empty()
                self.parent.init_login_widgets()
        return True


class ExitImageButton(ImageButton):
    def __init__(self, parent, file_name, width, height, x=0, y=0):
        super().__init__(parent, file_name, width, height, x, y)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the image rectangle
            if self.rectangle.collidepoint(event.pos):
                return False
        return True


class PlayAsGuestImageButton(ImageButton):
    def __init__(self, parent, file_name, width, height, x=0, y=0):
        super().__init__(parent, file_name, width, height, x, y)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the image rectangle
            if self.rectangle.collidepoint(event.pos):
                self.parent.widgets_group.empty()
                self.parent.init_play_as_guest_widgets()
        return True


class DefaultImageButton(ImageButton):
    def __init__(self, parent, file_name, width, height, x=0, y=0):
        super().__init__(parent, file_name, width, height, x, y)

    def update(self, event):
        return True


class RestartImageButton(ImageButton):
    def __init__(self, parent, file_name, width, height, x=0, y=0):
        super().__init__(parent, file_name, width, height, x, y)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the image rectangle
            if self.rectangle.collidepoint(event.pos):
                self.parent.restart_game()
        return True


class Label(pygame.sprite.Sprite):
    def __init__(self, parent, text, font, width, height, x=0, y=0, text_color=Colors.WHITE.value):
        super().__init__()
        self.__parent = parent
        self.__x = x
        self.__y = y
        self.__font = font
        self.__width = width
        self.__height = height
        self.__color = text_color
        self.change_text(text, font, text_color)

    @property
    def parent(self):
        return self.__parent

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, other):
        self.change_text(other, self.__font, self.__color)

    @property
    def font(self):
        return self.__font

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def text_color(self):
        return self.__text_color

    def update(self, event):
        return True

    def change_text(self, text, font, text_color=Colors.WHITE.value):
        self.__text = font.render(text, 1, text_color)
        text_size = self.__text.get_size()
        self.__rectangle = pygame.Rect(self.__x, self.__y, self.__width, self.__height)
        self.__text_color = text_color

    def draw(self, surface, middle=False):
        text_size = self.__text.get_size()
        text_x = self.__rectangle.centerx - text_size[0] / 2
        text_y = self.__rectangle.centery - text_size[1] / 2

        if not middle:
            surface.blit(self.__text, (self.__x, self.__y))
        else:
            surface.blit(self.__text, (text_x, text_y))


class MiddleLabel(Label):
    def __init__(self, parent, text, font, width, height, x=0, y=0, text_color=Colors.WHITE.value):
        super().__init__(parent, text, font, width, height, x, y, text_color)

    def draw(self, surface, middle=False):
        super().draw(surface, True)


class TextButton(Label):
    def __init__(self, parent, text, font, width, height, x=0, y=0, text_color=Colors.WHITE.value):
        super().__init__(parent, text, font, width, height, x, y, text_color)

    def update(self, event):
        pass


class CreateAccountTextButton(TextButton):
    def __init__(self, parent, text, font, width, height, x=0, y=0, text_color=Colors.WHITE.value):
        super().__init__(parent, text, font, width, height, x, y, text_color)
        self.__rectangle = pygame.Rect(x, y, width, height)
        self.__initial_text = text
        self.__initial_text_color = text_color

    def update(self, event):
        position = pygame.mouse.get_pos()
        if self.__rectangle.x <= position[0] <= self.__rectangle.x + self.__rectangle.w and \
                self.__rectangle.y <= position[1] <= self.__rectangle.y + self.__rectangle.h:
            self.change_text(self.__initial_text, self.font, Colors.GRAY.value)
        else:
            self.change_text(self.__initial_text, self.font, self.__initial_text_color)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the image rectangle
            if self.__rectangle.collidepoint(event.pos):
                self.parent.widgets_group.empty()
                self.parent.init_account_widgets()
        return True


class TextBox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, hidden=False, text='', font=None, inactive_color=Colors.WHITE.value,
                 active_color=Colors.GRAY.value, text_color=Colors.WHITE.value):
        super().__init__()

        if font is None:
            font = pygame.font.Font(None, 20)

        self.__rectangle = pygame.Rect(x, y, width, height)
        self.__inactive_color = inactive_color
        self.__active_color = active_color
        self.__color = inactive_color
        self.__text_color = text_color
        self.__text = text
        self.__font = font
        if hidden:
            self.__text_surface = self.__font.render('*' * len(text), 1, self.__color)
        else:
            self.__text_surface = self.__font.render(text, 1, self.__color)
        self.__active = False
        self.__hidden = hidden

    @property
    def text(self):
        return self.__text

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the textBox rectangle
            if self.__rectangle.collidepoint(event.pos):
                # Toggle the active variable
                self.__active = not self.__active
            else:
                self.__active = False
            # Change the current color of the textBox
            self.__color = self.__active_color if self.__active else self.__inactive_color
        if event.type == pygame.KEYDOWN:
            if self.__active:
                if event.key == pygame.K_RETURN:
                    self.__color = self.__inactive_color
                elif event.key == pygame.K_BACKSPACE:
                    self.__text = self.__text[:-1]
                else:
                    if len(self.__text) >= 25:
                        if self.__hidden:
                            raise UserInputError('Password must have no more than 25 characters.')
                        raise UserInputError('Username must have no more than 25 characters.')
                    self.__text += event.unicode
                # Re-render the text
                if self.__hidden:
                    self.__text_surface = self.__font.render('*' * len(self.__text), 1, self.__text_color)
                else:
                    self.__text_surface = self.__font.render(self.__text, 1, self.__text_color)
        return True

    def draw(self, surface):
        text_size = self.__text_surface.get_size()
        surface.blit(self.__text_surface, (self.__rectangle.x + 5, self.__rectangle.centery - text_size[1] / 2))
        pygame.draw.rect(surface, self.__color, self.__rectangle, 1)
