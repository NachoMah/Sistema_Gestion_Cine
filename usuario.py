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

# Funciones helper para validaciones de formato (específicas del contexto)
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

def validar_seleccion_menu(valor, min_opcion, max_opcion):
    """
    Valida que la selección esté en el rango válido del menú.
    Retorna el número si es válido, None en caso contrario.
    """
    try:
        numero = int(valor.strip())
        if not (min_opcion <= numero <= max_opcion):
            print(f"ERROR: La opción debe estar entre {min_opcion} y {max_opcion}.")
            return None
        return numero
    except ValueError:
        print("ERROR: Debe ingresar un número válido.")
        return None

usuarios = {}

#Funcion para registrar usuario
def registrar_usuario(mail, nombre, apellido, edad, contrasenia):
    """
    Función para registrar un nuevo usuario en el sistema.
    """
    # Validar datos no nulos primero
    datos = [mail, nombre, apellido, edad, contrasenia]
    if not validacion.validar_datos_no_nulos(datos):
        print("ERROR: Todos los campos son obligatorios y no pueden estar vacíos.")
        return False
    
    # Validar formato de mail
    if not validacion.validar_mail(mail):
        print("ERROR: El mail debe tener un dominio válido (gmail, hotmail, outlook, yahoo, etc.).")
        return False
    
    # Validar contraseña
    if not validacion.validar_contrasena(contrasenia):
        print("ERROR: La contraseña debe tener al menos 5 caracteres.")
        return False
    
    # Normalizar email a minúsculas para evitar errores de tipeo
    mail = mail.strip().lower()
    nombre_usuario = mail
    
    # Validar que el usuario no exista (validación manual específica del contexto)
    if nombre_usuario in usuarios:
        print("El usuario ya existe")
        return False
    
    try:
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
    from validacion import validar_usuario_y_contrasena
    
    try:
        resultado = validar_usuario_y_contrasena(usuario, contrasena)
        if resultado is None:
            print("Usuario o contraseña incorrectos.")
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
            # Verificar si la película existe en el sistema
            peliculas = cargar_peliculas()
            pelicula_existe = False
            pelicula_normalizada = pelicula.strip().lower()
            titulo_original = pelicula.strip()
            
            for pelicula_data in peliculas:
                if pelicula_data.get("titulo", "").lower() == pelicula_normalizada:
                    pelicula_existe = True
                    titulo_original = pelicula_data.get("titulo", pelicula.strip())
                    break
            
            if not pelicula_existe:
                print(f"ERROR: La película '{pelicula}' no existe en el sistema.")
            else:
                # La película existe pero no tiene funciones
                if fecha:
                    print(f"No hay funciones para '{titulo_original}' el {fecha}.")
                else:
                    print(f"No hay funciones programadas para '{titulo_original}'.")
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
    try:
        # Validar que la función existe
        if funcion_id not in funciones:
            print("ERROR: La función no existe.")
            return False
        
        datos_funcion = funciones[funcion_id]
        pelicula_nombre = datos_funcion["Película"]
        
        # Validar que la película de la función aún existe en el sistema
        ruta_peliculas = os.path.join(os.path.dirname(__file__), "peliculas.txt")
        try:
            with open(ruta_peliculas, "r", encoding="utf-8") as f:
                peliculas = json.load(f)
            
            # Buscar la película (case-insensitive)
            pelicula_existe = False
            pelicula_normalizada = pelicula_nombre.strip().lower()
            for pelicula_key in peliculas.keys():
                if pelicula_key.lower() == pelicula_normalizada:
                    pelicula_existe = True
                    break
            
            if not pelicula_existe:
                print(f"ERROR: La película '{pelicula_nombre}' asociada a esta función ya no existe en el sistema.")
                print("No se puede realizar la compra para una función de una película eliminada.")
                return False
        except Exception as e:
            print(f"ERROR: No se pudo validar la existencia de la película. Error: {e}")
            return False
        
        fila, columna = butaca  # Índices 0-based recibidos del menú
        
        # Convertir a 1-based para validaciones y visualización
        fila_1based = fila + 1
        columna_1based = columna + 1
        
        # Confirmar compra con valores 1-based para mostrar correctamente
        if not validacion.confirmar_accion(f"comprar la entrada en la butaca F{fila_1based}-A{columna_1based}"):
            print("Compra cancelada.")
            return False
        
        # Validar que el usuario esté registrado
        if not validacion.verificar_usuario_registrado(usuario):
            print("ERROR: Usuario no registrado en el sistema.")
            return False
        
        # Validar que la butaca esté disponible
        if not validacion.validar_butaca_disponible(funcion_id, fila_1based, columna_1based, funciones):
            print("ERROR: La butaca seleccionada no está disponible.")
            return False
        
        # Calcular precio de la entrada
        from precios import calcular_precio_entrada, cargar_precios
        
        # Cargar precios
        cargar_precios()
        
        # Preguntar tipo de entrada
        print("\n--- Tipo de Entrada ---")
        print("1. Normal (2D)")
        print("2. 3D")
        print("3. VIP")
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
            else:
                print("ERROR: Opción no válida. Intente nuevamente.")
        
        # Preguntar si aplica promoción o entrada especial
        print("\n--- Promoción o Entrada Especial ---")
        print("1. Sin promoción/descuento")
        print("2. Entrada para niños (menores de 12 años)")
        print("3. Entrada para jubilados")
        print("4. Entrada para estudiantes")
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
            else:
                print("ERROR: Opción no válida. Intente nuevamente.")
        
        # Calcular precio automáticamente
        precio_calculado = calcular_precio_entrada(tipo_entrada, descuento)
        print(f"\n✓ Precio calculado: ${precio_calculado}")
        
        # Validar edad (si la película tiene clasificación)
        try:
            # Cargar datos de la película
            ruta_peliculas = os.path.join(os.path.dirname(__file__), "peliculas.txt")
            with open(ruta_peliculas, "r", encoding="utf-8") as f:
                peliculas = json.load(f)
            
            pelicula_datos = peliculas.get(pelicula_nombre, {})
            
            # Si la película tiene clasificación, validar edad
            if "Clasificación" in pelicula_datos or "clasificacion" in pelicula_datos:
                clasificacion = pelicula_datos.get("Clasificación") or pelicula_datos.get("clasificacion", "")
                if clasificacion:
                    usuario_datos = usuarios.get(usuario, {})
                    
                    # Verificar que el usuario tenga edad registrada
                    if "edad" not in usuario_datos:
                        print("ERROR: No se puede validar la edad. El usuario no tiene edad registrada.")
                        return False
                    
                    pelicula_con_clasificacion = {"clasificacion": clasificacion}
                    
                    if not validacion.validar_edad(usuario_datos, pelicula_con_clasificacion):
                        print("ERROR: No cumple con la edad mínima requerida para esta película.")
                        return False
        except FileNotFoundError:
            print("ERROR: No se pudo validar la edad. Archivo de películas no encontrado.")
            return False
        except json.JSONDecodeError:
            print("ERROR: No se pudo validar la edad. Error al leer el archivo de películas.")
            return False
        except Exception as e:
            # Si hay error al validar edad, bloquear la compra por seguridad
            print(f"ERROR: No se pudo validar la edad. Error: {e}")
            return False
        
        # Marcar butaca como ocupada
        funciones[funcion_id]["Butacas"][fila][columna] = "Ocupada"
        
        # Cargar reservas existentes
        reservas = cargar_reservas()
        
        # Generar ID de reserva
        reserva_id = generar_id_reserva(reservas)
        
        # Crear reserva en el sistema de admin
        reservas[reserva_id] = {
            "Usuario": usuario,
            "FuncionID": funcion_id,
            "Butaca": {"Fila": fila_1based, "Columna": columna_1based},
            "Precio": precio_calculado,  # Precio real calculado
            "Estado": "Activa"
        }
        
        # Guardar reservas
        guardar_reservas(reservas)
        
        # Agregar a la lista de reservas del usuario (para compatibilidad)
        usuarios[usuario]["reservas"].append({
            "pelicula": pelicula_nombre,
            "funcion_id": funcion_id,
            "butaca": f"F{fila_1based}-A{columna_1based}",
            "reserva_id": reserva_id,
            "precio": precio_calculado
        })
        
        # Guardar usuarios actualizados
        guardar_usuarios()

        # Generar comprobante automáticamente
        compra_comprobante = {
            "reserva_id": reserva_id,
            "usuario": usuario,
            "pelicula": pelicula_nombre,
            "fecha": datos_funcion.get("Fecha", "N/A"),
            "hora": datos_funcion.get("Hora", "N/A"),
            "sala": datos_funcion.get("Sala", "N/A"),
            "butaca": f"F{fila_1based}-A{columna_1based}",
            "tipo_entrada": tipo_entrada,
            "descuento": descuento,
            "precio": precio_calculado
        }
        generar_comprobante(compra_comprobante)

        print(f"Entrada comprada para '{pelicula_nombre}' - Butaca F{fila_1based}-A{columna_1based} - Precio: ${precio_calculado} - Reserva ID: {reserva_id}")
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
        
        # Validar datos modificados
        if "mail" in datos_nuevos and datos_nuevos["mail"]:
            nuevo_mail = datos_nuevos["mail"].strip().lower()  # Normalizar a minúsculas
            if nuevo_mail:
                # Validar formato de mail
                if not validacion.validar_mail(nuevo_mail):
                    print("ERROR: El mail debe tener un dominio válido (gmail, hotmail, outlook, yahoo, etc.).")
                    return None
                # Validar que el nuevo mail no esté en uso (búsqueda case-insensitive)
                mail_en_uso = False
                for usuario_key in usuarios.keys():
                    if usuario_key.lower() == nuevo_mail and usuario_key.lower() != usuario.lower():
                        mail_en_uso = True
                        break
                if mail_en_uso:
                    print("ERROR: El mail ingresado ya está en uso por otro usuario.")
                    return None
        
        if "contraseña" in datos_nuevos and datos_nuevos["contraseña"]:
            nueva_contrasenia = datos_nuevos["contraseña"].strip()
            if nueva_contrasenia:
                # Validar contraseña
                if not validacion.validar_contrasena(nueva_contrasenia):
                    print("ERROR: La contraseña debe tener al menos 5 caracteres.")
                    return None
        
        # Validar que los datos no sean nulos/vacíos
        datos_a_validar = [v for v in datos_nuevos.values() if v]  # Solo los que tienen valor
        if datos_a_validar and not validacion.validar_datos_no_nulos(datos_a_validar):
            print("ERROR: Los campos no pueden estar vacíos.")
            return None
        
        nuevo_usuario = usuario
        # Si se cambia el mail, mover los datos a la nueva clave
        if "mail" in datos_nuevos:
            nuevo_mail = datos_nuevos["mail"].strip().lower()  # Normalizar a minúsculas
            if nuevo_mail and nuevo_mail.lower() != usuario.lower():
                # Actualizar referencias en reservas si es necesario
                reservas = cargar_reservas()
                for reserva_id, datos_reserva in reservas.items():
                    if datos_reserva.get("Usuario") == usuario:
                        datos_reserva["Usuario"] = nuevo_mail
                guardar_reservas(reservas)
                
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
        # Usar ruta absoluta para guardar en la carpeta TPO
        ruta_comprobante = os.path.join(os.path.dirname(__file__), f"comprobante_{compra['reserva_id']}.txt")
        
        with open(ruta_comprobante, "w", encoding="utf-8") as archivo:
            archivo.write("=" * 50 + "\n")
            archivo.write("        COMPROBANTE DE COMPRA\n")
            archivo.write("=" * 50 + "\n\n")
            archivo.write(f"ID de Reserva: {compra['reserva_id']}\n")
            archivo.write(f"Usuario: {compra['usuario']}\n")
            archivo.write(f"Película: {compra['pelicula']}\n")
            archivo.write(f"Fecha: {compra['fecha']}\n")
            archivo.write(f"Hora: {compra['hora']}\n")
            archivo.write(f"Sala: {compra['sala']}\n")
            archivo.write(f"Butaca: {compra['butaca']}\n")
            archivo.write(f"Tipo de Entrada: {compra.get('tipo_entrada', 'Normal')}\n")
            if compra.get('descuento'):
                archivo.write(f"Descuento Aplicado: {compra['descuento']}\n")
            archivo.write(f"Precio: ${compra['precio']}\n")
            archivo.write("\n" + "=" * 50 + "\n")
            archivo.write("        ¡Gracias por su compra!\n")
            archivo.write("=" * 50 + "\n")
        
        print(f"✓ Comprobante generado: comprobante_{compra['reserva_id']}.txt")
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
        # Usar ruta absoluta para consistencia
        ruta_funciones = os.path.join(os.path.dirname(__file__), "funciones.txt")
        with open(ruta_funciones, "r", encoding="utf-8") as f:
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
        # Usar ruta absoluta para consistencia
        ruta_funciones = os.path.join(os.path.dirname(__file__), "funciones.txt")
        with open(ruta_funciones, "w", encoding="utf-8") as f:
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
        # Usar la misma ruta que validacion.py para consistencia
        ruta_usuarios = os.path.join(os.path.dirname(__file__), "usuarios.txt")
        with open(ruta_usuarios, "r", encoding="utf-8") as f:
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
        # Usar la misma ruta que validacion.py para consistencia
        ruta_usuarios = os.path.join(os.path.dirname(__file__), "usuarios.txt")
        with open(ruta_usuarios, "w", encoding="utf-8") as f:
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
        # Usar ruta absoluta para consistencia
        ruta_peliculas = os.path.join(os.path.dirname(__file__), "peliculas.txt")
        with open(ruta_peliculas, "r", encoding="utf-8") as f:
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
        # Usar ruta absoluta para consistencia
        ruta_reservas = os.path.join(os.path.dirname(__file__), "reservas.txt")
        with open(ruta_reservas, "r", encoding="utf-8") as f:
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
        # Usar ruta absoluta para consistencia
        ruta_reservas = os.path.join(os.path.dirname(__file__), "reservas.txt")
        with open(ruta_reservas, "w", encoding="utf-8") as f:
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
            # Validar nombre de película inmediatamente después del Enter
            bandera = True
            while bandera:
                pelicula = input("Ingrese el título de la película: ").strip()
                if not pelicula:
                    print("ERROR: El título de la película no puede estar vacío.")
                    continue
                
                # Cargar películas para validar existencia
                peliculas = cargar_peliculas()
                pelicula_existe = False
                pelicula_normalizada = pelicula.lower()
                
                # Verificar si la película existe (búsqueda case-insensitive)
                for pelicula_data in peliculas:
                    if pelicula_data.get("titulo", "").lower() == pelicula_normalizada:
                        pelicula_existe = True
                        # Usar el título original de la película
                        pelicula = pelicula_data.get("titulo", pelicula)
                        break
                
                if not pelicula_existe:
                    print(f"ERROR: La película '{pelicula}' no existe en el sistema.")
                    print("\nOpciones:")
                    print("1. Intentar con otra película")
                    print("-1. Volver al menú")
                    opcion_error = input("Seleccione una opción: ").strip()
                    if opcion_error == "-1":
                        bandera = False
                        continue
                    elif opcion_error == "1":
                        continue  # Volver a pedir película
                    else:
                        print("Opción no válida. Volviendo al menú.")
                        bandera = False
                        continue
                else:
                    bandera = False
            
            # Solo pedir fecha si la película existe
            fecha = input("Ingrese la fecha (DD-MM-YY) o presione \"Enter\" para ver todos los horarios: ")
            fecha = fecha if fecha.strip() else None
            ver_horarios_pelicula(pelicula, fecha, funciones)
            pausar()

        elif opcion == "3":
            # Validar fecha con opción de reintentar
            from admin import validar_formato_fecha
            bandera_fecha = True
            while bandera_fecha:
                bandera = True
                fecha = None
                while bandera:
                    fecha_str = input("Ingrese la fecha (DD-MM-YY): ").strip()
                    if not fecha_str:
                        print("ERROR: La fecha no puede estar vacía.")
                        continue
                    if not validar_formato_fecha(fecha_str):
                        print("ERROR: La fecha debe tener formato DD-MM-YY (ej: 15-11-25).")
                        continue
                    fecha = fecha_str
                    bandera = False
                
                coincidencias = []
                for fid, datos in funciones.items():
                    if datos.get("Fecha") == fecha:
                        coincidencias.append((datos.get("Película", ""), datos.get("Hora", ""), datos.get("Sala", ""), fid))
                
                if not coincidencias:
                    print(f"No hay funciones disponibles el {fecha}.")
                    print("\nOpciones:")
                    print("1. Intentar con otra fecha")
                    print("-1. Volver al menú")
                    opcion_error = input("Seleccione una opción: ").strip()
                    if opcion_error == "-1":
                        bandera_fecha = False
                        break
                    elif opcion_error == "1":
                        continue  # Volver a pedir fecha
                    else:
                        print("ERROR: Opción no válida. Intente nuevamente.")
                        continue  # Volver a mostrar opciones
                else:
                    bandera_fecha = False
            
            # Si se encontraron coincidencias, mostrarlas
            if coincidencias:
                coincidencias.sort(key=lambda x: (x[0], x[1], x[2]))
                print(f"\nFunciones disponibles el {fecha}:")
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
                                print("\nOpciones:")
                                print("1. Intentar con otra película")
                                print("-1. Volver al menú")
                                opcion_error = input("Seleccione una opción: ").strip()
                                if opcion_error == "-1":
                                    break
                                elif opcion_error == "1":
                                    continue  # Volver a pedir película
                                else:
                                    print("Opción no válida. Volviendo al menú.")
                                    break
                            else:
                                coincidencias_compra.sort(key=lambda x: (x[0], x[1]))
                                print("\nFunciones encontradas:")
                                for idx, (hora, sala, fid) in enumerate(coincidencias_compra, 1):
                                    print(f"{idx}. Hora {hora} | Sala {sala} | ID {fid}")
                                bandera = True
                                while bandera:
                                    seleccion_str = input("Seleccione una función (número): ").strip()
                                    seleccion = validar_seleccion_menu(seleccion_str, 1, len(coincidencias_compra))
                                    if seleccion is None:
                                        continue
                                    bandera = False
                                
                                funcion_id = coincidencias_compra[seleccion - 1][2]
                                resultado_consulta = consultar_butacas(funcion_id, funciones)
                                if resultado_consulta:
                                    # Validar fila
                                    bandera = True
                                    while bandera:
                                        fila_str = input("Fila (número): ").strip()
                                        fila = validar_numero_positivo(fila_str, "La fila debe ser un número positivo.")
                                        if fila is None:
                                            continue
                                        bandera = False
                                    
                                    # Validar columna
                                    bandera = True
                                    while bandera:
                                        columna_str = input("Columna (número): ").strip()
                                        columna = validar_numero_positivo(columna_str, "La columna debe ser un número positivo.")
                                        if columna is None:
                                            continue
                                        bandera = False
                                    
                                    # Convertir a 0-based para la función
                                    resultado_compra = comprar_entrada(usuario_actual, funcion_id, (fila - 1, columna - 1), funciones)
                                    if resultado_compra:
                                        guardar_funciones(funciones)
                                    else:
                                        print("\nOpciones:")
                                        print("1. Intentar con otra butaca")
                                        print("-1. Volver al menú")
                                        opcion_error = input("Seleccione una opción: ").strip()
                                        if opcion_error == "-1":
                                            break
                                        elif opcion_error == "1":
                                            continue  # Volver a pedir fila y columna
                                        else:
                                            print("Opción no válida. Volviendo al menú.")
                                            break
                            break
                        elif opcion_funciones == "2":
                            break
                        else:
                            print("Opción no válida.")
            pausar()

        elif opcion == "4":
            # Validar película
            bandera = True
            pelicula = None
            while bandera:
                pelicula = input("Ingrese el título de la película: ").strip()
                if not pelicula:
                    print("ERROR: El título de la película no puede estar vacío.")
                    continue
                # Verificar si la película existe
                peliculas = cargar_peliculas()
                pelicula_existe = False
                pelicula_normalizada = pelicula.lower()
                for pelicula_data in peliculas:
                    if pelicula_data.get("titulo", "").lower() == pelicula_normalizada:
                        pelicula_existe = True
                        pelicula = pelicula_data.get("titulo", pelicula)
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
                        print("Opción no válida. Volviendo al menú.")
                        bandera = False
                        break
                else:
                    bandera = False
            
            if pelicula is None:
                pausar()
                continue
            
            # Validar fecha
            from admin import validar_formato_fecha
            bandera = True
            fecha = None
            while bandera:
                fecha_str = input("Ingrese la fecha (DD-MM-YY): ").strip()
                if not fecha_str:
                    print("ERROR: La fecha no puede estar vacía.")
                    continue
                if not validar_formato_fecha(fecha_str):
                    print("ERROR: La fecha debe tener formato DD-MM-YY (ej: 15-11-25).")
                    continue
                fecha = fecha_str
                bandera = False
            
            coincidencias = []
            if pelicula and fecha:
                for fid, datos in funciones.items():
                    if str(datos.get("Película", "")).strip().lower() == pelicula.strip().lower() and datos.get("Fecha") == fecha:
                        coincidencias.append((datos.get("Hora", ""), datos.get("Sala", ""), fid))
            
            if not coincidencias:
                print("No se encontraron funciones para esa película en la fecha indicada.")
                print("\nOpciones:")
                print("1. Intentar con otra película/fecha")
                print("-1. Volver al menú")
                opcion_error = input("Seleccione una opción: ").strip()
                if opcion_error == "-1":
                    pausar()
                    continue
                elif opcion_error == "1":
                    continue  # Volver al inicio de la opción 4
                else:
                    print("ERROR: Opción no válida. Volviendo al menú.")
                    pausar()
                    continue
            else:
                coincidencias.sort(key=lambda x: (x[0], x[1]))
                print("\nFunciones encontradas:")
                for idx, (hora, sala, fid) in enumerate(coincidencias, 1):
                    print(f"{idx}. Hora {hora} | Sala {sala} | ID {fid}")
                bandera_seleccion = True
                seleccion = None
                while bandera_seleccion:
                    seleccion_str = input("Seleccione una función (número): ").strip()
                    seleccion = validar_seleccion_menu(seleccion_str, 1, len(coincidencias))
                    if seleccion is None:
                        print("ERROR: Debe seleccionar un número válido de la lista.")
                        continue
                    bandera_seleccion = False
                
                funcion_id = coincidencias[seleccion - 1][2]
                resultado_consulta = consultar_butacas(funcion_id, funciones)
                if resultado_consulta:
                    # Obtener dimensiones de la matriz de butacas
                    butacas = funciones[funcion_id]["Butacas"]
                    max_filas = len(butacas)
                    max_columnas = len(butacas[0]) if butacas else 0
                    
                    sub_menu_activo = True
                    while sub_menu_activo:
                        print("\nOpciones disponibles:")
                        print("1. Comprar entrada")
                        print("2. Volver al menú principal")
                        eleccion = input("Seleccione una opción: ").strip()
                        if eleccion == "1":
                            # Validar fila con rango de matriz
                            bandera = True
                            while bandera:
                                fila_str = input(f"Fila (número entre 1 y {max_filas}): ").strip()
                                fila = validar_numero_positivo(fila_str, "La fila debe ser un número positivo.")
                                if fila is None:
                                    continue
                                if fila < 1 or fila > max_filas:
                                    print(f"ERROR: La fila debe estar entre 1 y {max_filas}.")
                                    continue
                                bandera = False
                            
                            # Validar columna con rango de matriz
                            bandera = True
                            while bandera:
                                columna_str = input(f"Columna (número entre 1 y {max_columnas}): ").strip()
                                columna = validar_numero_positivo(columna_str, "La columna debe ser un número positivo.")
                                if columna is None:
                                    continue
                                if columna < 1 or columna > max_columnas:
                                    print(f"ERROR: La columna debe estar entre 1 y {max_columnas}.")
                                    continue
                                bandera = False
                            
                            # Convertir a 0-based para la función
                            if comprar_entrada(usuario_actual, funcion_id, (fila - 1, columna - 1), funciones):
                                guardar_funciones(funciones)
                            sub_menu_activo = False
                        elif eleccion == "2":
                            sub_menu_activo = False
                        else:
                            print("ERROR: Opción no válida. Intente nuevamente.")
            pausar()

        elif opcion == "5":
            # Validar película
            bandera = True
            pelicula = None
            while bandera:
                pelicula = input("Ingrese el título de la película: ").strip()
                if not pelicula:
                    print("ERROR: El título de la película no puede estar vacío.")
                    continue
                # Verificar si la película existe
                peliculas = cargar_peliculas()
                pelicula_existe = False
                pelicula_normalizada = pelicula.lower()
                for pelicula_data in peliculas:
                    if pelicula_data.get("titulo", "").lower() == pelicula_normalizada:
                        pelicula_existe = True
                        pelicula = pelicula_data.get("titulo", pelicula)
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
                        print("Opción no válida. Volviendo al menú.")
                        bandera = False
                        break
                else:
                    bandera = False
            
            if pelicula is None:
                pausar()
                continue
            
            # Validar fecha
            from admin import validar_formato_fecha
            bandera = True
            fecha = None
            while bandera:
                fecha_str = input("Ingrese la fecha (DD-MM-YY): ").strip()
                if not fecha_str:
                    print("ERROR: La fecha no puede estar vacía.")
                    continue
                if not validar_formato_fecha(fecha_str):
                    print("ERROR: La fecha debe tener formato DD-MM-YY (ej: 15-11-25).")
                    continue
                fecha = fecha_str
                bandera = False
            
            coincidencias = []
            if pelicula and fecha:
                for fid, datos in funciones.items():
                    if str(datos.get("Película", "")).strip().lower() == pelicula.strip().lower() and datos.get("Fecha") == fecha:
                        coincidencias.append((datos.get("Hora", ""), datos.get("Sala", ""), fid))
            
            if not coincidencias:
                print("No se encontraron funciones para esa película en la fecha indicada.")
                print("\nOpciones:")
                print("1. Intentar con otra película/fecha")
                print("-1. Volver al menú")
                opcion_error = input("Seleccione una opción: ").strip()
                if opcion_error == "-1":
                    pausar()
                    continue
                elif opcion_error == "1":
                    continue  # Volver al inicio de la opción 5
                else:
                    print("ERROR: Opción no válida. Volviendo al menú.")
                    pausar()
                    continue
            else:
                coincidencias.sort(key=lambda x: (x[0], x[1]))
                print("\nFunciones encontradas:")
                for idx, (hora, sala, fid) in enumerate(coincidencias, 1):
                    print(f"{idx}. Hora {hora} | Sala {sala} | ID {fid}")
                bandera = True
                while bandera:
                    seleccion_str = input("Seleccione una función (número): ").strip()
                    seleccion = validar_seleccion_menu(seleccion_str, 1, len(coincidencias))
                    if seleccion is None:
                        continue
                    bandera = False
                
                funcion_id = coincidencias[seleccion - 1][2]
                resultado_consulta = consultar_butacas(funcion_id, funciones)
                if resultado_consulta:
                    # Validar fila
                    bandera = True
                    while bandera:
                        fila_str = input("Fila (número): ").strip()
                        fila = validar_numero_positivo(fila_str, "La fila debe ser un número positivo.")
                        if fila is None:
                            continue
                        bandera = False
                    
                    # Validar columna
                    bandera = True
                    while bandera:
                        columna_str = input("Columna (número): ").strip()
                        columna = validar_numero_positivo(columna_str, "La columna debe ser un número positivo.")
                        if columna is None:
                            continue
                        bandera = False
                    
                    # Convertir a 0-based para la función
                    resultado_compra = comprar_entrada(usuario_actual, funcion_id, (fila - 1, columna - 1), funciones)
                    if resultado_compra:
                        guardar_funciones(funciones)  # Guardar cambios después de comprar
                    else:
                        print("\nOpciones:")
                        print("1. Intentar con otra butaca")
                        print("-1. Volver al menú")
                        opcion_error = input("Seleccione una opción: ").strip()
                        if opcion_error == "-1":
                            pass  # Continuar al pausar() y volver al menú
                        elif opcion_error == "1":
                            # Volver a pedir fila y columna
                            bandera_fila = True
                            while bandera_fila:
                                fila_str = input("Fila (número): ").strip()
                                fila = validar_numero_positivo(fila_str, "La fila debe ser un número positivo.")
                                if fila is None:
                                    continue
                                bandera_fila = False
                            
                            bandera_col = True
                            while bandera_col:
                                columna_str = input("Columna (número): ").strip()
                                columna = validar_numero_positivo(columna_str, "La columna debe ser un número positivo.")
                                if columna is None:
                                    continue
                                bandera_col = False
                            
                            # Intentar comprar de nuevo
                            resultado_compra = comprar_entrada(usuario_actual, funcion_id, (fila - 1, columna - 1), funciones)
                            if resultado_compra:
                                guardar_funciones(funciones)
                        else:
                            print("Opción no válida. Volviendo al menú.")
            pausar()

        elif opcion == "6":
            ver_historial_compras(usuario_actual)
            pausar()

        elif opcion == "7":
            # Validar género (opcional)
            genero = None
            bandera = True
            while bandera:
                genero_str = input("Género (Enter para omitir): ").strip()
                if not genero_str:
                    # Si está vacío, omitir el filtro
                    bandera = False
                    break
                # Validar que solo contenga letras
                if not validacion.validar_solo_letras(genero_str):
                    print("ERROR: El género solo puede contener letras, espacios y guiones. No se permiten números.")
                    continue
                genero = genero_str
                bandera = False
            
            # Validar duración máxima (opcional)
            max_duracion = None
            bandera = True
            while bandera:
                max_duracion_str = input("Duración máxima en minutos (Enter para omitir): ").strip()
                if not max_duracion_str:
                    # Si está vacío, omitir el filtro
                    bandera = False
                    break
                # Validar que sea un número positivo
                max_duracion = validar_numero_positivo(max_duracion_str, "La duración máxima debe ser un número positivo.")
                if max_duracion is None:
                    continue
                bandera = False
            
            # Construir filtros
            filtros = {}
            if genero:
                filtros["genero"] = genero
            if max_duracion:
                filtros["max_duracion"] = max_duracion
            
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
                        datos_nuevos["mail"] = nuevo_mail.strip().lower()  # Normalizar a minúsculas
                    if nuevo_nombre.strip():
                        if not validacion.validar_solo_letras(nuevo_nombre.strip()):
                            print("ERROR: El nombre solo puede contener letras, espacios y guiones. No se permiten números.")
                            pausar()
                            continue
                        datos_nuevos["nombre"] = nuevo_nombre.strip()
                    if nuevo_apellido.strip():
                        if not validacion.validar_solo_letras(nuevo_apellido.strip()):
                            print("ERROR: El apellido solo puede contener letras, espacios y guiones. No se permiten números.")
                            pausar()
                            continue
                        datos_nuevos["apellido"] = nuevo_apellido.strip()
                    if nueva_contrasenia.strip():
                        datos_nuevos["contraseña"] = nueva_contrasenia.strip()
                    if datos_nuevos:
                        # Mostrar resumen de cambios
                        cambios_texto = ", ".join([f"{k}: {v}" for k, v in datos_nuevos.items()])
                        if validacion.confirmar_accion(f"modificar sus datos personales ({cambios_texto})"):
                            nuevo_identificador = modificar_datos_usuario(usuario_actual, datos_nuevos)
                            if nuevo_identificador:
                                usuario_actual = nuevo_identificador
                        else:
                            print("Modificación de datos cancelada.")
                            pausar()
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
            # Validar mail
            bandera = True
            while bandera:
                mail = input("Ingrese su mail: ").strip().lower()  # Normalizar a minúsculas
                if not mail:
                    print("ERROR: El mail no puede estar vacío.")
                    continue
                if not validacion.validar_mail(mail):
                    print("ERROR: El mail debe tener un dominio válido (gmail, hotmail, outlook, yahoo, cineuade.com, etc.).")
                    continue
                # Verificar si el mail ya está registrado (búsqueda case-insensitive)
                mail_existe = False
                for usuario_key in usuarios.keys():
                    if usuario_key.lower() == mail:
                        mail_existe = True
                        break
                if mail_existe:
                    print("ERROR: El mail ya está registrado.")
                    continue
                bandera = False
            
            # Validar nombre
            bandera = True
            while bandera:
                nombre = input("Ingrese su nombre: ").strip()
                if not nombre:
                    print("ERROR: El nombre no puede estar vacío.")
                    continue
                if not validacion.validar_solo_letras(nombre):
                    print("ERROR: El nombre solo puede contener letras, espacios y guiones. No se permiten números.")
                    continue
                bandera = False
            
            # Validar apellido
            bandera = True
            while bandera:
                apellido = input("Ingrese su apellido: ").strip()
                if not apellido:
                    print("ERROR: El apellido no puede estar vacío.")
                    continue
                if not validacion.validar_solo_letras(apellido):
                    print("ERROR: El apellido solo puede contener letras, espacios y guiones. No se permiten números.")
                    continue
                bandera = False
            
            # Validar edad
            bandera = True
            while bandera:
                edad_str = input("Ingrese su edad: ").strip()
                if not edad_str:
                    print("ERROR: La edad no puede estar vacía.")
                    continue
                try:
                    edad = int(edad_str)
                    if edad < 0 or edad > 120:
                        print("ERROR: La edad debe ser un número válido entre 0 y 120.")
                        continue
                    bandera = False
                except ValueError:
                    print("ERROR: La edad debe ser un número válido.")
                    continue
            
            # Validar contraseña
            bandera = True
            while bandera:
                contrasenia = input("Ingrese su contraseña: ").strip()
                if not contrasenia:
                    print("ERROR: La contraseña no puede estar vacía.")
                    continue
                if not validacion.validar_contrasena(contrasenia):
                    print("ERROR: La contraseña debe tener al menos 5 caracteres.")
                    continue
                bandera = False
            
            # Si todas las validaciones pasaron, registrar
            if registrar_usuario(mail, nombre, apellido, edad, contrasenia):
                pausar()
            else:
                pausar()

        elif opcion == "2":
            bandera = True
            while bandera:
                usuario = input("Mail (o -1 para volver): ").strip().lower()  # Normalizar a minúsculas
                if usuario == "-1":
                    bandera = False
                    continue
                contrasenia = input("Contraseña: ").strip()
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
            # Validar nombre de película inmediatamente después del Enter
            bandera = True
            while bandera:
                pelicula = input("Ingrese el título de la película: ").strip()
                if not pelicula:
                    print("ERROR: El título de la película no puede estar vacío.")
                    continue
                
                # Cargar películas para validar existencia
                peliculas = cargar_peliculas()
                pelicula_existe = False
                pelicula_normalizada = pelicula.lower()
                
                # Verificar si la película existe (búsqueda case-insensitive)
                for pelicula_data in peliculas:
                    if pelicula_data.get("titulo", "").lower() == pelicula_normalizada:
                        pelicula_existe = True
                        # Usar el título original de la película
                        pelicula = pelicula_data.get("titulo", pelicula)
                        break
                
                if not pelicula_existe:
                    print(f"ERROR: La película '{pelicula}' no existe en el sistema.")
                    print("\nOpciones:")
                    print("1. Intentar con otra película")
                    print("-1. Volver al menú")
                    opcion_error = input("Seleccione una opción: ").strip()
                    if opcion_error == "-1":
                        bandera = False
                        continue
                    elif opcion_error == "1":
                        continue  # Volver a pedir película
                    else:
                        print("Opción no válida. Volviendo al menú.")
                        bandera = False
                        continue
                else:
                    bandera = False
            
            # Solo pedir fecha si la película existe
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