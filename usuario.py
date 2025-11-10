import json

usuarios = {}
peliculas_disponibles = [
    {"titulo": "Gladiador", "genero": "accion", "duracion": 155},
    {"titulo": "Batman", "genero": "superheroes", "duracion": 176},
    {"titulo": "Saw", "genero": "terror", "duracion": 100},
]

#Funcion para registrar usuario
def registrar_usuario(nombre_usuario, nombre, apellido, edad, mail, contrasenia):
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
        print(f"Usuario '{nombre_usuario}' registrado correctamente.")
        return True
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return False


#Funcion para login de usuario
def login_usuario(usuario, contrasena):
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
    try:
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
    try:
        datos_funcion = funciones[funcion_id]
        pelicula = datos_funcion["Película"]
        fila, columna = butaca
        
        funciones[funcion_id]["Butacas"][fila][columna] = "Ocupada"
        usuarios[usuario]["reservas"].append({
            "pelicula": pelicula,
            "funcion_id": funcion_id,
            "butaca": f"F{fila+1}-A{columna+1}"
        })

        print(f"Entrada comprada para '{pelicula}' - Butaca F{fila+1}-A{columna+1}")
        return True

    except Exception as e:
        print(f"Error al comprar entrada: {e}")
        return False

#Funcion para ver historial de compras
def ver_historial_compras(usuario):
    pass


#Funcion para modificar datos usuario
def modificar_datos_usuario(usuario, datos_nuevos):
    try:
        if usuario not in usuarios:
            print("El usuario no existe.")
            return None
        
        nuevo_nombre_usuario = None
        
        # Si se cambia el nombre de usuario, mover los datos a la nueva clave
        if "usuario" in datos_nuevos:
            nuevo_nombre_usuario = datos_nuevos["usuario"].strip()
            if nuevo_nombre_usuario != usuario:
                # Verificar que el nuevo nombre no esté en uso
                if nuevo_nombre_usuario in usuarios:
                    print(f"El nombre de usuario '{nuevo_nombre_usuario}' ya está en uso.")
                    return None
                # Mover los datos a la nueva clave
                usuarios[nuevo_nombre_usuario] = usuarios[usuario].copy()
                del usuarios[usuario]
                usuario = nuevo_nombre_usuario  # Actualizar referencia
                print(f"Nombre de usuario cambiado a '{nuevo_nombre_usuario}'.")
                # Eliminar "usuario" de datos_nuevos para no intentar actualizarlo como campo
                del datos_nuevos["usuario"]
        
        # Actualizar los demás campos
        if datos_nuevos:
            usuarios[usuario].update(datos_nuevos)
            campos_cambiados = []
            if "mail" in datos_nuevos:
                campos_cambiados.append("mail")
            if "contraseña" in datos_nuevos:
                campos_cambiados.append("contraseña")
            if "nombre" in datos_nuevos:
                campos_cambiados.append("nombre")
            if "apellido" in datos_nuevos:
                campos_cambiados.append("apellido")
            
            if campos_cambiados:
                print(f"Datos actualizados: {', '.join(campos_cambiados)}")
        
        print(f"Datos de '{usuario}' actualizados correctamente.")
        return nuevo_nombre_usuario if nuevo_nombre_usuario else usuario
        
    except Exception as e:
        print(f"Error al modificar los datos: {e}")
        return None


#Funcion para borrar la cuenta
def borrar_cuenta(usuario):
    """
    Elimina la cuenta del usuario y sus datos asociados
    """
    try:
        if usuario not in usuarios:
            print("El usuario no existe.")
            return False
        del usuarios[usuario]
        print(f"Cuenta de '{usuario}' eliminada correctamente.")
        return True
    except Exception as e:
        print(f"Error al borrar cuenta: {e}")
        return False


#Funcion para buscar peliculas por filtros
def buscar_peliculas(filtros):
    try:
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
    try:
        archivo = f"comprobante_{compra['pelicula']}.txt"
        with open(archivo, "w", encoding="utf-8") as archivo:
            json.dump(compra, archivo, indent=4, ensure_ascii=False)
        print(f"Comprobante generado: {archivo}")
        return True
    except Exception as e:
        print(f"Error al generar comprobante: {e}")
        return False


