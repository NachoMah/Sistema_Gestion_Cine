import json
import os
import platform
import validacion

def clear():
    """
    Función para limpiar la consola según el sistema operativo detectado."
    """
    try:
        current_os = platform.system()
        if current_os == "Windows":
            os.system('cls') # Windows
        else:
            os.system('clear') # macOS/Linux
    except Exception as e:
        print(f"Error al limpiar la pantalla: {e}")   

def pausar():
    """
    Función para pausar la ejecución hasta que el usuario presione Enter.
    """
    input("\nPresione Enter para continuar...")

usuarios = {}

#Funcion para registrar usuario
def registrar_usuario(mail, nombre, apellido, edad, contrasenia):
    """
    Función para registrar un nuevo usuario en el sistema.
    """
    if not validacion.validar_mail(mail):
        print("Mail inválido. Debe tener un dominio válido (gmail, yahoo, etc.)")
        return False
    
    if not validacion.validar_contrasena(contrasenia):
        print("Contraseña inválida. Debe tener al menos 8 caracteres.")
        return False
    
    if not validacion.validar_datos_no_nulos([mail, nombre, apellido, edad, contrasenia]):
        print("ERROR: Todos los campos son obligatorios y no pueden estar vacíos.")
        return False
    
    nombre_usuario = mail
    
    if validacion.validar_usuario_registrado(nombre_usuario):
        print("El usuario ya existe")
        return False
    
    try:
        if nombre_usuario in usuarios:
            print("El usuario ya existe")
            return False
        
        usuarios[nombre_usuario] = {
            "nombre": nombre,
            "apellido": apellido,
            "edad": edad,
            "mail": mail,
            "contraseña": contrasenia,
            "reservas": []
        }
        guardar_usuarios()
        print(f"Usuario '{nombre_usuario}' registrado correctamente.")
        return True
    
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return False


#Funcion para login de usuario
def login_usuario(usuario, contrasena):
    """
    Función para iniciar sesión verificando usuario y contraseña.
    """
    try:
        if usuario not in usuarios:
            print("El usuario no existe.")
            return False
        if usuarios[usuario]["contraseña"] != contrasena:
            print("Contraseña incorrecta.")
            return False
        print(f"¡Bienvenido {usuario}!")
        return True
    except Exception as e:
        print(f"Error en el inicio de sesión: {e}")
        return False


#Funcion para ver cartelera
def ver_cartelera():
    """
    Función para mostrar la cartelera de películas disponibles.
    """
    try:
        peliculas_disponibles = cargar_peliculas()
        if not peliculas_disponibles:
            print("No hay películas en cartelera.")
            return []
        print("\nCartelera actual:")
        for p in sorted(peliculas_disponibles, key=lambda x: x["titulo"]):
            print(f"- {p['titulo']} ({p['genero']}, {p['duracion']} min)")
        return peliculas_disponibles
    except Exception as e:
        print(f"Error al mostrar la cartelera: {e}")
        return []


#Funcion para ver horarios de pelicula
def ver_horarios_pelicula(pelicula, fecha=None, funciones_dict=None):
    """
    Función para mostrar los horarios disponibles de una película dada
    """
    try:
        if not isinstance(pelicula, str) or not pelicula.strip():
            print("Debe indicar el título de la película.")
            return []

        if not funciones_dict:
            print("No hay funciones cargadas.")
            return []

        resultados = []
        titulo = pelicula.strip().lower()

        for fid, datos in funciones_dict.items():
            if str(datos.get("Película", "")).strip().lower() == titulo:
                if fecha is None or datos.get("Fecha") == fecha:
                    resultados.append({
                        "funcion_id": fid,
                        "fecha": datos.get("Fecha"),
                        "hora": datos.get("Hora"),
                        "sala": str(datos.get("Sala")),
                    })

        if not resultados:
            if fecha:
                print(f"No hay funciones para '{pelicula}' el {fecha}.")
            else:
                print(f"No hay funciones programadas para '{pelicula}'.")
            return []

        resultados.sort(key=lambda x: (x["fecha"], x["hora"], x["sala"]))

        print(f"\nHorarios para '{pelicula}'" + (f" - {fecha}" if fecha else "") + ":")
        for r in resultados:
            print(f"- {r['fecha']} {r['hora']} | Sala {r['sala']} | ID: {r['funcion_id']}")

        return resultados

    except Exception as e:
        print(f"Error al consultar horarios: {e}")
        return []


