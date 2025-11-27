import os
import json

rutaUsuarios = os.path.join(os.path.dirname(__file__), "usuarios.txt")
rutaPeliculas = os.path.join(os.path.dirname(__file__), "peliculas.txt")
rutaAdmins = os.path.join(os.path.dirname(__file__), "admins.txt")

def validar_usuario_y_contrasena(usuario, contrasena):
    """
    Función encargada de validar las credenciales de usuario.
    
    Returns:
        Diccionario del usuario si las credenciales son válidas, None si no son válidas, None si hay error
    """ 
    try:
        # Limpiar espacios en blanco y normalizar a minúsculas
        usuario = usuario.strip().lower() if usuario else ""
        contrasena = contrasena.strip() if contrasena else ""
        
        if not usuario or not contrasena:
            return None
        
        with open(rutaUsuarios, "r", encoding="utf-8") as archivoUsuarios:
            usuarios = json.load(archivoUsuarios)
        
        # Verificar que el usuario existe (búsqueda case-insensitive)
        usuario_encontrado = None
        for usuario_key in usuarios.keys():
            if usuario_key.lower() == usuario:
                usuario_encontrado = usuario_key
                break
        
        if usuario_encontrado is None:
            return None
        
        usuario = usuario_encontrado  # Usar la clave original del diccionario
        
        # Obtener la contraseña del usuario (puede estar como "contraseña" o "contrasena")
        contrasena_guardada = usuarios[usuario].get("contraseña") or usuarios[usuario].get("contrasena")
        
        # Comparar contraseñas
        if contrasena_guardada == contrasena:
            return usuarios[usuario]
        
        return None
        
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"ERROR: Error tipo: {e}")
        return None


def validar_admin_y_contrasena(usuario, contrasena):
    """
    Función encargada de validar las credenciales de administrador.
    
    Returns:
        Diccionario del admin si las credenciales son válidas, None si no son válidas, None si hay error
    """
    try:
        # Limpiar espacios en blanco y normalizar a minúsculas
        usuario = usuario.strip().lower() if usuario else ""
        contrasena = contrasena.strip() if contrasena else ""
        
        if not usuario or not contrasena:
            return None
        
        with open(rutaAdmins, "r", encoding="utf-8") as archivoAdmins:
            admins = json.load(archivoAdmins)
        
        # Verificar que el usuario existe (búsqueda case-insensitive)
        usuario_encontrado = None
        for usuario_key in admins.keys():
            if usuario_key.lower() == usuario:
                usuario_encontrado = usuario_key
                break
        
        if usuario_encontrado is None:
            return None
        
        usuario = usuario_encontrado  # Usar la clave original del diccionario
        
        # Obtener la contraseña del admin (puede estar como "Contraseña" o "contraseña")
        contrasena_guardada = admins[usuario].get("Contraseña") or admins[usuario].get("contraseña")
        
        # Comparar contraseñas
        if contrasena_guardada == contrasena:
            return admins[usuario]
        
        return None
        
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"ERROR: Error tipo: {e}")
        return None

def validar_mail(mail):
    """
    Función encargada de verificar que el correo tenga un dominio válido.
    """ 
    
    dominios =  ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "gmail.com.ar", "hotmail.com.ar", "cineuade.com"]
    
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
    caracteresMinimos = 5
    if len(contrasena) < caracteresMinimos:
        return False
    return True

def validar_solo_letras(texto):
    """
    Función encargada de verificar que el texto solo contenga letras, espacios y caracteres especiales comunes (guiones, apóstrofes).
    No permite números.
    
    Args:
        texto: String a validar
    
    Returns:
        True si solo contiene letras y caracteres permitidos, False si contiene números u otros caracteres no permitidos
    """
    if not texto or not texto.strip():
        return False
    
    # Permitir letras (incluyendo acentos), espacios, guiones y apóstrofes
    # (para nombres compuestos como "María José", "O'Connor", "Jean-Pierre")
    texto_limpio = texto.strip()
    
    # Verificar que al menos tenga una letra (no solo espacios o caracteres especiales)
    tiene_letra = False
    
    for caracter in texto_limpio:
        # Si es un número, rechazar inmediatamente
        if caracter.isdigit():
            return False
        
        # Si es una letra (incluye acentos y ñ), permitir
        if caracter.isalpha():
            tiene_letra = True
        # Si es espacio, guion o apóstrofe, permitir
        elif caracter.isspace() or caracter in ['-', "'", '´']:
            continue
        # Cualquier otro carácter no permitido
        else:
            return False
    
    # Debe tener al menos una letra
    return tiene_letra

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

