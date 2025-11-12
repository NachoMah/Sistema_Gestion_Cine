import json
import os
import platform

def clear():
    # Limpia la consola
    try:
        current_os = platform.system()
        if current_os == "Windows":
            os.system('cls') # Windows
        else:
            os.system('clear') # macOS/Linux
    except Exception as e:
        print(f"Error al limpiar la pantalla: {e}")

#Funcion para registrar administrador
def registrar_admin(usuario, contrasenia, mail, nombre, apellido):
    if usuario in admins:
        print(f"El usuario {usuario} que quiere registrar ya existe. Por favor incie sesión con ese usuario")
        return False
    else:
        admins[usuario] = {
            "Contraseña": contrasenia,
            "Mail": mail,
            "Nombre": nombre,
            "Apellido": apellido,
        }
        guardar_admins()
        
        print(f"¡Bienvenido {usuario}! Usted se ha registrado como administrador correctamente.")
        return True

#Funcion para iniciar sesión de administrador
def login_admin(usuario, contrasenia):
    if usuario not in admins:
        print(f"El usuario {usuario} no existe. Por favor, regístrese primero antes de realziar el log in.")
        return False
    elif admins[usuario]["Contraseña"] != contrasenia:
        print("Contraseña incorrecta")
        return False
    else:
        print(f"¡Bienvenido {usuario}! Se ha inciado sesión correctamente.")
        return True
    
#Funcion para agregar película
def agregar_pelicula(pelicula, genero, duracion, fecha):
    if not pelicula_existente_sistema(pelicula):
        peliculas[pelicula] = {
            "Género": genero, 
            "Duración": duracion,
            "Fecha": fecha,  # DD-MM-YY
        }
        print(f"La pelicula '{pelicula}' se agregó correctamente al sistema")
        return True
    else:
        print(f"La pelicula '{pelicula}' que intenta agregar ya existe en el sistema") 
        return False

#Funcion para eliminar película
def eliminar_pelicula(pelicula):
    try:
        if not pelicula_existente_sistema(pelicula):
            print(f"La película '{pelicula}' no se puede eliminar porque no existe en el sistema.")
            return False
        else:
            del peliculas[pelicula]
            print(f"La película '{pelicula}' fue eliminada correctamente del sistema.")
            return True
    except Exception as e:
        print(f"Ocurrio un error al intentar eliminar la pelicula: {e}")
        return False

#Funcion para modificar película
def modificar_pelicula(pelicula, nuevo_genero, nueva_duracion, nueva_fecha):
    if not pelicula_existente_sistema(pelicula):
        print(f"La película '{pelicula}' no existe en el sistema por lo que no se puede modificar.")
        return False
    else:
        if nuevo_genero:
            peliculas[pelicula]["Género"] = nuevo_genero
            
        if nueva_duracion:
            peliculas[pelicula]["Duración"] = nueva_duracion
        
        if nueva_fecha:
            peliculas[pelicula]["Fecha"] = nueva_fecha  # DD-MM-YY
        
        print(f"¡Los datos de la película '{pelicula}' se puedieron modificar correctamente!.")
        return True

#Funcion para verificar si la pelicula existe en el sistema
def pelicula_existente_sistema(pelicula):
    if pelicula in peliculas:
        return True
    else:
        return False
    
#Funcion para crear butacas
def crear_butacas(filas, asientos):
    butacas = []
    for i in range(filas):
        fila_butacas = []
        for j in range(asientos):
            fila_butacas.append("Libre")
        butacas.append(fila_butacas)
    return butacas

