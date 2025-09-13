admins = {}
peliculas = {}

def registrar_admin(usuario, contrasenia, mail, nombre, apellido, edad):
    """
    Funcion encargada de registrar a un usuario como adminsitrador
    """
    if usuario in admins:
        print(f"El usuario {usuario} que quiere registrar ya existe. Por favor incie sesión con ese usuario")
        return False
    else:
        admins[usuario] = {
            "Contraseña": contrasenia,
            "Mail": mail,
            "Nombre": nombre,
            "Apellido": apellido,
            "Edad": edad, 
        }
        
        print(f"¡Bienvenido {usuario}! Usted se ha registrado como administrador correctamente.")
        return True

def login_admin(usuario, contrasenia):
    """
    Función encargada de validar el inicio de sesión del administrador.
    """
    if usuario not in admins:
        print(f"El usuario {usuario} no existe. Por favor, regístrese primero antes de realziar el log in.")
        return False
    elif admins[usuario]["Contraseña"] != contrasenia:
        print("Contraseña incorrecta")
        return False
    else:
        print(f"¡Bienvenido {usuario}! Se ha inciado sesión correctamente.")
        return True
    
def agregar_pelicula(pelicula, genero, duracion, fecha):
    if not pelicula_existente_sistema(pelicula):
        peliculas[pelicula] = {
            "Género": genero, 
            "Duración": duracion,
            "Fecha": fecha,
        }
        print(f"La pelicula '{pelicula}' se agregó correctamente al sistema")
        return True
    else:
        print(f"La pelicula '{pelicula}' que intenta agregar ya existe en el sistema") 
        return False

def eliminar_pelicula(pelicula):
    """
    Funcion que se encarga de dar de baja una película y sus funciones asociadas.
    """
    if not pelicula_existente_sistema(pelicula):
        print(f"La película '{pelicula}' no se puede eliminar porque no existe en el sistema.")
        return False
    else:
        del peliculas[pelicula]
        print(f"La película '{pelicula}' fue eliminada correctamente del sistema.")
        return True

def modificar_pelicula(pelicula, nuevo_genero, nueva_duracion, nueva_fecha):
    """
    Función que permite editar información de películas existentes (duracion, genero, fecha).
    """
    if not pelicula_existente_sistema(pelicula):
        print(f"La película '{pelicula}' no existe en el sistema por lo que no se puede modificar.")
        return False
    else:
        if nuevo_genero:
            peliculas[pelicula]["Género"] = nuevo_genero
            
        if nueva_duracion:
            peliculas[pelicula]["Duración"] = nueva_duracion
        
        if nueva_fecha:
            peliculas[pelicula]["Fecha"] = nueva_fecha
        
        print(f"¡Los datos de la película '{pelicula}' se puedieron modificar correctamente!.")
        return True


def pelicula_existente_sistema(pelicula):
    """
    Función auxiliar para verificar si la película ya existe en el sistema (ayuda a las funciones que gestionan las peliculas).
    """
    if pelicula in peliculas:
        return True
    else:
        return False

def agregar_promocion(promocion):
    # se encarga de registrar una promoción o descuento.
    pass

def cargar_funcion(pelicula, fecha, hora, sala):
    # se encarga de crear una nueva función para una película ya existente.
    pass

def ver_disponibilidad_funcion(funcion):
    # se encarga de mostrar la disponibilidad de butacas.
    pass

def consultar_funciones():
    # devuelve el listado de las funciones programadas.
    pass

def consultar_reservas_por_funcion(funcion):
    # devuelve todas las reservas asociadas a una función.
    pass

def consultar_reservas_por_usuario(usuario):
    # se encarga de devolver todas las reservas realizadas por un usuario.
    pass

def calcular_ingresos(filtro=None):
    # se encarga de calcular/consultar el total de ingresos según un filtro (película, sala, día, semana).
    pass

def cambiar_butaca(reserva, nueva_butaca):
    # se encarga de cambiar la butaca de una reserva si está disponible.
    pass

def cancelar_compra(reserva):
    # se encarga de cancelar una compra y liberar la butaca correspondiente.
    pass

def generar_reporte_ocupacion():
    # se encarga de generar un reporte simple de ocupación de salas.
    pass

def guardar_datos():
    # se encarga de guardar toda la información del sistema en archivos .txt.
    pass

def cargar_datos():
    # se encarga de cargar la información desde archivos .txt al sistema.
    pass     

def main():
    #Menú para el registro/logueo del administrador y otras funcionalidades que va a poder realizar
    pass