import customtkinter as ctk
from .pages.page_home import PageHome
from .pages.page_fabric import PageFabric
from .pages.page_mods import PageMods
from .pages.page_shaders import PageShaders
from .pages.page_resourcepacks import PageResourcepacks
from .pages.page_server import PageAddServer
from .pages.page_dh_lod import PageDHLOD
from .pages.page_ram import PageRam
from .pages.page_preferences import PagePref
from settings import (
    APP_NAME,
    APP_VERSION,
    ICONBITMAP_PATH,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_X_POSITION,
    WINDOW_Y_POSITION,
    WINDOW_X_RESIZABLE,
    WINDOW_Y_RESIZABLE
    )

class App(ctk.CTk):

    def __init__(self) -> None:
        super().__init__()

        self.total_columns : int = 4
        self.total_rows : int = 2

        self.title(f'{APP_NAME} for Minecraft Java Edition')
        self.iconbitmap(ICONBITMAP_PATH)
        self.geometry(f"{str(WINDOW_WIDTH)}x{str(WINDOW_HEIGHT)}+{str(WINDOW_X_POSITION)}+{str(WINDOW_Y_POSITION)}")
        self.resizable(WINDOW_X_RESIZABLE, WINDOW_Y_RESIZABLE)

        # Contenedor para las páginas
        self.container : ctk.CTkFrame = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames : dict[str, ctk.CTkFrame] = {}
        for F in (PageHome, PageFabric, PageMods, PageShaders, PageResourcepacks, PageAddServer, PageDHLOD, PageRam, PagePref):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("PageHome")


    def show_frame(self, page_name : str) -> None:
        if page_name in self.frames:
            self.frames[page_name].destroy()

        frame = globals()[page_name](parent=self.container, controller=self)
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

        #frame = self.frames[page_name]
        #frame.tkraise()