#Funcion para consultar butacas
def consultar_butacas(funcion_id, funciones):
    """
    Función para mostrar la disponibilidad de butacas de una función.
    """
    try:
        if funcion_id not in funciones:
            print(f"La función '{funcion_id}' no existe.")
            return False
        
        datos_funcion = funciones[funcion_id]
        butacas = datos_funcion["Butacas"]
        
        print(f"Disponibilidad de butacas - {datos_funcion['Película']}")
        print(f"Fecha: {datos_funcion['Fecha']} | Hora: {datos_funcion['Hora']} | Sala: {datos_funcion['Sala']}")
        print("   " + "  ".join([f"A{col+1}" for col in range(len(butacas[0]))]))
        
        for i, fila in enumerate(butacas):
            fila_impresa = ["L" if asiento == "Libre" else "O" for asiento in fila]
            print(f"F{i+1} " + "  ".join(fila_impresa))
            
        return butacas
    
    except Exception as e:
        print(f"Error al consultar butacas: {e}")
        return False

#Funcion para comprar entrada
def comprar_entrada(usuario, funcion_id, butaca, funciones):
    """
    Función para registrar la compra de una entrada y generar una reserva.
    """
    if not validacion.confirmar_accion(f"comprar la entrada en la butaca {butaca}"):
        print("Compra cancelada.")
        return False
    
    try:
        datos_funcion = funciones[funcion_id]
        pelicula = datos_funcion["Película"]
        fila, columna = butaca  # Índices 0-based recibidos del menú
        
        
        if not validacion.validar_edad(usuario, pelicula):
            print("No tenés la edad suficiente para ver esta película.")
            return False
        
        # Marcar butaca como ocupada
        funciones[funcion_id]["Butacas"][fila][columna] = "Ocupada"
        
        # Cargar reservas existentes
        reservas = cargar_reservas()
        
        # Generar ID de reserva
        reserva_id = generar_id_reserva(reservas)
        
        # Convertir índices a 1-based para el sistema de reservas (formato admin)
        fila_1based = fila + 1
        columna_1based = columna + 1
        
        # Crear reserva en el sistema de admin
        reservas[reserva_id] = {
            "Usuario": usuario,
            "FuncionID": funcion_id,
            "Butaca": {"Fila": fila_1based, "Columna": columna_1based},
            "Precio": 0,  # Se puede agregar precio después si es necesario
            "Estado": "Activa"
        }
        
        # Guardar reservas
        guardar_reservas(reservas)
        
        # Agregar a la lista de reservas del usuario (para compatibilidad)
        usuarios[usuario]["reservas"].append({
            "pelicula": pelicula,
            "funcion_id": funcion_id,
            "butaca": f"F{fila_1based}-A{columna_1based}",
            "reserva_id": reserva_id
        })
        
        # Guardar usuarios actualizados
        guardar_usuarios()

        print(f"Entrada comprada para '{pelicula}' - Butaca F{fila_1based}-A{columna_1based} - Reserva ID: {reserva_id}")
        return True

    except Exception as e:
        print(f"Error al comprar entrada: {e}")
        return False