#Funcion para cargar funcion
def cargar_funcion(pelicula, fecha, hora, sala):
    sala = str(sala)

    if not pelicula_existente_sistema(pelicula):
        print(f"La película '{pelicula}' no está registrada. Antes de cargar la función debe registrar la película.")
        return False

    #Se verifica que no haya solapamientos en la misma sala, fecha y hora
    for _, datos in funciones.items():
        misma_sala = str(datos.get("Sala")) == sala
        misma_fecha = datos.get("Fecha") == fecha
        misma_hora = datos.get("Hora") == hora
        if misma_sala and misma_fecha and misma_hora:
            print(f"No se puede cargar la función: ya existe otra función en la sala {sala} el {fecha} a las {hora}.")
            return False

    clave_nueva = f"{pelicula}_{fecha}_{hora}_{sala}"
    if clave_nueva in funciones: 
        print(f"La función de '{pelicula}' ya está programada para esa fecha, hora y sala.")
        return False

    butacas = crear_butacas(6, 6)

    funciones[clave_nueva] = {
        "Película": pelicula,
        "Fecha": fecha,  # DD-MM-YY
        "Hora": hora,    # HH:MM
        "Sala": sala,
        "Butacas": butacas
    }
    print("Función cargada exitosamente.")
    return True


#Funcion para consultar funciones
def consultar_funciones():
    if not funciones:
        print("No se puede, consultar las funciones porque no hay ninguna cargada.")
    else:
        for _, datos in funciones.items():
            print(f"{datos['Película']} - {datos['Fecha']} - {datos['Hora']} - Sala {datos['Sala']}")

def ver_todas_las_peliculas():
    if not peliculas:
        print("No hay películas registradas.")
    else:
        print("\nListado de películas registradas:")
        for nombre, datos in sorted(peliculas.items()):
            genero = datos.get("Género", "N/A")
            duracion = datos.get("Duración", "N/A")
            fecha = datos.get("Fecha", "N/A")
            print(f"- {nombre} | Género: {genero} | Duración: {duracion} | Fecha: {fecha}")


#Funcion para agregar promocion
def agregar_promocion(promocion, tipo, valor, condicion):
    if promocion in promociones:
        print(f"La promoción '{promocion}' ya está cargda.")
        return False
    else:
        promociones[promocion] = {
            "Tipo": tipo,
            "Valor": valor,
            "Condición": condicion,  
        }
        print(f"La promoción {promocion} fue cargada correctamente")
        return True
    
#Funcion para consultar promociones
def consultar_promocion():
    if not promociones: 
        print("No hay promociones registradas. Se deben cargar")
    else:
        for nombre, datos in promociones.items():
            print(f"- {nombre}: Tipo={datos['Tipo']}, Valor={datos['Valor']}, Condición={datos['Condición']}")


#Funcion para ver disponibilidad de butacas
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

#Funcion para generar id de reserva
def generar_id_reserva():
    siguiente = len(reservas) + 1
    if siguiente < 10:
        return f"R000{siguiente}"
    elif siguiente < 100:
        return f"R00{siguiente}"
    elif siguiente < 1000:
        return f"R0{siguiente}"
    else:
        return f"R{siguiente}"

#Funcion para verificar si el asiento existe
def asiento_existe(funcion_id, fila, columna):
    if funcion_id not in funciones:
        return False
    butacas = funciones[funcion_id]["Butacas"]
    total_filas = len(butacas)
    total_cols = len(butacas[0]) if total_filas > 0 else 0
    if fila < 1 or columna < 1:
        return False
    if fila > total_filas:
        return False
    if columna > total_cols:
        return False
    return True


#Funcion para verificar si el asiento esta libre
def asiento_esta_libre(funcion_id, fila, columna):
    """
    True si la butaca está 'Libre'. Índices 1-based.
    """
    butacas = funciones[funcion_id]["Butacas"]
    return butacas[fila - 1][columna - 1] == "Libre"


