import json

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
    
def crear_butacas(filas, asientos):
    """
    Funcion encaragda de crear las butacas
    """
    butacas = []
    for fila in range(filas):
        fila_butacas = []
        for asiento in range(asientos):
            fila_butacas.append("Libre")
        butacas.append(fila_butacas)
    return butacas

def cargar_funcion(pelicula, fecha, hora, sala):
    """
    Funcion que se encarga de crear una nueva función para una película ya existente.
    """ 
    if not pelicula_existente_sistema(pelicula):
        print(f"La pelicula '{pelicula} no esta registrada. Antes de cargar la funcion debe registrar la pelicula.")
        return False
    else:
        datos_funcion = f"{pelicula}_{fecha}_{hora}_{sala}"
        
        if datos_funcion in funciones:
            print(f"La función de la película '{pelicula}' ya está programada para tal fecha y hora")
            return False
        
        else:
           
            butacas = crear_butacas(6,6)
            
            funciones[datos_funcion] = {
                "Película": pelicula,
                "Fecha": fecha,
                "Hora": hora,
                "Sala": sala,
                "Butacas": butacas
                }
            
            return True

def consultar_funciones():
    if not funciones:
        print("No se puede, consultar las funciones porque no hay ninguna cargada.")
    else:
        for datos_funcion, datos in funciones.items():
            print(f"{datos['Película']} - {datos['Fecha']} - {datos['Hora']} - Sala {datos['Sala']}")

def agregar_promocion(promocion):
    # se encarga de registrar una promoción o descuento.
    pass

def ver_disponibilidad_funcion(funcion_id):
    """
    Muestra la disponibilidad de butacas de una función.
    Imprime 'L' para Libre y 'O' para Ocupada.
    """
    if funcion_id not in funciones:
        print(f"La función '{funcion_id}' no existe en el sistema.")
        return False
    
    butacas = funciones[funcion_id]["Butacas"]
    print(f"\nDisponibilidad de la función: {funciones[funcion_id]['Película']} "
          f"- {funciones[funcion_id]['Fecha']} "
          f"- {funciones[funcion_id]['Hora']} "
          f"- Sala {funciones[funcion_id]['Sala']}")
    print("   " + "  ".join([f"A{col+1}" for col in range(len(butacas[0]))]))

    for i, fila in enumerate(butacas):
        fila_impresa = []
        for asiento in fila:
            if asiento == "Libre":
                fila_impresa.append("L")
            else:
                fila_impresa.append("O")
        print(f"F{i+1} " + "  ".join(fila_impresa))
    return True

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
    """
    Guarda los diccionarios del sistema (admins, peliculas, funciones)
    en archivos .txt usando formato JSON.
    """
    try:
        with open("admins.txt", "w", encoding="utf-8") as f:
            json.dump(admins, f, indent=4, ensure_ascii=False)

        with open("peliculas.txt", "w", encoding="utf-8") as f:
            json.dump(peliculas, f, indent=4, ensure_ascii=False)

        with open("funciones.txt", "w", encoding="utf-8") as f:
            json.dump(funciones, f, indent=4, ensure_ascii=False)

        print("Datos guardados.")
        return True
    except Exception as e:
        print(f"Error al guardar los datos: {e}")
        return False


def cargar_datos():
    """
    Carga los diccionarios del sistema desde archivos .txt.
    Si no existen los archivos, inicializa los diccionarios vacíos.
    """
    global admins, peliculas, funciones
    try:
        with open("admins.txt", "r", encoding="utf-8") as f:
            admins = json.load(f)
    except FileNotFoundError:
        admins = {}

    try:
        with open("peliculas.txt", "r", encoding="utf-8") as f:
            peliculas = json.load(f)
    except FileNotFoundError:
        peliculas = {}

    try:
        with open("funciones.txt", "r", encoding="utf-8") as f:
            funciones = json.load(f)
    except FileNotFoundError:
        funciones = {}

    print("Datos cargados.")
    return True

def main():
    cargar_datos()
    while True:
        print("\n--- Menú Administrativo ---")
        print("1. Registrar administrador")
        print("2. Iniciar sesión administrador")
        print("3. Agregar película")
        print("4. Modificar película")
        print("5. Eliminar película")
        print("6. Cargar función de película")
        print("7. Consultar funciones programadas")
        print("8. Ver disponibilidad de butacas")
        print("9. Guardar datos")
        print("0. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            usuario = input("Usuario: ")
            contrasenia = input("Contraseña: ")
            mail = input("Mail: ")
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            edad = input("Edad: ")
            registrar_admin(usuario, contrasenia, mail, nombre, apellido, edad)

        elif opcion == "2":
            usuario = input("Usuario: ")
            contrasenia = input("Contraseña: ")
            login_admin(usuario, contrasenia)

        elif opcion == "3":
            pelicula = input("Título de la película: ")
            genero = input("Género: ")
            duracion = input("Duración (minutos): ")
            fecha = input("Fecha de estreno (DD-MM-YYYY): ")
            agregar_pelicula(pelicula, genero, duracion, fecha)

        elif opcion == "4":
            pelicula = input("Película a modificar: ")
            nuevo_genero = input("Nuevo género (Enter para no cambiar): ")
            nueva_duracion = input("Nueva duración (Enter para no cambiar): ")
            nueva_fecha = input("Nueva fecha (Enter para no cambiar): ")
            modificar_pelicula(pelicula, nuevo_genero, nueva_duracion, nueva_fecha)

        elif opcion == "5":
            pelicula = input("Película a eliminar: ")
            eliminar_pelicula(pelicula)

        elif opcion == "6":
            pelicula = input("Película: ")
            fecha = input("Fecha (DD-MM-YYYY): ")
            hora = input("Hora (HH:MM): ")
            sala = input("Sala: ")
            cargar_funcion(pelicula, fecha, hora, sala)

        elif opcion == "7":
            consultar_funciones()

        elif opcion == "8":
            funcion_id = input("Ingrese el ID de la función (pelicula_fecha_hora_sala): ")
            ver_disponibilidad_funcion(funcion_id)

        elif opcion == "9":
            guardar_datos()

        elif opcion == "0":
            print("Saliendo del sistema.")
            break

        else:
            print("Error, intente nuevamente.")

#Programa principal 
admins = {}
peliculas = {}
funciones = {}
main()