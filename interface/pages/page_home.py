import customtkinter as ctk
from PIL import Image
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, BANNER_PATH, BACKGROUND_IMAGE
from interface.components import create_menu_button, create_title_page, create_back_button, create_button
from tkinter import messagebox
from backend.verifications import Verificator
from interface.text import (TEXT_HOME_TITLE,
                            TEXT_MENU_OPTION_1,
                            TEXT_MENU_OPTION_2,
                            TEXT_MENU_OPTION_3,
                            TEXT_MENU_OPTION_4,
                            TEXT_MENU_OPTION_5,
                            TEXT_MENU_OPTION_6,
                            TEXT_MENU_OPTION_7,
                            TEXT_MENU_OPTION_PREF,
                            TEXT_MENU_EXIT,
                            TEXT_MENU_LOCAL_MC)

#PÁGINA PRINCIPAL PARA EL MENÚ DE OPCIONES
class PageHome(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        #Label de confirmación (error/éxito)
        self.answer_text = ctk.CTkLabel(master=self, text="")
        self.answer_text.place(relx=0.5, rely=0.2, anchor="center")


        #Cargar banner
        self.banner_image = Image.open(BANNER_PATH)
        #self.banner_photo = ImageTk.PhotoImage(self.banner_image)
        self.banner_photo = ctk.CTkImage(light_image=self.banner_image, size=(900,100))

        #CTKLabel para banner
        self.banner_label = ctk.CTkLabel(master=self, image=self.banner_photo, text="")
        self.banner_label.grid(row=0, column=0, columnspan=controller.total_columns, sticky="ew")


        #CTKFrame para el body
        self.body_frame : ctk.CTkFrame = ctk.CTkFrame(master=self, width=WINDOW_WIDTH, height=(WINDOW_HEIGHT - 50))
        self.body_frame.grid(column=0, row=1, columnspan=controller.total_columns)


        ##Cargar imagen lateral
        #self.leftimage_image = Image.open(LEFT_IMAGE)
        ##self.banner_photo = ImageTk.PhotoImage(self.banner_image)
        #self.leftimage_photo = ctk.CTkImage(light_image=self.leftimage_image, size=(int(798*0.456),int(1080*0.456)))
        #
        ##CTKLabel para imagen lateral
        #self.leftimage_label = ctk.CTkLabel(master=self.body_frame, image=self.leftimage_photo, text="")
        #self.leftimage_label.place(relx=0.0, rely=0.461, anchor="w")


        #Título principal
        self.title : ctk.CTkLabel = create_title_page(master=self.body_frame, text=TEXT_HOME_TITLE, relx=0.7)


        ##Cargar imagen de fondo
        self.bg_image_image = Image.open(BACKGROUND_IMAGE)
        self.bg_image_photo = ctk.CTkImage(light_image=self.bg_image_image, size=(int(1280*0.71),int(720*0.71)))
        #CTKLabel para imagen lateral
        self.bg_image_label = ctk.CTkLabel(master=self.body_frame, image=self.bg_image_photo, text="")
        self.bg_image_label.place(relx=0.5, rely=0.461, anchor="center")


        #Menú principal
        self.option : ctk.CTkButton = create_menu_button(self.body_frame, text=TEXT_MENU_OPTION_1, rely=0.1, command=self.go_page_modloader)
        self.option : ctk.CTkButton = create_menu_button(self.body_frame, text=TEXT_MENU_OPTION_2, rely=0.19, command=lambda: controller.show_frame("PageMods"))
        self.option : ctk.CTkButton = create_menu_button(self.body_frame, text=TEXT_MENU_OPTION_3, rely=0.28, command=lambda: controller.show_frame("PageShaders"))
        self.option : ctk.CTkButton = create_menu_button(self.body_frame, text=TEXT_MENU_OPTION_4, rely=0.37, command=lambda: controller.show_frame("PageResourcepacks"))
        self.option : ctk.CTkButton = create_menu_button(self.body_frame, text=TEXT_MENU_OPTION_5, rely=0.46, command=lambda: controller.show_frame("PageAddServer"))
        self.option : ctk.CTkButton = create_menu_button(self.body_frame, text=TEXT_MENU_OPTION_6, rely=0.55, command=lambda: controller.show_frame("PageDHLOD"))
        self.option : ctk.CTkButton = create_menu_button(self.body_frame, text=TEXT_MENU_OPTION_7, rely=0.64, command=lambda: controller.show_frame("PageRam"))
        self.option : ctk.CTkButton = create_menu_button(self.body_frame, text=TEXT_MENU_OPTION_PREF, rely=0.73, command=lambda: controller.show_frame("PagePref"), fg_color=None, hover_color=None)
        self.option : ctk.CTkButton = create_back_button(self.body_frame, text=TEXT_MENU_EXIT, corner_radius=0, command=lambda: controller.destroy())
        self.option : ctk.CTkButton = create_button(self.body_frame, text=TEXT_MENU_LOCAL_MC, rely=0.875, relx=0.725, corner_radius=0, command=self.go_mc_folder_path)
        #self.option : ctk.CTkButton = create_menu_button(self.body_frame, text=TEXT_MENU_OPTION_MY, rely=0.8, command=lambda: controller.show_frame("PageAdmin"), fg_color=None, hover_color=None)

    def show_msg(self) -> None:
        messagebox.showinfo("Confirmación", "La tarea se realizó correctamente.")

    def go_page_modloader(self) -> None:
        Verificator.verificate_vanilla_installation()
        self.controller.show_frame("PageFabric")

    def go_mc_folder_path(self) -> None:
        Verificator.validate_game_directory()