def butaca_existe(funcion_id, fila, columna, funciones):
    """
    Función auxiliar para verificar solo si la butaca existe (sin verificar disponibilidad).
    
    Args:
        funcion_id: ID de la función
        fila: Número de fila (1-based)
        columna: Número de columna/asiento (1-based)
        funciones: Diccionario con todas las funciones
    
    Returns:
        True si la butaca existe, False en caso contrario
    """
    # Verificar que la función existe
    if funcion_id not in funciones:
        return False
    
    butacas = funciones[funcion_id].get("Butacas", [])
    if not butacas:
        return False
    
    total_filas = len(butacas)
    total_cols = len(butacas[0]) if total_filas > 0 else 0
    
    # Validar que fila y columna estén en rango válido (1-based)
    if fila < 1 or columna < 1:
        return False
    if fila > total_filas or columna > total_cols:
        return False
    
    return True


def validar_butaca_disponible(funcion_id, fila, columna, funciones):
    """
    Función encargada de verificar que la butaca esté libre en una función.
    Combina la verificación de existencia y disponibilidad de la butaca.
    
    Args:
        funcion_id: ID de la función
        fila: Número de fila (1-based)
        columna: Número de columna/asiento (1-based)
        funciones: Diccionario con todas las funciones
    
    Returns:
        True si la butaca existe y está libre, False en caso contrario
    """
    # Primero verificar que existe
    if not butaca_existe(funcion_id, fila, columna, funciones):
        return False
    
    # Luego verificar que está libre (convertir a 0-based para acceder a la matriz)
    butacas = funciones[funcion_id]["Butacas"]
    estado_butaca = butacas[fila - 1][columna - 1]
    if estado_butaca != "Libre":
        return False
    
    return True

