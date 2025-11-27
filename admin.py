import json
import os
from clear import clear
import validacion

def pausar():
    """
    Función para pausar la ejecución hasta que el usuario presione Enter.
    """
    input("\nPresione Enter para continuar...")

# Funciones helper para validaciones de formato (específicas del contexto)
def validar_formato_fecha(fecha):
    """
    Valida que la fecha tenga formato DD-MM-YY.
    Retorna True si es válido, False en caso contrario.
    Solo acepta números en los campos de día, mes y año.
    """
    if not fecha or not fecha.strip():
        return False
    
    try:
        partes = fecha.strip().split('-')
        if len(partes) != 3:
            return False
        
        # Verificar que cada parte contenga solo dígitos
        if not (partes[0].isdigit() and partes[1].isdigit() and partes[2].isdigit()):
            return False
        
        dia, mes, anio = int(partes[0]), int(partes[1]), int(partes[2])
        
        # Validar que el día tenga 2 dígitos, mes tenga 2 dígitos y año tenga 2 dígitos
        if not (len(partes[0]) == 2 and len(partes[1]) == 2 and len(partes[2]) == 2):
            return False
        
        # Validar rangos básicos
        if not (1 <= dia <= 31 and 1 <= mes <= 12):
            return False
        
        return True
    except (ValueError, IndexError):
        return False

def validar_formato_hora(hora):
    """
    Valida que la hora tenga formato HH:MM.
    Retorna True si es válido, False en caso contrario.
    """
    try:
        partes = hora.strip().split(':')
        if len(partes) != 2:
            return False
        horas, minutos = int(partes[0]), int(partes[1])
        # Validar rangos
        if not (0 <= horas <= 23 and 0 <= minutos <= 59):
            return False
        return True
    except (ValueError, IndexError):
        return False

def validar_numero_positivo(valor, mensaje_error="Debe ser un número positivo."):
    """
    Valida que el valor sea un número positivo.
    Retorna el número si es válido, None en caso contrario.
    """
    try:
        numero = int(valor.strip())
        if numero <= 0:
            print(f"ERROR: {mensaje_error}")
            return None
        return numero
    except ValueError:
        print("ERROR: Debe ingresar un número válido.")
        return None

def validar_sala(sala_str):
    """
    Valida que la sala sea un número entre 1 y 6.
    Retorna el número si es válido, None en caso contrario.
    """
    try:
        sala = int(sala_str.strip())
        if not (1 <= sala <= 6):
            print("ERROR: La sala debe ser un número entre 1 y 6.")
            return None
        return sala
    except ValueError:
        print("ERROR: Debe ingresar un número válido.")
        return None

from precios import (
    cargar_precios,
    calcular_precio_entrada,
    obtener_precio_base,
    menu_gestion_precios,
    seleccionar_tipo_entrada,
    seleccionar_descuento
)

#Funcion para registrar administrador
def registrar_admin(usuario, contrasenia, mail, nombre, apellido):
    """
    Función para registrar un nuevo administrador en el sistema.
    """
    from validacion import validar_mail, validar_contrasena, validar_datos_no_nulos
    
    # Validar datos no nulos
    datos = [usuario, contrasenia, mail, nombre, apellido]
    if not validar_datos_no_nulos(datos):
        print("ERROR: Todos los campos son obligatorios y no pueden estar vacíos.")
        return False
    
    # Validar formato de mail
    if not validar_mail(mail):
        print("ERROR: El mail debe tener un dominio válido (gmail, hotmail, outlook, yahoo, cineuade.com, etc.).")
        return False
    
    # Validar contraseña
    if not validar_contrasena(contrasenia):
        print("ERROR: La contraseña debe tener al menos 5 caracteres.")
        return False
    
    # Normalizar usuario a minúsculas para evitar errores de tipeo
    usuario = usuario.strip().lower()
    mail = mail.strip().lower()
    
    # Validar que el usuario no exista (búsqueda case-insensitive)
    usuario_existe = False
    for usuario_key in admins.keys():
        if usuario_key.lower() == usuario:
            usuario_existe = True
            break
    
    if usuario_existe:
        print(f"El usuario {usuario} que quiere registrar ya existe. Por favor incie sesión con ese usuario")
        return False
    
    # Registrar admin
    admins[usuario] = {
        "Contraseña": contrasenia,
        "Mail": mail,
        "Nombre": nombre,
        "Apellido": apellido,
    }
    guardar_admins()
    
    print(f"¡Bienvenido {usuario}! Usted se ha registrado como administrador correctamente.")
    print("Administrador registrado de manera exitosa.")
    return True

#Funcion para iniciar sesión de administrador
def login_admin(usuario, contrasenia):
    """
    Función para iniciar sesión de administrador
    """
    from validacion import validar_admin_y_contrasena
    
    resultado = validar_admin_y_contrasena(usuario, contrasenia)
    if resultado is None:
        print("Usuario o contraseña incorrectos.")
        return False
    else:
        print(f"¡Bienvenido {usuario}! Se ha iniciado sesión correctamente.")
        return True
    
#Funcion para agregar película
def agregar_pelicula(pelicula, genero, duracion, fecha):
    """
    Función para agregar una película al sistema
    """
    from validacion import validar_pelicula_existente
    
    # Limpiar espacios pero mantener el formato original (case-sensitive)
    pelicula_limpia = pelicula.strip()
    
    # Verificar si existe (búsqueda case-insensitive, pero guardar con formato original)
    pelicula_normalizada = pelicula_limpia.lower()
    pelicula_existe = False
    pelicula_clave_original = None
    for pelicula_key in peliculas.keys():
        if pelicula_key.lower() == pelicula_normalizada:
            pelicula_existe = True
            pelicula_clave_original = pelicula_key
            break
    
    if pelicula_existe:
        print(f"La pelicula '{pelicula_clave_original}' que intenta agregar ya existe en el sistema")
        return False
    
    # Guardar con el formato original (case-sensitive)
    peliculas[pelicula_limpia] = {
        "Género": genero, 
        "Duración": duracion,
        "Fecha": fecha,  # DD-MM-YY
    }
    print(f"La pelicula '{pelicula_limpia}' se agregó correctamente al sistema")
    return True

