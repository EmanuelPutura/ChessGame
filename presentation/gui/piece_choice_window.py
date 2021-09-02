import os
import tkinter

from tools.constants import PieceColor
from PIL import Image, ImageTk


class PieceChoiceWindow(object):
    def __init__(self, color):
        self.__window = tkinter.Tk()
        self.__window.title("Choose a piece!")
        self.__window.geometry("230x284")
        self.__window.minsize(230, 284)
        self.__window.maxsize(230, 284)
        self.__chosen_piece = None

        image_color = 'white_' if color == PieceColor.WHITE else 'black_'
        image_type_dictionary = {(0, 0): 'bishop', (0, 1): 'knight', (1, 0): 'rook', (1, 1): 'queen'}
        relative_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        bg_colors = {(0, 0): 'white', (0, 1): 'black', (1, 0): 'black', (1, 1): 'white'}

        images = []
        for current_image in image_type_dictionary:
            path = relative_path + '\\assets\\' + image_color + image_type_dictionary[current_image] + '.png'
            resized_image = Image.open(path)
            resized_image = resized_image.resize((100, 100), Image.ANTIALIAS)

            images.append(ImageTk.PhotoImage(resized_image))
            button = tkinter.Button(self.__window, image=images[-1], bg=bg_colors[current_image[0], current_image[1]],
                                    borderwidth=7, relief=tkinter.RIDGE, command=lambda row=current_image[0], column=current_image[1]: self.__piece_button_clicked(row, column))
            button.grid(row=current_image[0], column=current_image[1])

        ok_button = tkinter.Button(self.__window, height=2, command=self.__ok_button_clicked, text="Choose piece", borderwidth=7, relief=tkinter.RIDGE)
        ok_button.grid(row=2, column=0, columnspan=2, sticky=tkinter.EW)

        self.__window.mainloop()

    @property
    def piece(self):
        return self.__chosen_piece

    def __piece_button_clicked(self, row, column):
        image_type_dictionary = {(0, 0): 'Bishop', (0, 1): 'Knight', (1, 0): 'Rook', (1, 1): 'Queen'}
        self.__chosen_piece = image_type_dictionary[row, column]

    def __ok_button_clicked(self):
        if self.__chosen_piece is not None:
            self.__window.destroy()