#Funcion para crear reserva
def crear_reserva(usuario, funcion_id, fila, columna, precio_base):
    """
    Crea una reserva si la función existe y la butaca está libre.
    Marca la butaca como 'Ocupada' y guarda la reserva en 'reservas'.
    Retorna el id de reserva si se crea, o None si falla.
    """
    if funcion_id not in funciones:
        print(f"La función '{funcion_id}' no existe.")
        return None

    if not asiento_existe(funcion_id, fila, columna):
        print("Butaca inexistente para esa función.")
        return None

    if not asiento_esta_libre(funcion_id, fila, columna):
        print("La butaca ya está ocupada.")
        return None

    funciones[funcion_id]["Butacas"][fila - 1][columna - 1] = "Ocupada"

    reserva_id = generar_id_reserva()
    reservas[reserva_id] = {
        "Usuario": usuario,
        "FuncionID": funcion_id,
        "Butaca": {"Fila": fila, "Columna": columna},
        "Precio": precio_base,
        "Estado": "Activa"
    }

    print(f"Reserva creada. ID: {reserva_id} - Usuario: {usuario} - Función: {funcion_id} - Butaca F{fila}A{columna}")
    return reserva_id


#Funcion para consultar reservas por funcion
def consultar_reservas_por_funcion(funcion_id):
    if funcion_id not in funciones:
        print(f"La función '{funcion_id}' no existe.")
        return False

    hay = False
    for rid, r in reservas.items():
        if r["FuncionID"] == funcion_id:
            if not hay:
                print(f"\nReservas de la función {funcion_id}:")
                hay = True
            print(f"- {rid} | Usuario: {r['Usuario']} | Butaca: F{r['Butaca']['Fila']}A{r['Butaca']['Columna']} | "
                  f"Precio: {r['Precio']} | Estado: {r['Estado']}")
    if not hay:
        print("No hay reservas para esta función.")
    return True


#Funcion para consultar reservas por usuario
def consultar_reservas_por_usuario(usuario):
    hay = False
    for rid, r in reservas.items():
        if r["Usuario"] == usuario:
            if not hay:
                print(f"\nReservas del usuario '{usuario}':")
                hay = True
            print(f"- {rid} | Función: {r['FuncionID']} | Butaca: F{r['Butaca']['Fila']}A{r['Butaca']['Columna']} | "
                  f"Precio: {r['Precio']} | Estado: {r['Estado']}")
    if not hay:
        print(f"El usuario '{usuario}' no tiene reservas registradas.")
    return True


#Funcion para calcular ingresos
def calcular_ingresos(filtro=None):
    # se encarga de calcular/consultar el total de ingresos según un filtro (película, sala, día, semana).
    pass


#Funcion para cambiar butaca
def cambiar_butaca(reserva_id, nueva_fila, nueva_columna):
    # 1) Validar reserva
    if reserva_id not in reservas:
        print(f"La reserva '{reserva_id}' no existe.")
        return False

    # 2) Validar estado
    if reservas[reserva_id].get("Estado") != "Activa":
        print(f"La reserva '{reserva_id}' no está activa (estado: {reservas[reserva_id].get('Estado')}).")
        return False

    # 3) Datos actuales
    funcion_id = reservas[reserva_id]["FuncionID"]
    fila_actual = reservas[reserva_id]["Butaca"]["Fila"]
    col_actual  = reservas[reserva_id]["Butaca"]["Columna"]

    # Si pide la misma butaca, no hacemos nada
    misma_fila = (nueva_fila == fila_actual)
    misma_col  = (nueva_columna == col_actual)
    if misma_fila and misma_col:
        print("La nueva butaca es la misma que la actual. No se realizaron cambios.")
        return False

    # 4) Validar función y existencia de la nueva butaca
    if funcion_id not in funciones:
        print(f"La función '{funcion_id}' no existe.")
        return False

    if not asiento_existe(funcion_id, nueva_fila, nueva_columna):
        print("La nueva butaca no existe para esta función.")
        return False

    # 5) Verificar disponibilidad de la nueva butaca
    if not asiento_esta_libre(funcion_id, nueva_fila, nueva_columna):
        print("La nueva butaca está ocupada.")
        return False

    # 6) Efectuar el cambio: liberar vieja y ocupar nueva
    funciones[funcion_id]["Butacas"][fila_actual - 1][col_actual - 1] = "Libre"
    funciones[funcion_id]["Butacas"][nueva_fila - 1][nueva_columna - 1] = "Ocupada"

    # 7) Actualizar la reserva
    reservas[reserva_id]["Butaca"]["Fila"] = nueva_fila
    reservas[reserva_id]["Butaca"]["Columna"] = nueva_columna

    print(f"Butaca cambiada: reserva {reserva_id} -> F{fila_actual}A{col_actual} -> F{nueva_fila}A{nueva_columna}")
    return True