#Funcion para eliminar película
def eliminar_pelicula(pelicula):
    """
    Función para eliminar una película del sistema si existe.
    También elimina todas las funciones asociadas a esa película.
    """
    from validacion import validar_pelicula_existente, confirmar_accion
    
    # Normalizar película a minúsculas para búsqueda
    pelicula_normalizada = pelicula.strip().lower()
    
    # Buscar película (case-insensitive)
    pelicula_clave_original = None
    for pelicula_key in peliculas.keys():
        if pelicula_key.lower() == pelicula_normalizada:
            pelicula_clave_original = pelicula_key
            break
    
    try:
        if pelicula_clave_original is None:
            print(f"La película '{pelicula}' no se puede eliminar porque no existe en el sistema.")
            return False
        
        # Contar funciones asociadas
        funciones_asociadas = []
        for funcion_id, datos_funcion in funciones.items():
            if str(datos_funcion.get("Película", "")).strip().lower() == pelicula_normalizada:
                funciones_asociadas.append(funcion_id)
        
        # Confirmar eliminación
        mensaje_confirmacion = f"eliminar la película '{pelicula_clave_original}'"
        if funciones_asociadas:
            mensaje_confirmacion += f" y sus {len(funciones_asociadas)} función(es) asociada(s)"
        
        if not confirmar_accion(mensaje_confirmacion):
            print("Eliminación de película cancelada.")
            return False
        
        # Eliminar todas las funciones asociadas
        funciones_eliminadas = 0
        for funcion_id in funciones_asociadas:
            del funciones[funcion_id]
            funciones_eliminadas += 1
        
        # Eliminar la película
        del peliculas[pelicula_clave_original]
        
        # Guardar cambios
        guardar_datos()
        
        mensaje = f"La película '{pelicula_clave_original}' fue eliminada correctamente del sistema."
        if funciones_eliminadas > 0:
            mensaje += f" Se eliminaron {funciones_eliminadas} función(es) asociada(s)."
        print(mensaje)
        return True
    except Exception as e:
        print(f"Ocurrio un error al intentar eliminar la pelicula: {e}")
        return False

#Funcion para modificar película
def modificar_pelicula(pelicula, nuevo_genero, nueva_duracion, nueva_fecha):
    """
    Función para modificar los datos de una película.
    """
    from validacion import confirmar_accion
    
    # Normalizar película a minúsculas para búsqueda
    pelicula_normalizada = pelicula.strip().lower()
    
    # Buscar película (case-insensitive)
    pelicula_clave_original = None
    for pelicula_key in peliculas.keys():
        if pelicula_key.lower() == pelicula_normalizada:
            pelicula_clave_original = pelicula_key
            break
    
    if pelicula_clave_original is None:
        print(f"La película '{pelicula}' no existe en el sistema por lo que no se puede modificar.")
        return False
    else:
        # Construir mensaje de cambios
        cambios = []
        if nuevo_genero:
            cambios.append(f"género: {nuevo_genero}")
        if nueva_duracion:
            cambios.append(f"duración: {nueva_duracion}")
        if nueva_fecha:
            cambios.append(f"fecha: {nueva_fecha}")
        
        if cambios:
            cambios_texto = ", ".join(cambios)
            if not confirmar_accion(f"modificar la película '{pelicula_clave_original}' ({cambios_texto})"):
                print("Modificación de película cancelada.")
                return False
        
        if nuevo_genero:
            peliculas[pelicula_clave_original]["Género"] = nuevo_genero
            
        if nueva_duracion:
            peliculas[pelicula_clave_original]["Duración"] = nueva_duracion
        
        if nueva_fecha:
            peliculas[pelicula_clave_original]["Fecha"] = nueva_fecha  # DD-MM-YY
        
        print(f"¡Los datos de la película '{pelicula_clave_original}' se puedieron modificar correctamente!.")
        return True

#Funcion para crear butacas
def crear_butacas(filas, asientos):
    """
    Función para generar la matriz de butacas en estado 'Libre'.
    """
    butacas = []
    for i in range(filas):
        fila_butacas = []
        for j in range(asientos):
            fila_butacas.append("Libre")
        butacas.append(fila_butacas)
    return butacas

#Funcion para cargar funcion
def cargar_funcion(pelicula, fecha, hora, sala):
    """
    Función para cargar una nueva función de película
    """
    from validacion import validar_pelicula_existente
    sala = str(sala)

    # Normalizar película a minúsculas para búsqueda
    pelicula_normalizada = pelicula.strip().lower()
    
    # Buscar película (case-insensitive)
    pelicula_clave_original = None
    for pelicula_key in peliculas.keys():
        if pelicula_key.lower() == pelicula_normalizada:
            pelicula_clave_original = pelicula_key
            break
    
    if pelicula_clave_original is None:
        print(f"La película '{pelicula}' no está registrada. Antes de cargar la función debe registrar la película.")
        return False

    # Obtener duración de la película para validar solapamiento
    duracion_pelicula = peliculas.get(pelicula_clave_original, {}).get("Duración", "0")
    if isinstance(duracion_pelicula, str):
        try:
            duracion_pelicula = int(duracion_pelicula)
        except:
            duracion_pelicula = 0
    
    # Validar que no haya solapamientos usando función modular
    # Pasar también el diccionario de películas para evitar leer el archivo múltiples veces
    from validacion import validar_funcion_no_solapada
    resultado_validacion, pelicula_solapada = validar_funcion_no_solapada(sala, fecha, hora, duracion_pelicula, funciones, peliculas)
    if not resultado_validacion:
        if pelicula_solapada:
            print(f"No se puede cargar la función: ya existe otra función solapada en la sala {sala} el {fecha} a las {hora}.")
            print(f"La función se solapa con la película '{pelicula_solapada}'.")
        else:
            print(f"No se puede cargar la función: ya existe otra función solapada en la sala {sala} el {fecha} a las {hora}.")
        return False

    fecha_compacta = fecha.replace('-', '')
    conteo_existente = sum(
        1
        for datos in funciones.values()
        if str(datos.get("Película", "")).strip().lower() == pelicula_normalizada and datos.get("Fecha") == fecha
    )
    sufijo = chr(ord('a') + conteo_existente)
    clave_nueva = f"{pelicula_clave_original}_{fecha_compacta}_{sufijo}"

    if clave_nueva in funciones:
        print("Error interno: ya existe una función con ese identificador. Intente nuevamente.")
        return False

    butacas = crear_butacas(6, 6)

    funciones[clave_nueva] = {
        "Película": pelicula_clave_original,  # Usar la clave original normalizada
        "Fecha": fecha,  # DD-MM-YY
        "Hora": hora,    # HH:MM
        "Sala": sala,
        "Butacas": butacas
    }

    print(f"Función cargada exitosamente. ID asignado: {clave_nueva}")
    return True