def validar_funcion_no_solapada(sala, fecha, hora, duracion_pelicula, funciones_dict=None, peliculas_dict=None):
    """
    Función encargada de verificar que no existan funciones solapadas en la misma sala y horario.
    Considera la duración de la película para detectar solapamientos reales.
    
    Args:
        sala: Número de sala (string)
        fecha: Fecha de la función (DD-MM-YY)
        hora: Hora de inicio (HH:MM)
        duracion_pelicula: Duración de la película en minutos (int o string convertible)
        funciones_dict: Diccionario de funciones (opcional). Si se proporciona, se usa en lugar de leer el archivo.
        peliculas_dict: Diccionario de películas (opcional). Si se proporciona, se usa en lugar de leer el archivo.
    
    Returns:
        Tupla (resultado, pelicula_solapada):
        - (True, None) si no hay solapamiento
        - (False, nombre_pelicula) si hay solapamiento, donde nombre_pelicula es el nombre de la película que causa el solapamiento
    """
    try:
        # Convertir duración a int si es string
        if isinstance(duracion_pelicula, str):
            try:
                duracion_pelicula = int(duracion_pelicula)
            except:
                duracion_pelicula = 0
        
        # Si se proporciona el diccionario de funciones, usarlo directamente
        if funciones_dict is not None:
            funciones = funciones_dict
        else:
            # Si no se proporciona, leer del archivo
            rutaFunciones = os.path.join(os.path.dirname(__file__), "funciones.txt")
            with open(rutaFunciones, "r", encoding="utf-8") as archivoFunciones:
                funciones = json.load(archivoFunciones)
        
        # Si se proporciona el diccionario de películas, usarlo directamente
        if peliculas_dict is not None:
            peliculas = peliculas_dict
        else:
            # Si no se proporciona, leer del archivo
            with open(rutaPeliculas, "r", encoding="utf-8") as archivoPeliculas:
                peliculas = json.load(archivoPeliculas)
        
        # Convertir sala a string para comparación consistente
        sala = str(sala)
        
        # Calcular hora de fin de la nueva función
        # Parsear hora de inicio (HH:MM)
        partes_hora = hora.split(':')
        if len(partes_hora) != 2:
            return (False, "Función desconocida")
        
        try:
            hora_inicio_nueva = int(partes_hora[0])
            minuto_inicio_nueva = int(partes_hora[1])
        except ValueError:
            return (False, "Función desconocida")
        
        # Calcular minutos totales desde medianoche para inicio
        minutos_inicio_nueva = hora_inicio_nueva * 60 + minuto_inicio_nueva
        
        # Calcular minutos totales desde medianoche para fin
        minutos_fin_nueva = minutos_inicio_nueva + duracion_pelicula
        
        # Verificar solapamiento con cada función existente
        for funcion_id, datos_funcion in funciones.items():
            # Verificar misma sala y misma fecha
            sala_funcion = str(datos_funcion.get("Sala", ""))
            fecha_funcion = datos_funcion.get("Fecha", "")
            
            if sala_funcion != sala or fecha_funcion != fecha:
                continue  # No es la misma sala/fecha, no puede haber solapamiento
            
            # Obtener hora de la función existente
            hora_funcion = datos_funcion.get("Hora", "")
            if not hora_funcion:
                continue
            
            # Parsear hora de la función existente
            partes_hora_existente = hora_funcion.split(':')
            if len(partes_hora_existente) != 2:
                continue
            
            try:
                hora_inicio_existente = int(partes_hora_existente[0])
                minuto_inicio_existente = int(partes_hora_existente[1])
            except ValueError:
                continue
                
            minutos_inicio_existente = hora_inicio_existente * 60 + minuto_inicio_existente
            
            # Obtener duración de la película de la función existente
            pelicula_existente = datos_funcion.get("Película", "")
            if not pelicula_existente:
                # Si no hay película, hacer verificación simple (solo hora exacta)
                if hora == hora_funcion:
                    return (False, "Función desconocida")
                continue
            
            # Buscar la película en el diccionario de películas
            duracion_existente = 0
            if pelicula_existente in peliculas:
                duracion_existente_str = peliculas[pelicula_existente].get("Duración", "0")
                try:
                    duracion_existente = int(duracion_existente_str) if isinstance(duracion_existente_str, str) else duracion_existente_str
                except (ValueError, TypeError):
                    duracion_existente = 0
            else:
                # Si la película no se encuentra, hacer verificación simple (solo hora exacta)
                if hora == hora_funcion:
                    return (False, pelicula_existente)
                continue
            
            minutos_fin_existente = minutos_inicio_existente + duracion_existente
            
            # Verificar solapamiento: dos funciones se solapan si:
            # - La nueva empieza antes de que termine la existente Y
            # - La nueva termina después de que empiece la existente
            hay_solapamiento = (
                minutos_inicio_nueva < minutos_fin_existente and
                minutos_fin_nueva > minutos_inicio_existente
            )
            
            if hay_solapamiento:
                return (False, pelicula_existente)
        
        return (True, None)  # No hay solapamiento
    
    except Exception as e:
        print(f"Error al validar solapamiento de funciones: {e}")
        return (False, "Error desconocido")

def validar_pelicula_existente(pelicula, peliculas_dict=None):
    """
    Función encargada de verificar que la película exista antes de asignarla a una función.
    
    Args:
        pelicula: Nombre de la película a validar
        peliculas_dict: Diccionario de películas (opcional). Si se proporciona, se usa en lugar de leer el archivo.
    
    Returns:
        True si la película existe, False si no existe, -1 si hay error
    """
    try:
        # Si se proporciona el diccionario, usarlo directamente (más eficiente)
        if peliculas_dict is not None:
            pelicula_sin_espacios = pelicula.strip()
            # Buscar coincidencia exacta primero (más rápido)
            if pelicula_sin_espacios in peliculas_dict:
                return True
            # Si no hay coincidencia exacta, buscar case-insensitive
            for titulo in peliculas_dict.keys():
                if pelicula_sin_espacios.lower() == titulo.lower():
                    return True
            return False
        
        # Si no se proporciona diccionario, leer del archivo
        with open(rutaPeliculas, "r", encoding="utf-8") as archivoPelicula:
            peliculas = json.load(archivoPelicula)
            
            pelicula_sin_espacios = pelicula.strip()
            # Buscar coincidencia exacta primero
            if pelicula_sin_espacios in peliculas:
                return True
            # Si no hay coincidencia exacta, buscar case-insensitive
            for titulo in peliculas.keys():
                if pelicula_sin_espacios.lower() == titulo.lower():
                    return True
            return False
    
    except FileNotFoundError:
        print("ERROR: El archivo no se pudo encontrar. Intentelo más tarde")
        return False
    
    except Exception as e:
        print(f"Error al validar película: {e}")
        return False
        
