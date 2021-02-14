import pygame


class GradientGenerator:
    def __init__(self, surface, color, gradient, rectangle=None):
        """
        :param surface: the surface to be filled with the gradient pattern
        :param color: the starting color
        :param gradient: the final color
        :param rectangle: area to be filled, by default it's the surface's rectangle
        """
        self.__surface = surface
        self.__color = color
        self.__gradient = gradient
        if rectangle is None:
            rectangle = self.__surface.get_rect()
        self.__rectangle = rectangle

    def fill_gradient(self, vertical=True, forward=True):
        """
        Fill a surface with a gradient pattern
        :param vertical: if true use vertical direction, else if false use horizontal direction
        :param forward: if true use forward direction, else if false user reverse direction
        """
        if self.__rectangle is None:
            self.__rectangle = self.__surface.get_rect()
        x1, x2 = self.__rectangle.left, self.__rectangle.right
        y1, y2 = self.__rectangle.top, self.__rectangle.bottom
        if vertical:
            height = y2 - y1
        else:
            height = x2 - x1
        if forward:
            start_color, end_color = self.__color, self.__gradient
        else:
            end_color, start_color = self.__color, self.__gradient
        rate = (
            float(end_color[0] - start_color[0]) / height,
            float(end_color[1] - start_color[1]) / height,
            float(end_color[2] - start_color[2]) / height
        )
        if vertical:
            for line in range(y1, y2):
                color = (
                    min(max(start_color[0] + (rate[0] * (line - y1)), 0), 255),
                    min(max(start_color[1] + (rate[1] * (line - y1)), 0), 255),
                    min(max(start_color[2] + (rate[2] * (line - y1)), 0), 255)
                )
                pygame.draw.line(self.__surface, color, (x1, line), (x2, line))
        else:
            for col in range(x1, x2):
                color = (
                    min(max(start_color[0] + (rate[0] * (col - x1)), 0), 255),
                    min(max(start_color[1] + (rate[1] * (col - x1)), 0), 255),
                    min(max(start_color[2] + (rate[2] * (col - x1)), 0), 255)
                )
                pygame.draw.line(self.__surface, color, (col, y1), (col, y2))
