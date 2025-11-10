"""
Sistema de Gestión de Cine
Punto de entrada principal del sistema
"""

from admin import login_admin_menu
from usuario import login_usuario_menu

def main():
    """
    Función principal que determina el tipo de usuario y redirige al menú correspondiente.
    """
    while True:
        print("\n" + "="*50)
        print("    SISTEMA DE GESTIÓN DE CINE")
        print("="*50)
        print("1. Acceder como Usuario")
        print("2. Acceder como Administrador")
        print("0. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            terminar = login_usuario_menu()
            if terminar:  # Si se borró la cuenta, terminar ejecución
                break
        elif opcion == "2":
            login_admin_menu()
        elif opcion == "0":
            print("\n¡Hasta luego!")
            break
        else:
            print("\nOpción no válida. Por favor, seleccione una opción correcta.")



main()