def validar_datos_no_nulos(datos):
    """
    Función encargada de verificar que los datos ingresados no sean nulos
    """
    for dato in datos:
        if dato is None:
            return False
        
        if type(dato) == str:
            datoSinEspacios = dato.strip()
            if datoSinEspacios == "":
                return False
    
    return True

def validar_usuario_registrado(usuario):
    """
    Función encargada de verificar que el usuario esté registrado en el sistema.
    """
    try:
        with open(rutaUsuarios, "r", encoding="utf-8") as archivoUsuarios:
            usuarios = json.load(archivoUsuarios)
            if usuario in usuarios:
                return True
            else:
                return False
    except FileNotFoundError:
        print("ERROR: El archivo no se pudo encontrar. intentelo más tarde")
    except Exception as e:
        print(f"ERROR: Error del tipo: {e}")
        return False

def confirmar_accion(accion):
    """
    Función encargada de pedir confirmación antes de ejecutar una acción crítica.
    """
    print(f"¿Confirma que desea {accion}? (S/N): ")
    respuesta = input().strip().upper()

    while respuesta not in ("S", "N"):
        print("Respuesta inválida. Ingrese 'S' para Sí o 'N' para No.")
        respuesta = input("¿Confirma? (S/N): ").strip().upper()

    if respuesta == "S":
        return True
    else:
        return False

def manejar_entrada_invalida(entrada):
    """ 
    Función encargada de manejar entradas inválidas del usuario.
    
    ACLARACION: Sirve únicamente para mostrar un mensaje estándar cuando el usuario ingresa algo incorrecto.
    No realiza validaciones complejas porque es imposible cubrir todos los escenarios; solo centraliza el mensaje de error.
    """
    print(f"Entrada inválida: '{entrada}'. Por favor, intentelo nuevamente.")  
   

def verificar_usuario_registrado(usuario):
    """
    Función encargada de revisar si el usuario está registrado antes de realizar la compra.
    Similar a validar_usuario_registrado() pero con propósito específico para compras.
    
    Args:
        usuario: Mail o nombre de usuario a verificar
    
    Returns:
        True si el usuario está registrado, False en caso contrario
    """
    try:
        # Normalizar a minúsculas para búsqueda case-insensitive
        usuario_normalizado = usuario.strip().lower() if usuario else ""
        
        with open(rutaUsuarios, "r", encoding="utf-8") as archivoUsuarios:
            usuarios = json.load(archivoUsuarios)
            # Búsqueda case-insensitive
            for usuario_key in usuarios.keys():
                if usuario_key.lower() == usuario_normalizado:
                    return True
            return False
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"ERROR: Error del tipo: {e}")
        return False

def validar_titulo_pelicula(titulo):
    """
    Función encargada de validar que el título de la película cumpla con los requisitos:
    - Debe tener al menos 2 caracteres
    - No puede ser solamente un carácter especial
    
    Args:
        titulo: String con el título de la película a validar
    
    Returns:
        True si el título es válido, False en caso contrario
    """
    if not titulo or not titulo.strip():
        return False
    
    titulo_limpio = titulo.strip()
    
    # Verificar que tenga al menos 2 caracteres
    if len(titulo_limpio) < 2:
        return False
    
    # Verificar que no sea solo un carácter especial
    # Contar cuántos caracteres son letras o números
    caracteres_validos = 0
    for caracter in titulo_limpio:
        if caracter.isalnum():  # Letra o número
            caracteres_validos += 1
    
    # Debe tener al menos un carácter alfanumérico
    if caracteres_validos == 0:
        return False
    
    return True