#Funcion para ver historial de compras
def ver_historial_compras(usuario):
    """
    Función para mostrar el historial de compras del usuario.
    """
    try:
        reservas = cargar_reservas()
        funciones = cargar_funciones()
        
        reservas_usuario = []
        for reserva_id, datos_reserva in reservas.items():
            if datos_reserva.get("Usuario") == usuario:
                funcion_id = datos_reserva.get("FuncionID", "")
                datos_funcion = funciones.get(funcion_id, {})
                
                reservas_usuario.append({
                    "reserva_id": reserva_id,
                    "funcion_id": funcion_id,
                    "pelicula": datos_funcion.get("Película", "N/A"),
                    "fecha": datos_funcion.get("Fecha", "N/A"),
                    "hora": datos_funcion.get("Hora", "N/A"),
                    "sala": datos_funcion.get("Sala", "N/A"),
                    "butaca": f"F{datos_reserva['Butaca']['Fila']}-A{datos_reserva['Butaca']['Columna']}",
                    "precio": datos_reserva.get("Precio", 0),
                    "estado": datos_reserva.get("Estado", "")
                })
        
        if not reservas_usuario:
            print(f"No hay reservas registradas para el usuario '{usuario}'.")
            return []
        
        print(f"\nHistorial de compras de '{usuario}':")
        print("=" * 80)
        for r in reservas_usuario:
            print(f"ID: {r['reserva_id']}")
            print(f"  Película: {r['pelicula']}")
            print(f"  Fecha: {r['fecha']} | Hora: {r['hora']} | Sala: {r['sala']}")
            print(f"  Butaca: {r['butaca']} | Precio: ${r['precio']} | Estado: {r['estado']}")
            print("-" * 80)
        
        return reservas_usuario
    except Exception as e:
        print(f"Error al consultar historial de compras: {e}")
        return []


#Funcion para modificar datos usuario
def modificar_datos_usuario(usuario, datos_nuevos):
    """
    Función para modificar los datos personales del usuario.
    """
    try:
        if usuario not in usuarios:
            print("El usuario no existe.")
            return None
        
        nuevo_usuario = usuario
        # Si se cambia el mail, mover los datos a la nueva clave
        if "mail" in datos_nuevos:
            nuevo_mail = datos_nuevos["mail"].strip()
            if nuevo_mail and nuevo_mail != usuario:
                usuarios[nuevo_mail] = usuarios.pop(usuario)
                usuario = nuevo_usuario = nuevo_mail
        
        if datos_nuevos:
            usuarios[usuario].update(datos_nuevos)
            print("Datos modificados de manera exitosa")
        
        guardar_usuarios()
        return nuevo_usuario
        
    except Exception as e:
        print(f"Error al modificar los datos: {e}")
        return None


#Funcion para borrar la cuenta
def borrar_cuenta(usuario):
    """
    Función para eliminar la cuenta de un usuario del sistema.
    """
    try:
        if usuario not in usuarios:
            print("El usuario no existe.")
            return False
        del usuarios[usuario]
        guardar_usuarios()
        print(f"Cuenta de '{usuario}' eliminada correctamente.")
        return True
    except Exception as e:
        print(f"Error al borrar cuenta: {e}")
        return False


#Funcion para buscar peliculas por filtros
def buscar_peliculas(filtros):
    """
    Función para buscar películas aplicando filtros opcionales.
    """
    try:
        peliculas_disponibles = cargar_peliculas()
        genero = filtros.get("genero")
        max_duracion = filtros.get("max_duracion")

        resultado = [
            p for p in peliculas_disponibles
            if (not genero or p["genero"].lower() == genero.lower())
            and (not max_duracion or p["duracion"] <= max_duracion)
        ]

        resultado = sorted(resultado, key=lambda x: x["titulo"])

        if not resultado:
            print("No se encontraron películas con esos filtros.")
        else:
            print("\nPelículas encontradas:")
            for p in resultado:
                print(f"- {p['titulo']} ({p['genero']}, {p['duracion']} min)")
        return resultado
    except Exception as e:
        print(f"Error al buscar películas: {e}")
        return []