#Funcion para consultar funciones
def consultar_funciones():
    """
    Función para mostrar todas las funciones cargadas en el sistema
    """
    if not funciones:
        print("No se puede, consultar las funciones porque no hay ninguna cargada.")
    else:
        for fid, datos in funciones.items():
            print(f"ID: {fid} | {datos['Película']} - {datos['Fecha']} - {datos['Hora']} - Sala {datos['Sala']}")

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
    """
    Función para generar un ID para cada nueva reserva.
    """
    siguiente = len(reservas) + 1
    if siguiente < 10:
        return f"R000{siguiente}"
    elif siguiente < 100:
        return f"R00{siguiente}"
    elif siguiente < 1000:
        return f"R0{siguiente}"
    else:
        return f"R{siguiente}"

#Funcion para crear reserva
def crear_reserva(usuario, funcion_id, fila, columna, precio_base=None):
    """
    Crea una reserva si la función existe y la butaca está libre.
    Marca la butaca como 'Ocupada' y guarda la reserva en 'reservas'.
    Retorna el id de reserva si se crea, o None si falla.
    """
    from validacion import validar_butaca_disponible, butaca_existe
    
    # Normalizar usuario a minúsculas
    usuario = usuario.strip().lower() if usuario else ""
    
    if funcion_id not in funciones:
        print(f"La función '{funcion_id}' no existe.")
        return None
    
    # Validar que la película de la función aún existe en el sistema
    datos_funcion = funciones[funcion_id]
    pelicula_nombre = datos_funcion.get("Película", "")
    
    if pelicula_nombre:
        # Buscar la película (case-insensitive)
        pelicula_existe = False
        pelicula_normalizada = pelicula_nombre.strip().lower()
        for pelicula_key in peliculas.keys():
            if pelicula_key.lower() == pelicula_normalizada:
                pelicula_existe = True
                break
        
        if not pelicula_existe:
            print(f"ERROR: La película '{pelicula_nombre}' asociada a esta función ya no existe en el sistema.")
            print("No se puede crear una reserva para una función de una película eliminada.")
            return None

    # Verificar que la butaca existe
    if not butaca_existe(funcion_id, fila, columna, funciones):
        print("Butaca inexistente para esa función.")
        return None

    # Verificar que la butaca está libre
    if not validar_butaca_disponible(funcion_id, fila, columna, funciones):
        print("La butaca ya está ocupada.")
        return None
    
    # Si no se proporciona el precio, se calcula
    if precio_base is None:
        # Preguntar tipo de entrada
        print("\n--- Tipo de Entrada ---")
        print("1. Normal (2D)")
        print("2. 3D")
        print("3. VIP")
        print("-1. Volver al menú")
        bandera_tipo = True
        tipo_entrada = "normal"
        while bandera_tipo:
            opcion_tipo = input("Seleccione el tipo de entrada: ").strip()
            if opcion_tipo == "1":
                tipo_entrada = "normal"
                bandera_tipo = False
            elif opcion_tipo == "2":
                tipo_entrada = "3D"
                bandera_tipo = False
            elif opcion_tipo == "3":
                tipo_entrada = "VIP"
                bandera_tipo = False
            elif opcion_tipo == "-1":
                print("Operación cancelada. Volviendo al menú.")
                return None
            else:
                print("ERROR: Opción no válida. Intente nuevamente.")
        
        # Preguntar si aplica promoción o entrada especial
        print("\n--- Promoción o Entrada Especial ---")
        print("1. Sin promoción/descuento")
        print("2. Entrada para niños (menores de 12 años)")
        print("3. Entrada para jubilados")
        print("4. Entrada para estudiantes")
        print("-1. Volver al menú")
        bandera_descuento = True
        descuento = None
        while bandera_descuento:
            opcion_descuento = input("Seleccione una opción: ").strip()
            if opcion_descuento == "1":
                descuento = None
                bandera_descuento = False
            elif opcion_descuento == "2":
                descuento = "niños"
                bandera_descuento = False
            elif opcion_descuento == "3":
                descuento = "jubilado"
                bandera_descuento = False
            elif opcion_descuento == "4":
                descuento = "estudiante"
                bandera_descuento = False
            elif opcion_descuento == "-1":
                print("Operación cancelada. Volviendo al menú.")
                return None
            else:
                print("ERROR: Opción no válida. Intente nuevamente.")
        
        # Calcular precio automáticamente
        precio_base = calcular_precio_entrada(tipo_entrada, descuento)
        print(f"\n✓ Precio calculado automáticamente: ${precio_base}")

    funciones[funcion_id]["Butacas"][fila - 1][columna - 1] = "Ocupada"

    reserva_id = generar_id_reserva()
    reservas[reserva_id] = {
        "Usuario": usuario,
        "FuncionID": funcion_id,
        "Butaca": {"Fila": fila, "Columna": columna},
        "Precio": precio_base,
        "Estado": "Activa"
    }

    print(f"Reserva creada. ID: {reserva_id} - Usuario: {usuario} - Función: {funcion_id} - Butaca F{fila}A{columna} - Precio: ${precio_base}")
    return reserva_id


