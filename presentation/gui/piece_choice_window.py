import os
import tkinter

from tools.constants import PieceColor
from PIL import Image, ImageTk


class PieceChoiceWindow(object):
    def __init__(self, color):
        self.__window = tkinter.Tk()
        self.__window.title("Choose a piece!")
        self.__window.geometry("230x230")
        self.__window.minsize(230, 230)
        self.__window.maxsize(230, 230)

        image_color = 'white_' if color == PieceColor.WHITE else 'black_'
        image_dictionary = {(0, 0): "bishop", (0, 1): "knight", (1, 0): "rook", (1, 1): "queen"}
        relative_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        bg_colors = {(0, 0): 'white', (0, 1): 'black', (1, 0): 'black', (1, 1): 'white'}

        images = []
        for current_image in image_dictionary:
            path = relative_path + '\\assets\\' + image_color + image_dictionary[current_image] + '.png'
            resized_image = Image.open(path)
            resized_image = resized_image.resize((100, 100), Image.ANTIALIAS)

            images.append(ImageTk.PhotoImage(resized_image))
            button = tkinter.Button(self.__window, image=images[-1], height=100, width=100, bg=bg_colors[current_image[0], current_image[1]], borderwidth=7, relief=tkinter.RIDGE)
            button.grid(row=current_image[0], column=current_image[1])

        self.__window.mainloop()
