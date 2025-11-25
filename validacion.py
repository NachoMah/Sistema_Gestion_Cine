import os
import json

rutaUsuarios = os.path.join(os.path.dirname(__file__), "usuarios.txt")
rutaPeliculas = os.path.join(os.path.dirname(__file__), "peliculas.txt")

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
    caracteresMinimos = 8
    if len(contrasena) < caracteresMinimos:
        return False
    return True

def validar_edad(usuario, pelicula):
    """
    Función encargada de verificar si la edad del usuario permite comprar entradas según la clasificación de la película.
    """
    
    clasificacion = pelicula.get("clasificacion", "").upper()
    edadUsuario = usuario.get("edad", 0)

    edadesSegunClasificacion = {
        "ATP": 0,
        "+13": 13,
        "+16": 16,
        "+18": 18
    }

    if clasificacion not in edadesSegunClasificacion:
        return False

    edadMinima = edadesSegunClasificacion[clasificacion]

    if edadUsuario >= edadMinima:
        return True
    else:
        return False

def validar_butaca_disponible(funcion, butaca):
    """
    Función encargada de verificar que la butaca esté libre en una función.
    """

    pass

def validar_funcion_no_solapada(sala, fecha, hora):
    """
    Función encargada de verificar que no existan funciones solapadas en la misma sala y horario.
    """
    pass

def validar_pelicula_existente(pelicula):
    """
    Función encargada de verificar que la película exista antes de asignarla a una función.
    """
    try:
        with open("peliculas.txt", "r", encoding="utf-8") as archivoPelicula:
            peliculas = json.load(archivoPelicula)
            
            for titulo in peliculas.keys():
                if pelicula.strip().lower() == titulo.lower():
                    return True
            return False
    
    except FileNotFoundError:
        print("ERROR: El archivo no se pudo encontrar. Intentelo más tarde")
        
    
    except Exception as e:
        print(f"Error al validar película: {e}")
        return -1
        
def validar_datos_no_nulos(datos):
    """
    Función encargada de verificar que los datos ingresados no sean nulos
    """
    pass

def validar_usuario_registrado(usuario):
    """
    Función encargada de verificar que el usuario esté registrado en el sistema.
    """
    pass

def confirmar_accion(accion):
    """
    Función encargada de pedir confirmación antes de ejecutar una acción crítica.
    """
    pass

def manejar_entrada_invalida(entrada):
    """ 
    Función encargada de manejar entradas inválidas del usuario.
    """
    pass

def verificar_usuario_registrado(usuario):
    """
    Función encargada de revisar si el usuario está registrado antes de realizar la compra
    """
    pass