#Funcion para cancelar compra
def cancelar_compra(reserva_id):
    """
    Cancela una compra y libera la butaca correspondiente.
    Cambia el estado de la reserva a 'Cancelada' y marca la butaca como 'Libre'.
    """
    #1 Validar existencia de la reserva
    if reserva_id not in reservas:
        print(f"La reserva '{reserva_id}' no existe.")
        return False

    #2 Validar estado actual
    estado_actual = reservas[reserva_id].get("Estado")
    if estado_actual != "Activa":
        print(f"La reserva '{reserva_id}' no está activa (estado: {estado_actual}).")
        return False

    #3 Obtener datos
    funcion_id = reservas[reserva_id]["FuncionID"]
    fila = reservas[reserva_id]["Butaca"]["Fila"]
    columna = reservas[reserva_id]["Butaca"]["Columna"]

    #4 Intentar liberar butaca en la función (si existe)
    if funcion_id in funciones:
        if asiento_existe(funcion_id, fila, columna):
            funciones[funcion_id]["Butacas"][fila - 1][columna - 1] = "Libre"
        else:
            print("Atención: la butaca de la reserva no existe en la función (no se pudo liberar en la matriz).")
    else:
        print(f"Atención: la función '{funcion_id}' no existe (se cancela igual, sin liberar matriz).")

    #5 Marcar reserva como cancelada
    reservas[reserva_id]["Estado"] = "Cancelada"
    print(f"Reserva '{reserva_id}' cancelada. Butaca F{fila}A{columna} liberada en función {funcion_id}.")
    return True


#Funcion para egenrar un reporte de ocupacion
def generar_reporte_ocupacion():
    try:
        if not funciones:
            print("No hay funciones cargadas en el sistema.")
            return False
        else:
            for func_id, datos in sorted(funciones.items(), key=lambda x: x[1]["Película"]):
                butacas = datos["Butacas"]
                total = len(butacas) * len(butacas[0])

                ocupadas = sum([1 for fila in butacas for asiento in fila if asiento == "Ocupada"])

                porcentaje = (ocupadas / total) * 100 if total > 0 else 0

                print(f"{datos['Película']} - {datos['Fecha']} - {datos['Hora']} - Sala {datos['Sala']}")
                print(f"Butacas ocupadas: {ocupadas}/{total} ({porcentaje:.2f}%)")

            return True
    except KeyError as e:
        print(f"Error: falta la clave {e} en alguna función.")
        return False
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return False


#Funcion para guardar datos
def guardar_datos():
    try:
        with open("admins.txt", "w", encoding="utf-8") as f:
            json.dump(admins, f, indent=4, ensure_ascii=False)

        with open("peliculas.txt", "w", encoding="utf-8") as f:
            json.dump(peliculas, f, indent=4, ensure_ascii=False)

        with open("funciones.txt", "w", encoding="utf-8") as f:
            json.dump(funciones, f, indent=4, ensure_ascii=False)

        with open("reservas.txt", "w", encoding="utf-8") as f:
            json.dump(reservas, f, indent=4, ensure_ascii=False)

        print("Datos guardados.")
        return True
    except Exception as e:
        print(f"Error al guardar los datos: {e}")
        return False

