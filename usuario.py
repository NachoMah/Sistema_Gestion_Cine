#from usuario import consultar_butacas
#from admin import funciones            ------------> (Posibles imports para sacar datos de las funciones de admin.py)
import json
from validacion import validar_usuario_registrado, validar_pelicula_existente, validar_butaca_disponible, validar_edad


usuarios = {}
peliculas_disponibles = [
    {"titulo": "Gladiador", "genero": "accion", "duracion": 155},
    {"titulo": "Batman", "genero": "superheroes", "duracion": 176},
    {"titulo": "Saw", "genero": "terror", "duracion": 100},
]

def registrar_usuario(usuario):
    """
    Registra un nuevo usuario en el sistema
    """
    try:
        if usuario in usuarios:
            print("El usuario ya existe")
            return False
        usuarios[usuario] = {"reservas": []}
        print(f"Usuario '{usuario} registrado correctamente.")
        return True
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return False

def login_usuario(usuario, contrasena):
    """
    Validamos el inicio de sesion de un usuario
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

def ver_cartelera():
    """
    Devuelve el listado de películas disponibles
    """
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

# usuarios.py

def ver_horarios_pelicula(pelicula, fecha=None, funciones_dict=None):
    """
    Devuelve los horarios/salas de una película.
    Si se pasa 'fecha' (DD-MM-YY), filtra por ese día.
    Retorna lista de dicts: [{'funcion_id','fecha','hora','sala'}, ...]
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


def consultar_butacas(funcion_id, funciones):
    """
    Funcion encaragada de mostrar la disponibilidad de butacas.
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

def comprar_entrada(usuario, funcion_id, butaca, funciones):
    """
    Permite comprar una entrada simulada con validaciones.
    """
    try:
        if not validar_usuario_registrado(usuario):
            print("El usuario no está registrado.")
            return False

        if funcion_id not in funciones:
            print(f"La función '{funcion_id}' no existe.")
            return False

        datos_funcion = funciones[funcion_id]
        pelicula = datos_funcion["Película"]

        if not validar_pelicula_existente(pelicula):
            print(f"La película '{pelicula}' no está en cartelera.")
            return False
        
        if not validar_edad(usuario, pelicula):
            print(f"El usuario no cumple con la edad mínima para '{pelicula}'.")
            return False

        if not validar_butaca_disponible(datos_funcion, butaca):
            print("La butaca seleccionada no está disponible.")
            return False

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

def ver_historial_compras(usuario):
    # se encarga de devolver el historial completo de compras de un usuario.
    pass

def modificar_datos_usuario(usuario, datos_nuevos):
    """
    Funcion encaragada de modifciar datos 
    (SE DEBE MEJORAR CUANDO SE COMPLETE EL MODULO DE VALDIACIONES, POR EL MOMENTO QUEDA SIMPLE)
    """
    try:
        if usuario not in usuarios:
            print("El usuario no existe.")
            return False
        
        usuarios[usuario].update(datos_nuevos)
        print(f"Datos de '{usuario}' actualizados correctamente.")
        return True
    except Exception as e:
        print(f"Error al modificar los datos: {e}")
        return False

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

def buscar_peliculas(filtros):
    """
    Busca películas según filtros (por ejemplo, género o duración máxima)
    Usa lista por comprensión + lambda
    """
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

def generar_comprobante(compra):
    """
    Genera un comprobante de compra en formato JSON
    """
    try:
        archivo = f"comprobante_{compra['pelicula']}.txt"
        with open(archivo, "w", encoding="utf-8") as archivo:
            json.dump(compra, archivo, indent=4, ensure_ascii=False)
        print(f"Comprobante generado: {archivo}")
        return True
    except Exception as e:
        print(f"Error al generar comprobante: {e}")
        return False
    
def mainUsuario():
    """
    Funcion encaragada de mostrar un menú interactivo para navegar y utilziar otdas las funciones creadas en su modulo.
    """
    pass