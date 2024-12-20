import tkinter


def get_screen_dimentions() -> dict[str, int]:
    '''Función para calcular la resolución de pantalla del usuario. Devuelve un diccionario'''
    root : tkinter.Tk = tkinter.Tk()
    screen_width : int = root.winfo_screenwidth() # Ancho en px
    screen_height : int = root.winfo_screenheight() # Alto en px

    screen_dimentions : dict = {"width" : screen_width, "height" : screen_height}

    root.destroy()

    return screen_dimentions


def calculate_position(screen_dimention : int = 0, window_dimention : int = 600) -> int:
    '''Función para calcular la posición en determinado eje de la ventana. Permite centrarla'''
    if window_dimention == 0:
        raise ValueError("No se ha indicado las dimensiones de la pantalla. No es posible calcular la posición.")
    axis : int = int((screen_dimention / 2) - (window_dimention / 2))
    return axis