#Funcion para consultar reservas por funcion
def consultar_reservas_por_funcion(funcion_id):
    """
    Función para mostrar todas las reservas asociadas a una función.
    """
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
    """
    Función para mostrar todas las reservas realizadas por un usuario.
    """
    # Normalizar usuario a minúsculas para búsqueda case-insensitive
    usuario_normalizado = usuario.strip().lower() if usuario else ""
    
    hay = False
    usuario_encontrado = None
    for rid, r in reservas.items():
        usuario_reserva = r.get("Usuario", "")
        if usuario_reserva.lower() == usuario_normalizado:
            if not hay:
                usuario_encontrado = usuario_reserva  # Guardar el formato original
                print(f"\nReservas del usuario '{usuario_encontrado}':")
                hay = True
            print(f"- {rid} | Función: {r['FuncionID']} | Butaca: F{r['Butaca']['Fila']}A{r['Butaca']['Columna']} | "
                  f"Precio: {r['Precio']} | Estado: {r['Estado']}")
    if not hay:
        print(f"El usuario '{usuario}' no tiene reservas registradas.")
    return True


#Funcion para cambiar butaca
def cambiar_butaca(reserva_id, nueva_fila, nueva_columna):
    """
    Función para cambiar la butaca de una reserva existente.
    """
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
    from validacion import validar_butaca_disponible, butaca_existe
    
    if funcion_id not in funciones:
        print(f"La función '{funcion_id}' no existe.")
        return False

    if not butaca_existe(funcion_id, nueva_fila, nueva_columna, funciones):
        print("La nueva butaca no existe para esta función.")
        return False

    # 5) Verificar disponibilidad de la nueva butaca
    if not validar_butaca_disponible(funcion_id, nueva_fila, nueva_columna, funciones):
        print("La nueva butaca está ocupada.")
        return False

    # 6) Confirmar cambio de butaca
    from validacion import confirmar_accion
    if not confirmar_accion(f"cambiar la butaca de la reserva '{reserva_id}' de F{fila_actual}A{col_actual} a F{nueva_fila}A{nueva_columna}"):
        print("Cambio de butaca cancelado.")
        return False

    # 7) Efectuar el cambio: liberar vieja y ocupar nueva
    funciones[funcion_id]["Butacas"][fila_actual - 1][col_actual - 1] = "Libre"
    funciones[funcion_id]["Butacas"][nueva_fila - 1][nueva_columna - 1] = "Ocupada"

    # 8) Actualizar la reserva
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
    from validacion import confirmar_accion
    
    #1 Validar existencia de la reserva
    if reserva_id not in reservas:
        print(f"La reserva '{reserva_id}' no existe.")
        return False

    #2 Validar estado actual
    estado_actual = reservas[reserva_id].get("Estado")
    if estado_actual != "Activa":
        print(f"La reserva '{reserva_id}' no está activa (estado: {estado_actual}).")
        return False
    
    #3 Confirmar cancelación
    if not confirmar_accion(f"cancelar la reserva '{reserva_id}'"):
        print("Cancelación de compra cancelada.")
        return False

    #3 Obtener datos
    funcion_id = reservas[reserva_id]["FuncionID"]
    fila = reservas[reserva_id]["Butaca"]["Fila"]
    columna = reservas[reserva_id]["Butaca"]["Columna"]

    #4 Intentar liberar butaca en la función (si existe)
    from validacion import butaca_existe
    
    if funcion_id in funciones:
        if butaca_existe(funcion_id, fila, columna, funciones):
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
    """
    Funcion para egenrar un reporte de ocupacion
    """
    try:
        if not funciones:
            print("No hay funciones cargadas en el sistema.")
            return False
        else:
            for func_id, datos in sorted(funciones.items(), key=lambda x: x[1]["Película"]):
                butacas = datos["Butacas"]
                total = len(butacas) * len(butacas[0])

                ocupadas = sum([1 for fila in butacas for asiento in fila if asiento == "Ocupada"])

                porcentaje = round((ocupadas / total) * 100) if total > 0 else 0

                print(f"{datos['Película']} - {datos['Fecha']} - {datos['Hora']} - Sala {datos['Sala']}")
                print(f"Butacas ocupadas: {ocupadas}/{total} ({porcentaje}%)")

            return True
    except KeyError as e:
        print(f"Error: falta la clave {e} en alguna función.")
        return False
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return False


#Funcion para guardar datos
def guardar_datos():
    """
    Funcion para guardar datos utilziando archivos JSON
    """
    try:
        # Usar rutas absolutas para consistencia
        ruta_admins = os.path.join(os.path.dirname(__file__), "admins.txt")
        ruta_peliculas = os.path.join(os.path.dirname(__file__), "peliculas.txt")
        ruta_funciones = os.path.join(os.path.dirname(__file__), "funciones.txt")
        ruta_reservas = os.path.join(os.path.dirname(__file__), "reservas.txt")
        
        with open(ruta_admins, "w", encoding="utf-8") as f:
            json.dump(admins, f, indent=4, ensure_ascii=False)

        with open(ruta_peliculas, "w", encoding="utf-8") as f:
            json.dump(peliculas, f, indent=4, ensure_ascii=False)

        with open(ruta_funciones, "w", encoding="utf-8") as f:
            json.dump(funciones, f, indent=4, ensure_ascii=False)

        with open(ruta_reservas, "w", encoding="utf-8") as f:
            json.dump(reservas, f, indent=4, ensure_ascii=False)

        print("Datos guardados.")
        return True
    except Exception as e:
        print(f"Error al guardar los datos: {e}")
        return False

