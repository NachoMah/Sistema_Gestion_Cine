import os
import platform

def clear():
    """
    Funcion para limpiar la consola según el sistema operativo detectado
    """
    try:
        current_os = platform.system()
        if current_os == "Windows":
            os.system('cls') # Windows
        else:
            os.system('clear') # macOS/Linux
    except Exception as e:
        print(f"Error al limpiar la pantalla: {e}")