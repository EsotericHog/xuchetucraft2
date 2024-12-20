from customtkinter import CTkButton
from settings import MENU_BUTTON_WIDTH, BUTTON_WIDTH, BUTTON_SMALL_WIDTH
from typing import Callable
import customtkinter as ctk
from interface.text import TEXT_BTN_DOWNLOAD, TEXT_BTN_BACK


#-----Botones-----
M_BTN_COLOR : str = "green"
DOWNLOAD_BTN_COLOR : str = "green"
BACK_BTN_COLOR : str = "red"
COLOR_RED_HOVER : str = "#ff6868"
COLOR_GREEN_HOVER : str = "lightgreen"

def default_command()->None:
    print("Botón presionado")

#Opción de menú principal
def create_menu_button(master, command : Callable[[], None], text : str = "Opción", fg_color : str = M_BTN_COLOR, hover_color : str = COLOR_GREEN_HOVER, relx : float = 0.5, rely : float = 0.5) -> None:
    option = CTkButton(master=master, text=text, width=MENU_BUTTON_WIDTH, fg_color=fg_color, font=("Consolas", 15), hover_color=hover_color, command=command, corner_radius=0)
    option.place(relx=relx, rely=rely, anchor="center")


#Botón de descarga
def create_download_button(master, command=default_command, text : str = TEXT_BTN_DOWNLOAD, fg_color : str = DOWNLOAD_BTN_COLOR, hover_color : str = COLOR_GREEN_HOVER, relx : float = 0.5, rely : float = 0.5) -> None:
    button = CTkButton(master=master, text=text, width=BUTTON_WIDTH, fg_color=fg_color, font=("Consolas", 16), hover_color=hover_color, command=command)
    button.place(relx=relx, rely=rely, anchor="center")


#Botón de volver a la página anterior
def create_back_button(master, command : Callable[[], None], text : str = TEXT_BTN_BACK, fg_color : str = BACK_BTN_COLOR, relx : float = 0.9, rely : float = 0.875, corner_radius=None) -> None:
    button = CTkButton(master=master, text=text, width=BUTTON_SMALL_WIDTH, fg_color=fg_color, font=("Consolas", 15), hover_color=COLOR_RED_HOVER, corner_radius=corner_radius, command=command)
    button.place(relx=relx, rely=rely, anchor="center")
    return button


#Botón básico
def create_button(master, command=default_command, text : str = TEXT_BTN_BACK, fg_color : str = None, hover_color : str = None, relx : float = 0.9, rely : float = 0.875, corner_radius = None) -> None:
    button = CTkButton(master=master, text=text, width=BUTTON_SMALL_WIDTH, fg_color=fg_color, font=("Consolas", 15), hover_color=hover_color, corner_radius=corner_radius, command=command)
    button.place(relx=relx, rely=rely, anchor="center")
    return button


#-----Textos-----
def create_title_page(master, text : str = "Título de página", relx : float = 0.5, rely : float = 0.06) -> None:
    title = ctk.CTkLabel(master=master, text=text, font=("Consolas", 18))
    title.place(relx=relx, rely=rely, anchor="center")

def create_subtitle_page(master, text : str = "Subtítulo", relx : float = 0.5, rely : float = 0.1) -> None:
    subtitle = ctk.CTkLabel(master=master, text=text, font=("Consolas", 16))
    subtitle.place(relx=relx, rely=rely, anchor="center")
    return subtitle



class CustomCheckBox(ctk.CTkCheckBox):
    def __init__(self, master=None, extra_attribute=None, **kwargs):
        super().__init__(master, **kwargs)
        self.extra_attribute = extra_attribute