#Funcion para cargar datos
def cargar_datos():
    """
    Función para cargar administradores, películas, funciones y reservas desde archivos JSON.
    """
    global admins, peliculas, funciones, reservas
    try:
        # Usar la misma ruta que validacion.py para consistencia
        ruta_admins = os.path.join(os.path.dirname(__file__), "admins.txt")
        with open(ruta_admins, "r", encoding="utf-8") as f:
            admins = json.load(f)
    except FileNotFoundError:
        admins = {}

    try:
        # Usar rutas absolutas para consistencia
        ruta_peliculas = os.path.join(os.path.dirname(__file__), "peliculas.txt")
        with open(ruta_peliculas, "r", encoding="utf-8") as f:
            peliculas = json.load(f)
    except FileNotFoundError:
        peliculas = {}

    try:
        ruta_funciones = os.path.join(os.path.dirname(__file__), "funciones.txt")
        with open(ruta_funciones, "r", encoding="utf-8") as f:
            funciones = json.load(f)
    except FileNotFoundError:
        funciones = {}

    try:
        ruta_reservas = os.path.join(os.path.dirname(__file__), "reservas.txt")
        with open(ruta_reservas, "r", encoding="utf-8") as f:
            reservas = json.load(f)
    except FileNotFoundError:
        reservas = {}

    print("Datos cargados.")
    return True