#Funcion para cargar funciones
def cargar_funciones():
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
    try:
        with open("funciones.txt", "w", encoding="utf-8") as f:
            json.dump(funciones, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar funciones: {e}")
        return False
    
    
#Main usuario
def mainUsuario(usuario_actual):
    funciones = cargar_funciones()  # Cargar funciones al inicio

    while True:
        # Recargar funciones antes de mostrar opciones (por si se actualizaron)
        funciones = cargar_funciones()
        
        print("\n" + "="*50)
        print("    MENÚ USUARIO")
        print("="*50)
        print("1. Ver cartelera")
        print("2. Ver horarios de película")
        print("3. Consultar butacas")
        print("4. Comprar entrada")
        print("5. Consultar mis reservas / Historial de compras")
        print("6. Buscar películas por filtros")
        print("7. Modificar datos personales")
        print("8. Borrar cuenta")
        print("0. Cerrar sesión")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            ver_cartelera()
        
        elif opcion == "2":
            pelicula = input("Ingrese el título de la película: ")
            fecha = input("Ingrese la fecha (DD-MM-YY) o presione \"Enter\" para ver todos los horarios: ")
            fecha = fecha if fecha.strip() else None
            ver_horarios_pelicula(pelicula, fecha, funciones)

        elif opcion == "3":
            funcion_id = input("Ingrese el ID de la función: ")
            consultar_butacas(funcion_id, funciones)  

        elif opcion == "4":
            funcion_id = input("Ingrese el ID de la función: ")
            fila = int(input("Fila (número): ")) - 1
            columna = int(input("Columna (número): ")) - 1
            if comprar_entrada(usuario_actual, funcion_id, (fila, columna), funciones):
                guardar_funciones(funciones)  # Guardar cambios después de comprar

        elif opcion == "5":
            ver_historial_compras(usuario_actual)

        elif opcion == "6":
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

        elif opcion == "7":
            print("Modificar datos personales (dejar en blanco para no cambiar):")
            nuevo_usuario = input("Nuevo nombre de usuario: ")
            nuevo_nombre = input("Nuevo nombre: ")
            nuevo_apellido = input("Nuevo apellido: ")
            nuevo_mail = input("Nuevo mail: ")
            nueva_contrasenia = input("Nueva contraseña: ")
            datos_nuevos = {}
            if nuevo_usuario.strip():
                datos_nuevos["usuario"] = nuevo_usuario.strip()
            if nuevo_nombre.strip():
                datos_nuevos["nombre"] = nuevo_nombre.strip()
            if nuevo_apellido.strip():
                datos_nuevos["apellido"] = nuevo_apellido.strip()
            if nuevo_mail.strip():
                datos_nuevos["mail"] = nuevo_mail.strip()
            if nueva_contrasenia.strip():
                datos_nuevos["contraseña"] = nueva_contrasenia.strip()
            if datos_nuevos:
                nuevo_usuario_actual = modificar_datos_usuario(usuario_actual, datos_nuevos)
                if nuevo_usuario_actual:
                    usuario_actual = nuevo_usuario_actual  # Actualizar variable si cambió el nombre
            else:
                print("No se ingresaron cambios.")

        elif opcion == "8":
            confirmar = input("¿Está seguro de que desea borrar su cuenta? (s/n): ")
            if confirmar.lower() == "s":
                if borrar_cuenta(usuario_actual):
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
    funciones = cargar_funciones()  # Cargar funciones para opciones sin login

    while True:
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
            nombre_usuario = input("Ingrese nombre de usuario: ")
            nombre = input("Ingrese su nombre: ")
            apellido = input("Ingrese su apellido: ")
            edad = input("Ingrese su edad: ")
            mail = input("Ingrese su mail: ")
            contrasenia = input("Ingrese su contraseña: ")
            registrar_usuario(nombre_usuario, nombre, apellido, edad, mail, contrasenia)

        elif opcion == "2":
            usuario = input("Usuario: ")
            contrasenia = input("Contraseña: ")
            if login_usuario(usuario, contrasenia):  
                print("Inicio de sesión exitoso.")
                terminar = mainUsuario(usuario)
                if terminar:  # Si se borró la cuenta, terminar ejecución
                    return True
            else:
                print("Usuario o contraseña incorrectos.")

        elif opcion == "3":
            ver_cartelera()
        
        elif opcion == "4":
            pelicula = input("Ingrese el título de la película: ")
            fecha = input("Ingrese la fecha (DD-MM-YY) o presione \"Enter\" para ver todos los horarios: ")
            fecha = fecha if fecha.strip() else None
            ver_horarios_pelicula(pelicula, fecha, funciones)

        elif opcion == "0":
            break

        else:
            print("Opción no válida.")
    
    return False