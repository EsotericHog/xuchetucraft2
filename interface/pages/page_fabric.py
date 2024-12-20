import customtkinter as ctk
from interface.text import TEXT_FABRIC_TITLE, TEXT_FABRIC_DESCRIPTION
from settings import FABRIC_LOGO_PATH
from PIL import ImageTk, Image
from interface.components import create_title_page, create_download_button, create_back_button
from backend.tasks import option_1

class PageFabric(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.title : ctk.CTkLabel = create_title_page(master=self, text=TEXT_FABRIC_TITLE, relx=0.5)

        image : Image = Image.open(FABRIC_LOGO_PATH)
        width, height = image.size
        self.image : ctk.CTkImage = ctk.CTkImage(light_image=image, size=(width,height))
        
        self.label_ctk_image : ctk.CTkLabel = ctk.CTkLabel(master=self, image=self.image, text="")
        self.label_ctk_image.place(relx=0.2, rely=0.4, anchor="center")

        # Configurar el widget CTkLabel para que se ajuste al contenido
        #self.label_ctk_image.configure(width=resized_image.width, height=resized_image.height)

        self.text_content : ctk.CTkLabel = ctk.CTkLabel(master=self, width=400, text=TEXT_FABRIC_DESCRIPTION, wraplength=400, anchor="w", font=("Consolas", 16))
        self.text_content.place(relx=0.4, rely=0.25)

        self.download_button :ctk.CTkButton = create_download_button(master=self, command=option_1, relx=0.65, rely=0.625)
        self.back_button :ctk.CTkButton = create_back_button(master=self, command=lambda: controller.show_frame("PageHome"))