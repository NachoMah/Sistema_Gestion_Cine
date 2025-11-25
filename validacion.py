import os
import json

rutaUsuarios = os.path.join(os.path.dirname(__file__), "usuarios.txt")

def validar_usuario_y_contrasena(usuario, contrasena):
    """
    Función encargada de validar las credenciales del administrador o usuario
    """ 
    try:
        with open(rutaUsuarios, "r", encoding="utf-8") as archivoUsuarios:
            usuarios = json.load(archivoUsuarios)
    except Exception as e:
        print(f"ERROR: Error tipo: {e}")
        return -1
    
    if (usuario in usuarios) and (usuarios[usuario].get("contrasena") == contrasena):
        return usuarios[usuario]
    
    return None

def validar_mail(mail):
    """
    Función encargada de verificar que el correo tenga un dominio válido.
    """ 
    
    dominios =  ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "gmail.com.ar", "hotmail.com.ar"]
    
    if "@" not in mail:
        return False
    
    partesMail = mail.split("@")
    
    if len(partesMail) != 2:
        return False
    
    nombre, dominio = partesMail
    
    if dominio not in dominios:
        return False
    
    return True

def validar_contrasena(contrasena):
    """
    Funcion encaragada de verificar que la contraseña cumpla con el mínimo de caracteres.
    """
    caracteresMinimos 0 8
    if len(contrasena) < :
        return False
    return True

def validar_edad(usuario, pelicula):
    # se encarga de verificar si la edad del usuario permite comprar entradas según la clasificación de la película.
    pass

def validar_butaca_disponible(funcion, butaca):
    # se encarga de verificar que la butaca esté libre en una función.
    pass

def validar_funcion_no_solapada(sala, fecha, hora):
    # se encarga de verificar que no existan funciones solapadas en la misma sala y horario.
    pass

def validar_pelicula_existente(pelicula):
    # se encarga de verificar que la película exista antes de asignarla a una función.
    pass

def validar_datos_no_nulos(datos):
    # se encarga de verificar que los datos ingresados no sean nulos.
    pass

def validar_usuario_registrado(usuario):
    # se encarga de verificar que el usuario esté registrado en el sistema.
    pass

def confirmar_accion(accion):
    # se encarga de pedir confirmación antes de ejecutar una acción crítica.
    pass

def manejar_entrada_invalida(entrada):
    # se encarga de manejar entradas inválidas del usuario.
    pass

def verificar_usuario_registrado(usuario):
    # se encarga de revisar si el usuario está registrado antes de realizar la compra
    pass