def guardar_admins():
    """
    Función para guardar la lista de administradores en su archivo JSON.
    """
    try:
        # Usar la misma ruta que validacion.py para consistencia
        ruta_admins = os.path.join(os.path.dirname(__file__), "admins.txt")
        with open(ruta_admins, "w", encoding="utf-8") as f:
            json.dump(admins, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar administradores: {e}")
        return False


#Menu gestion peliculas
def menu_gestion_peliculas():
    """
    Menú para gestionar películas: agregar, modificar, eliminar y listar.
    """
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
            from validacion import validar_pelicula_existente, validar_datos_no_nulos
            
            # Validar título
            bandera = True
            while bandera:
                pelicula = input("Título de la película: ").strip()
                if not pelicula:
                    print("ERROR: El título no puede estar vacío.")
                    continue
                if validar_pelicula_existente(pelicula, peliculas):
                    print("ERROR: La película ya existe en el sistema.")
                    continue
                bandera = False
            
            # Validar género
            from validacion import validar_solo_letras
            bandera = True
            while bandera:
                genero = input("Género: ").strip()
                if not genero:
                    print("ERROR: El género no puede estar vacío.")
                    continue
                if not validar_solo_letras(genero):
                    print("ERROR: El género solo puede contener letras, espacios y guiones. No se permiten números.")
                    continue
                bandera = False
            
            # Validar duración
            bandera = True
            while bandera:
                duracion_str = input("Duración (minutos): ").strip()
                duracion = validar_numero_positivo(duracion_str, "La duración debe ser un número positivo.")
                if duracion is None:
                    continue
                bandera = False
            
            # Validar fecha
            bandera = True
            while bandera:
                fecha = input("Fecha de estreno (DD-MM-YY): ").strip()
                if not fecha:
                    print("ERROR: La fecha no puede estar vacía.")
                    continue
                if not validar_formato_fecha(fecha):
                    print("ERROR: La fecha debe tener formato DD-MM-YY (ej: 15-11-25).")
                    continue
                bandera = False
            
            # Si todas las validaciones pasaron, agregar película
            if agregar_pelicula(pelicula, genero, duracion, fecha):
                pausar()
            else:
                pausar()
        
        elif opcion == "2":
            from validacion import validar_pelicula_existente
            
            # Validar que la película existe
            bandera = True
            while bandera:
                pelicula = input("Película a modificar: ").strip()
                if not pelicula:
                    print("ERROR: El título no puede estar vacío.")
                    continue
                if not validar_pelicula_existente(pelicula, peliculas):
                    print("ERROR: La película no existe en el sistema.")
                    continue
                bandera = False
            
            # Validar género (opcional)
            from validacion import validar_solo_letras
            nuevo_genero = None
            bandera = True
            while bandera:
                nuevo_genero_str = input("Nuevo género (Enter para no cambiar): ").strip()
                if not nuevo_genero_str:
                    # Si está vacío, no cambiar el género
                    bandera = False
                    break
                if not validar_solo_letras(nuevo_genero_str):
                    print("ERROR: El género solo puede contener letras, espacios y guiones. No se permiten números.")
                    continue
                nuevo_genero = nuevo_genero_str
                bandera = False
            
            # Validar duración (opcional)
            nueva_duracion = None
            bandera = True
            while bandera:
                nueva_duracion_str = input("Nueva duración (Enter para no cambiar): ").strip()
                if not nueva_duracion_str:
                    # Si está vacío, no cambiar la duración
                    bandera = False
                    break
                nueva_duracion = validar_numero_positivo(nueva_duracion_str, "La duración debe ser un número positivo.")
                if nueva_duracion is None:
                    # Si es inválido, mostrar error y volver a pedir
                    continue
                bandera = False
            
            # Validar fecha (opcional)
            nueva_fecha = None
            bandera = True
            while bandera:
                nueva_fecha_str = input("Nueva fecha (DD-MM-YY, Enter para no cambiar): ").strip()
                if not nueva_fecha_str:
                    # Si está vacío, no cambiar la fecha
                    bandera = False
                    break
                if not validar_formato_fecha(nueva_fecha_str):
                    print("ERROR: La fecha debe tener formato DD-MM-YY (ej: 15-11-25).")
                    continue  # Volver a pedir la fecha
                nueva_fecha = nueva_fecha_str
                bandera = False
            
            # Si todas las validaciones pasaron, modificar película
            modificar_pelicula(pelicula, nuevo_genero, nueva_duracion, nueva_fecha)
            pausar()
        
        elif opcion == "3":
            from validacion import validar_pelicula_existente
            
            # Validar que la película existe
            bandera = True
            while bandera:
                pelicula = input("Película a eliminar (o -1 para volver): ").strip()
                if pelicula == "-1":
                    bandera = False
                    break
                if not pelicula:
                    print("ERROR: El título no puede estar vacío.")
                    continue
                if not validar_pelicula_existente(pelicula, peliculas):
                    print("ERROR: La película no existe en el sistema.")
                    print("\nOpciones:")
                    print("1. Intentar con otra película")
                    print("-1. Volver al menú")
                    opcion_error = input("Seleccione una opción: ").strip()
                    if opcion_error == "-1":
                        bandera = False
                        break
                    elif opcion_error == "1":
                        continue
                    else:
                        print("Opción no válida. Volviendo al menú.")
                        bandera = False
                        break
                else:
                    # Si la validación pasó, eliminar película
                    eliminar_pelicula(pelicula)
                    pausar()
                    bandera = False
        elif opcion == "4":
            ver_todas_las_peliculas()
            pausar()
        
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")
            pausar()


#Menu gestion funciones
def menu_gestion_funciones():
    """
    Menú para gestionar funciones: cargar, consultar horarios y ver disponibilidad de butacas.
    """
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
            from validacion import validar_pelicula_existente
            
            # Validar película
            bandera = True
            while bandera:
                pelicula = input("Película (o -1 para volver): ").strip()
                if pelicula == "-1":
                    bandera = False
                    break  # Salir del bucle y volver al menú
                if not pelicula:
                    print("ERROR: El título de la película no puede estar vacío.")
                    continue
                if not validar_pelicula_existente(pelicula, peliculas):
                    print("ERROR: La película no existe en el sistema. Debe registrarla primero.")
                    print("Ingrese -1 para volver al menú.")
                    continue
                bandera = False
            
            # Si el usuario salió con -1, continuar al siguiente ciclo del menú
            if pelicula == "-1":
                continue
            
            # Validar fecha
            bandera = True
            while bandera:
                fecha = input("Fecha (DD-MM-YY): ").strip()
                if not fecha:
                    print("ERROR: La fecha no puede estar vacía.")
                    continue
                if not validar_formato_fecha(fecha):
                    print("ERROR: La fecha debe tener formato DD-MM-YY (ej: 15-11-25).")
                    continue
                bandera = False
            
            # Validar hora
            bandera = True
            while bandera:
                hora = input("Hora (HH:MM): ").strip()
                if not hora:
                    print("ERROR: La hora no puede estar vacía.")
                    continue
                if not validar_formato_hora(hora):
                    print("ERROR: La hora debe tener formato HH:MM (ej: 18:30).")
                    continue
                bandera = False
            
            # Validar sala
            bandera = True
            while bandera:
                sala_str = input("Sala: ").strip()
                if not sala_str:
                    print("ERROR: La sala no puede estar vacía.")
                    continue
                sala = validar_sala(sala_str)
                if sala is None:
                    continue
                bandera = False
            
            # Si todas las validaciones pasaron, cargar función
            if cargar_funcion(pelicula, fecha, hora, sala):
                pausar()
            else:
                pausar()
        
        elif opcion == "2":
            consultar_funciones()
            pausar()
        
        elif opcion == "3":
            # Validar película
            bandera = True
            pelicula = None
            while bandera:
                pelicula = input("Pelicula: ").strip()
                if not pelicula:
                    print("ERROR: El título de la película no puede estar vacío.")
                    continue
                
                # Verificar si la película existe
                pelicula_existe = False
                pelicula_normalizada = pelicula.lower()
                pelicula_clave_original = None
                for pelicula_key in peliculas.keys():
                    if pelicula_key.lower() == pelicula_normalizada:
                        pelicula_existe = True
                        pelicula_clave_original = pelicula_key
                        break
                
                if not pelicula_existe:
                    print(f"ERROR: La película '{pelicula}' no existe en el sistema.")
                    print("\nOpciones:")
                    print("1. Intentar con otra película")
                    print("-1. Volver al menú")
                    opcion_error = input("Seleccione una opción: ").strip()
                    if opcion_error == "-1":
                        bandera = False
                        break
                    elif opcion_error == "1":
                        continue
                    else:
                        print("ERROR: Opción no válida. Volviendo al menú.")
                        bandera = False
                        break
                else:
                    pelicula = pelicula_clave_original
                    bandera = False
            
            if pelicula is None:
                pausar()
                continue
            
            # Validar fecha
            from admin import validar_formato_fecha
            bandera = True
            fecha = None
            while bandera:
                fecha_str = input("Fecha (DD-MM-YY): ").strip()
                if not fecha_str:
                    print("ERROR: La fecha no puede estar vacía.")
                    continue
                if not validar_formato_fecha(fecha_str):
                    print("ERROR: La fecha debe tener formato DD-MM-YY (ej: 15-11-25).")
                    continue
                fecha = fecha_str
                bandera = False
            
            funciones_encontradas = []
            for fid, datos in funciones.items():
                titulo = str(datos.get("Película", "")).strip().lower()
                fecha_funcion = datos.get("Fecha")
                if titulo == pelicula.lower() and fecha_funcion == fecha:
                    funciones_encontradas.append((datos.get("Hora", ""), datos.get("Sala", ""), fid))
            if not funciones_encontradas:
                print(f"No se encontraron funciones para '{pelicula}' en la fecha {fecha}.")
            else:
                funciones_encontradas.sort(key=lambda x: (x[0], x[1]))
                for hora, sala, fid in funciones_encontradas:
                    print(f"\nFunción ID {fid}: Hora {hora} | Sala {sala}")
                    ver_disponibilidad_funcion(fid)
            pausar()
        
        elif opcion == "4":
            from usuario import ver_horarios_pelicula
            
            # Validar película
            bandera = True
            pelicula = None
            while bandera:
                pelicula = input("Ingrese el título de la película: ").strip()
                if not pelicula:
                    print("ERROR: El título de la película no puede estar vacío.")
                    continue
                
                # Verificar si la película existe
                pelicula_existe = False
                pelicula_normalizada = pelicula.lower()
                pelicula_clave_original = None
                for pelicula_key in peliculas.keys():
                    if pelicula_key.lower() == pelicula_normalizada:
                        pelicula_existe = True
                        pelicula_clave_original = pelicula_key
                        break
                
                if not pelicula_existe:
                    print(f"ERROR: La película '{pelicula}' no existe en el sistema.")
                    print("\nOpciones:")
                    print("1. Intentar con otra película")
                    print("-1. Volver al menú")
                    opcion_error = input("Seleccione una opción: ").strip()
                    if opcion_error == "-1":
                        bandera = False
                        break
                    elif opcion_error == "1":
                        continue
                    else:
                        print("ERROR: Opción no válida. Volviendo al menú.")
                        bandera = False
                        break
                else:
                    pelicula = pelicula_clave_original
                    bandera = False
            
            if pelicula is None:
                pausar()
                continue
            
            fecha = input("Ingrese la fecha (DD-MM-YY) o presione \"Enter\" para ver todos los horarios: ")
            fecha = fecha if fecha.strip() else None
            ver_horarios_pelicula(pelicula, fecha, funciones)
            pausar()
        
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")
            pausar()


#Menu gestion reservas
def menu_gestion_reservas():
    """
    Menú para gestionar reservas: crear, consultar, cancelar y cambiar butacas.
    """
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
            from validacion import verificar_usuario_registrado, validar_butaca_disponible
            
            # Validar usuario
            bandera = True
            while bandera:
                usuario = input("Usuario (nombre o mail, o -1 para volver): ").strip().lower()  # Normalizar a minúsculas
                if usuario == "-1":
                    bandera = False
                    break
                if not usuario:
                    print("ERROR: El usuario no puede estar vacío.")
                    continue
                if not verificar_usuario_registrado(usuario):
                    print("ERROR: El usuario no está registrado en el sistema.")
                    continue
                bandera = False
            
            # Si el usuario salió con -1, continuar al siguiente ciclo del menú
            if usuario == "-1":
                continue
            
            # Validar función ID
            bandera = True
            while bandera:
                print("Formato de ID: pelicula_fechaCompacta_letra (ej.: Avatar_101024_a)")
                funcion_id = input("ID de la función (o -1 para volver): ").strip()
                if funcion_id == "-1":
                    bandera = False
                    break
                if not funcion_id:
                    print("ERROR: El ID de función no puede estar vacío.")
                    continue
                if funcion_id not in funciones:
                    print("ERROR: La función no existe en el sistema.")
                    continue
                bandera = False
            
            # Si el usuario salió con -1, continuar al siguiente ciclo del menú
            if funcion_id == "-1":
                continue
            
            # Validar fila, columna y disponibilidad de butaca
            bandera = True
            salir_butaca = False
            while bandera:
                # Validar fila
                bandera_fila = True
                while bandera_fila:
                    fila_str = input("Fila (número empezando en 1, o -1 para volver): ").strip()
                    if fila_str == "-1":
                        bandera_fila = False
                        salir_butaca = True
                        break
                    fila = validar_numero_positivo(fila_str, "La fila debe ser un número positivo.")
                    if fila is None:
                        continue
                    bandera_fila = False
                
                # Si el usuario salió con -1, salir del bucle de butaca
                if salir_butaca:
                    bandera = False
                    break
                
                # Validar columna
                bandera_columna = True
                while bandera_columna:
                    columna_str = input("Asiento (número empezando en 1, o -1 para volver): ").strip()
                    if columna_str == "-1":
                        bandera_columna = False
                        salir_butaca = True
                        break
                    columna = validar_numero_positivo(columna_str, "El asiento debe ser un número positivo.")
                    if columna is None:
                        continue
                    bandera_columna = False
                
                # Si el usuario salió con -1, salir del bucle de butaca
                if salir_butaca:
                    bandera = False
                    break
                
                # Validar que la butaca esté disponible
                if not validar_butaca_disponible(funcion_id, fila, columna, funciones):
                    print("ERROR: La butaca seleccionada no está disponible.")
                    print("\nOpciones:")
                    print("1. Elegir otra butaca")
                    print("2. Volver al menú")
                    opcion_butaca = input("Seleccione una opción: ").strip()
                    if opcion_butaca == "2":
                        bandera = False
                        salir_butaca = True
                        break  # Salir del bucle y volver al menú
                    elif opcion_butaca == "1":
                        continue  # Volver a pedir fila y columna
                    else:
                        print("Opción no válida. Volviendo al menú.")
                        bandera = False
                        salir_butaca = True
                        break
                else:
                    bandera = False
            
            # Si el usuario eligió volver al menú, continuar al siguiente ciclo
            if salir_butaca:
                continue
            
            # El precio se calcula automáticamente en crear_reserva
            # Si todas las validaciones pasaron, crear reserva
            if crear_reserva(usuario, funcion_id, fila, columna, None):
                pausar()
            else:
                pausar()
        
        elif opcion == "2":
            print("Formato de ID: pelicula_fechaCompacta_letra (ej.: Avatar_101024_a)")
            funcion_id = input("ID de la función: ")
            consultar_reservas_por_funcion(funcion_id)
            pausar()
        
        elif opcion == "3":
            usuario = input("Usuario (nombre o mail): ")
            consultar_reservas_por_usuario(usuario)
            pausar()
        
        elif opcion == "4":
            reserva_id = input("ID de la reserva (ej.: R0001): ")
            cancelar_compra(reserva_id)
            pausar()
        
        elif opcion == "5":
            from validacion import validar_butaca_disponible
            
            # Validar reserva ID
            bandera = True
            while bandera:
                reserva_id = input("ID de la reserva (ej.: R0001): ").strip()
                if not reserva_id:
                    print("ERROR: El ID de reserva no puede estar vacío.")
                    continue
                if reserva_id not in reservas:
                    print("ERROR: La reserva no existe en el sistema.")
                    continue
                bandera = False
            
            # Validar nueva fila
            bandera = True
            while bandera:
                nueva_fila_str = input("Nueva fila (número empezando en 1): ").strip()
                nueva_fila = validar_numero_positivo(nueva_fila_str, "La fila debe ser un número positivo.")
                if nueva_fila is None:
                    continue
                bandera = False
            
            # Validar nueva columna
            bandera = True
            while bandera:
                nueva_col_str = input("Nuevo asiento (número empezando en 1): ").strip()
                nueva_col = validar_numero_positivo(nueva_col_str, "El asiento debe ser un número positivo.")
                if nueva_col is None:
                    continue
                bandera = False
            
            # Validar que la nueva butaca esté disponible
            funcion_id_reserva = reservas[reserva_id].get("FuncionID", "")
            if funcion_id_reserva and not validar_butaca_disponible(funcion_id_reserva, nueva_fila, nueva_col, funciones):
                print("ERROR: La nueva butaca no está disponible.")
                pausar()
                continue
            
            # Si todas las validaciones pasaron, cambiar butaca
            if cambiar_butaca(reserva_id, nueva_fila, nueva_col):
                pausar()
            else:
                pausar()
        
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")
            pausar()


#Menu principal del administrador
def mainAdmin():
    """
    Menú principal del administrador con acceso a todas las gestiones y reportes.
    """
    cargar_datos()
    while True:
        clear()
        print("\n" + "="*50)
        print("    MENÚ ADMINISTRADOR")
        print("="*50)
        print("1. Gestión de Películas")
        print("2. Gestión de Funciones")
        print("3. Gestión de Reservas")
        print("4. Gestión de Precios y Promociones")
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
            menu_gestion_precios()
        elif opcion == "5":
            generar_reporte_ocupacion()
            pausar()
        elif opcion == "6":
            guardar_datos()
        elif opcion == "0":
            print("Sesión cerrada.")
            return  # Volver al menú principal
        else:
            print("Opción no válida.")


#Funcion de login administrador y menu
def login_admin_menu():
    """
    Menú de acceso para administradores: registro, inicio de sesión o volver al principal.
    """
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
            from validacion import validar_mail, validar_contrasena
            bandera = True
            while bandera:
                clave_registro = input("Clave de registro (o -1 para volver): ")
                if clave_registro == "-1":
                    bandera = False
                elif clave_registro != "Uade123":
                    print("Clave incorrecta.")
                else:
                    # Validar usuario
                    bandera_usuario = True
                    while bandera_usuario:
                        usuario = input("Usuario: ").strip().lower()  # Normalizar a minúsculas
                        if not usuario:
                            print("ERROR: El usuario no puede estar vacío.")
                            continue
                        # Verificar si el usuario ya existe (búsqueda case-insensitive)
                        usuario_existe = False
                        for usuario_key in admins.keys():
                            if usuario_key.lower() == usuario:
                                usuario_existe = True
                                break
                        if usuario_existe:
                            print("ERROR: El usuario ya existe.")
                            continue
                        bandera_usuario = False
                    
                    # Validar contraseña
                    bandera = True
                    while bandera:
                        contrasenia = input("Contraseña: ").strip()
                        if not contrasenia:
                            print("ERROR: La contraseña no puede estar vacía.")
                            continue
                        if not validar_contrasena(contrasenia):
                            print("ERROR: La contraseña debe tener al menos 5 caracteres.")
                            continue
                        bandera = False
                    
                    # Validar mail
                    bandera = True
                    while bandera:
                        mail = input("Mail: ").strip().lower()  # Normalizar a minúsculas
                        if not mail:
                            print("ERROR: El mail no puede estar vacío.")
                            continue
                        if not validar_mail(mail):
                            print("ERROR: El mail debe tener un dominio válido (gmail, hotmail, outlook, yahoo, cineuade.com, etc.).")
                            continue
                        bandera = False
                    
                    # Validar nombre
                    from validacion import validar_solo_letras
                    bandera = True
                    while bandera:
                        nombre = input("Nombre: ").strip()
                        if not nombre:
                            print("ERROR: El nombre no puede estar vacío.")
                            continue
                        if not validar_solo_letras(nombre):
                            print("ERROR: El nombre solo puede contener letras, espacios y guiones. No se permiten números.")
                            continue
                        bandera = False
                    
                    # Validar apellido
                    bandera = True
                    while bandera:
                        apellido = input("Apellido: ").strip()
                        if not apellido:
                            print("ERROR: El apellido no puede estar vacío.")
                            continue
                        if not validar_solo_letras(apellido):
                            print("ERROR: El apellido solo puede contener letras, espacios y guiones. No se permiten números.")
                            continue
                        bandera = False
                    
                    # Si todas las validaciones pasaron, registrar
                    if registrar_admin(usuario, contrasenia, mail, nombre, apellido):
                        pausar()  # Pausar para que el usuario vea el mensaje de éxito
                        bandera = False
                    else:
                        pausar()  # Pausar también en caso de error
                        bandera = False
        
        elif opcion == "2":
            bandera = True
            while bandera:
                usuario = input("Usuario (o -1 para volver): ").strip().lower()  # Normalizar a minúsculas
                if usuario == "-1":
                    bandera = False
                    continue
                contrasenia = input("Contraseña: ").strip()
                if login_admin(usuario, contrasenia):
                    pausar()
                    mainAdmin()
                    return
                else:
                    print("Credenciales incorrectas. Intente nuevamente o ingrese -1 para volver.")
                    pausar()
        
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


#Variables globales del sistema
admins = {}
peliculas = {}
funciones = {}
reservas = {}