#Funcion para cargar datos
def cargar_datos():
    global admins, peliculas, funciones, reservas
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

    try:
        with open("reservas.txt", "r", encoding="utf-8") as f:
            reservas = json.load(f)
    except FileNotFoundError:
        reservas = {}

    print("Datos cargados.")
    return True


def guardar_admins():
    try:
        with open("admins.txt", "w", encoding="utf-8") as f:
            json.dump(admins, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar administradores: {e}")
        return False


#Menu gestion peliculas
def menu_gestion_peliculas():
    while True:
        clear()
        print("\n--- GESTIÓN DE PELÍCULAS ---")
        print("1. Agregar película")
        print("2. Modificar película")
        print("3. Eliminar película")
        print("4. Ver todas las películas")
        print("0. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            pelicula = input("Título de la película: ")
            genero = input("Género: ")
            duracion = input("Duración (minutos): ")
            fecha = input("Fecha de estreno (DD-MM-YY): ")
            agregar_pelicula(pelicula, genero, duracion, fecha)
        
        elif opcion == "2":
            pelicula = input("Película a modificar: ")
            nuevo_genero = input("Nuevo género (Enter para no cambiar): ")
            nueva_duracion = input("Nueva duración (Enter para no cambiar): ")
            nueva_fecha = input("Nueva fecha (DD-MM-YY, Enter para no cambiar): ")
            modificar_pelicula(pelicula, nuevo_genero, nueva_duracion, nueva_fecha)
        
        elif opcion == "3":
            pelicula = input("Película a eliminar: ")
            eliminar_pelicula(pelicula)
        elif opcion == "4":
            ver_todas_las_peliculas()
        
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


#Menu gestion funciones
def menu_gestion_funciones():
    while True:
        clear()
        print("\n--- GESTIÓN DE FUNCIONES ---")
        print("1. Cargar función de película")
        print("2. Consultar funciones programadas")
        print("3. Ver disponibilidad de butacas")
        print("4. Ver horarios por película")
        print("0. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            pelicula = input("Película: ")
            fecha = input("Fecha (DD-MM-YY): ")
            hora = input("Hora (HH:MM): ")
            sala = input("Sala: ")
            cargar_funcion(pelicula, fecha, hora, sala)
        
        elif opcion == "2":
            consultar_funciones()
        
        elif opcion == "3":
            pelicula = input("Pelicula: ")
            fecha = input("Fecha (DD-MM-YY): ")
            hora = input("Hora (HH:MM): ")
            sala = input("Sala: ")
            funcion_id = f"{pelicula}_{fecha}_{hora}_{sala}"
            ver_disponibilidad_funcion(funcion_id)
        
        elif opcion == "4":
            from usuario import ver_horarios_pelicula
            pelicula = input("Ingrese el título de la película: ")
            fecha = input("Ingrese la fecha (DD-MM-YY) o presione \"Enter\" para ver todos los horarios: ")
            fecha = fecha if fecha.strip() else None
            ver_horarios_pelicula(pelicula, fecha, funciones)
        
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


#Menu gestion reservas
def menu_gestion_reservas():
    while True:
        clear()
        print("\n--- GESTIÓN DE RESERVAS ---")
        print("1. Crear reserva")
        print("2. Consultar reservas por función")
        print("3. Consultar reservas por usuario")
        print("4. Cancelar compra")
        print("5. Cambiar butaca")
        print("0. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            usuario = input("Usuario (nombre o mail): ")
            print("Formato de ID: pelicula_fecha_hora_sala (ej.: Avatar_10-10-25_20:00_1)")
            funcion_id = input("ID de la función: ")
            fila = int(input("Fila (número empezando en 1): "))
            columna = int(input("Asiento (número empezando en 1): "))
            precio = float(input("Precio base: "))
            crear_reserva(usuario, funcion_id, fila, columna, precio)
        
        elif opcion == "2":
            print("Formato de ID: pelicula_fecha_hora_sala (ej.: Avatar_10-10-25_20:00_1)")
            funcion_id = input("ID de la función: ")
            consultar_reservas_por_funcion(funcion_id)
        
        elif opcion == "3":
            usuario = input("Usuario (nombre o mail): ")
            consultar_reservas_por_usuario(usuario)
        
        elif opcion == "4":
            reserva_id = input("ID de la reserva (ej.: R0001): ")
            cancelar_compra(reserva_id)
        
        elif opcion == "5":
            reserva_id = input("ID de la reserva (ej.: R0001): ")
            nueva_fila = int(input("Nueva fila (número empezando en 1): "))
            nueva_col = int(input("Nuevo asiento (número empezando en 1): "))
            cambiar_butaca(reserva_id, nueva_fila, nueva_col)
        
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


#Menu gestion promociones
def menu_promociones():
    while True:
        clear()
        print("\n--- GESTIÓN DE PROMOCIONES ---")
        print("1. Agregar promoción")
        print("2. Consultar promociones")
        print("0. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre_promocion = input("Ingrese el nombre de la promoción: ")
            tipo = input("Tipo de promoción (Ejemplo: descuento, 2x1, etc. ): ")
            valor = int(input("Valor de la promocion (ej: 50 o 0.5 para 50%, 2 entradas para 2x1): "))
            condicion = input("Condición para que se cumpla (Ejemplo: 'miercoles', 'fecha festiva'): ")
            agregar_promocion(nombre_promocion, tipo, valor, condicion)
        
        elif opcion == "2":
            consultar_promocion()
        
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


#Menu principal del administrador
def mainAdmin():
    cargar_datos()
    while True:
        clear()
        print("\n" + "="*50)
        print("    MENÚ ADMINISTRADOR")
        print("="*50)
        print("1. Gestión de Películas")
        print("2. Gestión de Funciones")
        print("3. Gestión de Reservas")
        print("4. Gestión de Promociones")
        print("5. Generar reporte de ocupación")
        print("6. Guardar datos")
        print("0. Cerrar sesión")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            menu_gestion_peliculas()
        elif opcion == "2":
            menu_gestion_funciones()
        elif opcion == "3":
            menu_gestion_reservas()
        elif opcion == "4":
            menu_promociones()
        elif opcion == "5":
            generar_reporte_ocupacion()
        elif opcion == "6":
            guardar_datos()
        elif opcion == "0":
            print("Sesión cerrada.")
            return  # Volver al menú principal
        else:
            print("Opción no válida.")


#Funcion de login administrador y menu
def login_admin_menu():
    cargar_datos()
    
    while True:
        clear()
        print("\n" + "="*50)
        print("    ACCESO ADMINISTRADOR")
        print("="*50)
        print("1. Registrar administrador")
        print("2. Iniciar sesión")
        print("0. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            bandera = True
            while bandera:
                clave_registro = input("Clave de registro (o -1 para volver): ")
                if clave_registro == "-1":
                    bandera = False
                elif clave_registro != "Uade123":
                    print("Clave incorrecta.")
                else:
                    usuario = input("Usuario: ")
                    contrasenia = input("Contraseña: ")
                    mail = input("Mail: ")
                    nombre = input("Nombre: ")
                    apellido = input("Apellido: ")
                    registrar_admin(usuario, contrasenia, mail, nombre, apellido)
                    bandera = False
        
        elif opcion == "2":
            bandera = True
            while bandera:
                usuario = input("Usuario (o -1 para volver): ")
                if usuario == "-1":
                    bandera = False
                    continue
                contrasenia = input("Contraseña: ")
                if login_admin(usuario, contrasenia):
                    mainAdmin()
                    return
                else:
                    print("Credenciales incorrectas. Intente nuevamente o ingrese -1 para volver.")
        
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


#Variables globales del sistema
admins = {}
peliculas = {}
funciones = {}
promociones = {}
reservas = {}