#Funcion para generar comprobante
def generar_comprobante(compra):
    """
    Función para generar un comprobante en formato .txt de una compra.
    """
    try:
        nombre_archivo = f"comprobante_{compra['pelicula']}.txt"
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            json.dump(compra, archivo, indent=4, ensure_ascii=False)
        print(f"Comprobante generado: {nombre_archivo}")
        return True
    except Exception as e:
        print(f"Error al generar comprobante: {e}")
        return False


#Funcion para cargar funciones
def cargar_funciones():
    """
    Función para cargar desde archivo las funciones de cine.
    """
    try:
        with open("funciones.txt", "r", encoding="utf-8") as f:
            funciones = json.load(f)
        return funciones
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Error al cargar funciones: {e}")
        return {}

#Funcion para guardar funciones
def guardar_funciones(funciones):
    """
    Función para guardar en archivo las funciones de cine.
    """
    try:
        with open("funciones.txt", "w", encoding="utf-8") as f:
            json.dump(funciones, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar funciones: {e}")
        return False

#Funcion para cargar usuarios
def cargar_usuarios():
    """
    Función para cargar usuarios desde archivo y sincronizar sus reservas.
    """
    global usuarios
    try:
        with open("usuarios.txt", "r", encoding="utf-8") as f:
            usuarios = json.load(f)
        
        # Sincronizar reservas del usuario con el sistema de reservas de admin
        reservas = cargar_reservas()
        for usuario_nombre in usuarios:
            # Limpiar reservas antiguas y reconstruir desde el sistema de admin
            usuarios[usuario_nombre]["reservas"] = []
            for reserva_id, datos_reserva in reservas.items():
                if datos_reserva.get("Usuario") == usuario_nombre:
                    funcion_id = datos_reserva.get("FuncionID", "")
                    butaca = datos_reserva.get("Butaca", {})
                    usuarios[usuario_nombre]["reservas"].append({
                        "funcion_id": funcion_id,
                        "butaca": f"F{butaca.get('Fila', 0)}-A{butaca.get('Columna', 0)}",
                        "reserva_id": reserva_id
                    })
        
        return True
    except FileNotFoundError:
        usuarios = {}
        return True
    except Exception as e:
        print(f"Error al cargar usuarios: {e}")
        usuarios = {}
        return False

#Funcion para guardar usuarios
def guardar_usuarios():
    """
    Función para guardar los datos de usuarios en archivo.
    """
    try:
        with open("usuarios.txt", "w", encoding="utf-8") as f:
            json.dump(usuarios, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar usuarios: {e}")
        return False

#Funcion para cargar peliculas
def cargar_peliculas():
    """
    Función para cargar películas desde archivo en formato de usuario.
    """
    try:
        with open("peliculas.txt", "r", encoding="utf-8") as f:
            peliculas_admin = json.load(f)
        
        # Convertir formato admin a formato usuario
        peliculas_disponibles = []
        for titulo, datos in peliculas_admin.items():
            peliculas_disponibles.append({
                "titulo": titulo,
                "genero": datos.get("Género", ""),
                "duracion": datos.get("Duración", 0)
            })
        
        return peliculas_disponibles
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error al cargar películas: {e}")
        return []

#Funcion para cargar reservas
def cargar_reservas():
    """
    Función para cargar todas las reservas registradas desde archivo.
    """
    try:
        with open("reservas.txt", "r", encoding="utf-8") as f:
            reservas = json.load(f)
        return reservas
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Error al cargar reservas: {e}")
        return {}

#Funcion para guardar reservas
def guardar_reservas(reservas):
    """
    Función para guardar las reservas actualizadas en archivo.
    """
    try:
        with open("reservas.txt", "w", encoding="utf-8") as f:
            json.dump(reservas, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar reservas: {e}")
        return False

#Funcion para generar id de reserva
def generar_id_reserva(reservas):
    """
    Función para generar un ID único para cada nueva reserva.
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
    
    
#Main usuario
def mainUsuario(usuario_actual):
    """
    Función para mostrar el menú principal del usuario y gestionar todas sus opciones.
    """
    funciones = cargar_funciones()  # Cargar funciones al inicio

    while True:
        # Recargar funciones antes de mostrar opciones (por si se actualizaron)
        funciones = cargar_funciones()
        
        clear()
        print("\n" + "="*50)
        print("    MENÚ USUARIO")
        print("="*50)
        print("1. Ver cartelera")
        print("2. Ver horarios de película")
        print("3. Funciones disponibles")
        print("4. Consultar butacas")
        print("5. Comprar entrada")
        print("6. Consultar mis reservas / Historial de compras")
        print("7. Buscar películas por filtros")
        print("8. Ver/Modificar datos personales")
        print("9. Borrar cuenta")
        print("0. Cerrar sesión")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            ver_cartelera()
            pausar()
        
        elif opcion == "2":
            pelicula = input("Ingrese el título de la película: ")
            fecha = input("Ingrese la fecha (DD-MM-YY) o presione \"Enter\" para ver todos los horarios: ")
            fecha = fecha if fecha.strip() else None
            ver_horarios_pelicula(pelicula, fecha, funciones)
            pausar()

        elif opcion == "3":
            fecha = input("Ingrese la fecha (DD-MM-YY): ")
            coincidencias = []
            if fecha.strip():
                for fid, datos in funciones.items():
                    if datos.get("Fecha") == fecha.strip():
                        coincidencias.append((datos.get("Película", ""), datos.get("Hora", ""), datos.get("Sala", ""), fid))
                if not coincidencias:
                    print(f"No hay funciones disponibles el {fecha.strip()}.")
                else:
                    coincidencias.sort(key=lambda x: (x[0], x[1], x[2]))
                    print(f"\nFunciones disponibles el {fecha.strip()}:")
                    pelicula_actual = None
                    for pelicula, hora, sala, fid in coincidencias:
                        if pelicula != pelicula_actual:
                            print(f"\n{pelicula}:")
                            pelicula_actual = pelicula
                        print(f"- Hora {hora} | Sala {sala} | ID: {fid}")
                    while True:
                        print("\nOpciones:")
                        print("1. Comprar entrada")
                        print("2. Volver al menú")
                        opcion_funciones = input("Seleccione una opción: ")
                        if opcion_funciones == "1":
                            pelicula_compra = input("Ingrese el título de la película: ")
                            fecha_compra = fecha.strip()
                            coincidencias_compra = []
                            if pelicula_compra.strip():
                                for fid, datos in funciones.items():
                                    if str(datos.get("Película", "")).strip().lower() == pelicula_compra.strip().lower() and datos.get("Fecha") == fecha_compra:
                                        coincidencias_compra.append((datos.get("Hora", ""), datos.get("Sala", ""), fid))
                            if not coincidencias_compra:
                                print("No se encontraron funciones para esa película en la fecha indicada.")
                            else:
                                coincidencias_compra.sort(key=lambda x: (x[0], x[1]))
                                print("\nFunciones encontradas:")
                                for idx, (hora, sala, fid) in enumerate(coincidencias_compra, 1):
                                    print(f"{idx}. Hora {hora} | Sala {sala} | ID {fid}")
                                seleccion = int(input("Seleccione una función (número): "))
                                if 1 <= seleccion <= len(coincidencias_compra):
                                    funcion_id = coincidencias_compra[seleccion - 1][2]
                                    resultado_consulta = consultar_butacas(funcion_id, funciones)
                                    if resultado_consulta:
                                        fila = int(input("Fila (número): ")) - 1
                                        columna = int(input("Columna (número): ")) - 1
                                        if comprar_entrada(usuario_actual, funcion_id, (fila, columna), funciones):
                                            guardar_funciones(funciones)
                            break
                        elif opcion_funciones == "2":
                            break
                        else:
                            print("Opción no válida.")
            else:
                print("Debe ingresar una fecha.")
            pausar()

        elif opcion == "4":
            pelicula = input("Ingrese el título de la película: ")
            fecha = input("Ingrese la fecha (DD-MM-YY): ")
            coincidencias = []
            if pelicula.strip() and fecha.strip():
                for fid, datos in funciones.items():
                    if str(datos.get("Película", "")).strip().lower() == pelicula.strip().lower() and datos.get("Fecha") == fecha.strip():
                        coincidencias.append((datos.get("Hora", ""), datos.get("Sala", ""), fid))
            if not coincidencias:
                print("No se encontraron funciones para esa película en la fecha indicada.")
            else:
                coincidencias.sort(key=lambda x: (x[0], x[1]))
                print("\nFunciones encontradas:")
                for idx, (hora, sala, fid) in enumerate(coincidencias, 1):
                    print(f"{idx}. Hora {hora} | Sala {sala} | ID {fid}")
                seleccion = int(input("Seleccione una función (número): "))
                if 1 <= seleccion <= len(coincidencias):
                    funcion_id = coincidencias[seleccion - 1][2]
                    resultado_consulta = consultar_butacas(funcion_id, funciones)
                    if resultado_consulta:
                        sub_menu_activo = True
                        while sub_menu_activo:
                            print("\nOpciones disponibles:")
                            print("1. Comprar entrada")
                            print("2. Volver al menú principal")
                            eleccion = input("Seleccione una opción: ")
                            if eleccion == "1":
                                fila = int(input("Fila (número): ")) - 1
                                columna = int(input("Columna (número): ")) - 1
                                if comprar_entrada(usuario_actual, funcion_id, (fila, columna), funciones):
                                    guardar_funciones(funciones)
                                sub_menu_activo = False
                            elif eleccion == "2":
                                sub_menu_activo = False
                            else:
                                print("Opción no válida. Intente nuevamente.")
            pausar()

        elif opcion == "5":
            pelicula = input("Ingrese el título de la película: ")
            fecha = input("Ingrese la fecha (DD-MM-YY): ")
            coincidencias = []
            if pelicula.strip() and fecha.strip():
                for fid, datos in funciones.items():
                    if str(datos.get("Película", "")).strip().lower() == pelicula.strip().lower() and datos.get("Fecha") == fecha.strip():
                        coincidencias.append((datos.get("Hora", ""), datos.get("Sala", ""), fid))
            if not coincidencias:
                print("No se encontraron funciones para esa película en la fecha indicada.")
            else:
                coincidencias.sort(key=lambda x: (x[0], x[1]))
                print("\nFunciones encontradas:")
                for idx, (hora, sala, fid) in enumerate(coincidencias, 1):
                    print(f"{idx}. Hora {hora} | Sala {sala} | ID {fid}")
                seleccion = int(input("Seleccione una función (número): "))
                if 1 <= seleccion <= len(coincidencias):
                    funcion_id = coincidencias[seleccion - 1][2]
                    resultado_consulta = consultar_butacas(funcion_id, funciones)
                    if resultado_consulta:
                        fila = int(input("Fila (número): ")) - 1
                        columna = int(input("Columna (número): ")) - 1
                        if comprar_entrada(usuario_actual, funcion_id, (fila, columna), funciones):
                            guardar_funciones(funciones)  # Guardar cambios después de comprar
            pausar()

        elif opcion == "6":
            ver_historial_compras(usuario_actual)
            pausar()

        elif opcion == "7":
            genero = input("Género (Enter para omitir): ")
            max_duracion = input("Duración máxima en minutos (Enter para omitir): ")
            filtros = {}
            if genero.strip():
                filtros["genero"] = genero.strip()
            if max_duracion.strip():
                try:
                    filtros["max_duracion"] = int(max_duracion.strip())
                except ValueError:
                    print("Duración inválida. Se omitirá este filtro.")
            buscar_peliculas(filtros)
            pausar()

        elif opcion == "8":
            while True:
                clear()
                datos_actuales = usuarios.get(usuario_actual, {})
                print("\nDatos personales actuales:")
                print(f"Mail: {usuario_actual}")
                print(f"Nombre: {datos_actuales.get('nombre', '')}")
                print(f"Apellido: {datos_actuales.get('apellido', '')}")
                print(f"Contraseña: {datos_actuales.get('contraseña', '')}")
                print("\nOpciones:")
                print("1. Modificar datos personales")
                print("2. Volver al menú")
                opcion_datos = input("Seleccione una opción: ")
                if opcion_datos == "1":
                    print("Modificar datos personales (dejar en blanco para no cambiar):")
                    nuevo_mail = input("Nuevo mail: ")
                    nuevo_nombre = input("Nuevo nombre: ")
                    nuevo_apellido = input("Nuevo apellido: ")
                    nueva_contrasenia = input("Nueva contraseña: ")
                    datos_nuevos = {}
                    if nuevo_mail.strip():
                        datos_nuevos["mail"] = nuevo_mail.strip()
                    if nuevo_nombre.strip():
                        datos_nuevos["nombre"] = nuevo_nombre.strip()
                    if nuevo_apellido.strip():
                        datos_nuevos["apellido"] = nuevo_apellido.strip()
                    if nueva_contrasenia.strip():
                        datos_nuevos["contraseña"] = nueva_contrasenia.strip()
                    if datos_nuevos:
                        nuevo_identificador = modificar_datos_usuario(usuario_actual, datos_nuevos)
                        if nuevo_identificador:
                            usuario_actual = nuevo_identificador
                    else:
                        print("No se ingresaron cambios.")
                        pausar()
                elif opcion_datos == "2":
                    break
                else:
                    print("Opción no válida.")
                    pausar()

        elif opcion == "9":
            if validacion.confirmar_accion("borrar su cuenta"):
                borrar_cuenta(usuario_actual)
                print("Cuenta eliminada. Saliendo del sistema...")
                return True  # Indica que se debe terminar la ejecución
            else:
                print("Operación cancelada.")

        elif opcion == "0":
            print("Sesión cerrada.")
            return False  # Volver al menú principal

        else:
            print("Opción no válida.")
    
    return False

#Funcion de login usuario y menu
def login_usuario_menu():
    """
    Función para manejar el menú de acceso del usuario, incluyendo registro e inicio de sesión.
    """
    cargar_usuarios()  # Cargar usuarios al inicio
    funciones = cargar_funciones()  # Cargar funciones para opciones sin login

    while True:
        clear()
        print("\n" + "="*50)
        print("    ACCESO USUARIO")
        print("="*50)
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Ver cartelera")
        print("4. Ver horarios de película")
        print("0. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            mail = input("Ingrese su mail: ")
            nombre = input("Ingrese su nombre: ")
            apellido = input("Ingrese su apellido: ")
            edad = input("Ingrese su edad: ")
            contrasenia = input("Ingrese su contraseña: ")
            registrar_usuario(mail, nombre, apellido, edad, contrasenia)
            pausar()

        elif opcion == "2":
            bandera = True
            while bandera:
                usuario = input("Mail (o -1 para volver): ")
                if usuario == "-1":
                    bandera = False
                    continue
                contrasenia = input("Contraseña: ")
                if login_usuario(usuario, contrasenia):  
                    print("Inicio de sesión exitoso.")
                    pausar()
                    terminar = mainUsuario(usuario)
                    if terminar:  # Si se borró la cuenta, terminar ejecución
                        return True
                    bandera = False
                else:
                    print("Usuario o contraseña incorrectos. Intente nuevamente o ingrese -1 para volver.")
                    pausar()

        elif opcion == "3":
            ver_cartelera()
            pausar()
        
        elif opcion == "4":
            pelicula = input("Ingrese el título de la película: ")
            fecha = input("Ingrese la fecha (DD-MM-YY) o presione \"Enter\" para ver todos los horarios: ")
            fecha = fecha if fecha.strip() else None
            ver_horarios_pelicula(pelicula, fecha, funciones)
            pausar()

        elif opcion == "0":
            break

        else:
            print("Opción no válida.")
            pausar()
    
    return False