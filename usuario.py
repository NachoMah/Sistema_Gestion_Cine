usuarios = {}
peliculas_disponibles = [
    {"titulo": "Gladiador", "genero": "accion", "duracion": 155},
    {"titulo": "Batman", "genero": "superheroes", "duracion": 176},
    {"titulo": "Saw", "genero": "terror", "duracion": 100},
]

def registrar_usuario(usuario):
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
    # se encarga de validar el inicio de sesión de un usuario.
    pass

def ver_cartelera():
    # se encarga de devolver el listado de películas disponibles en cartelera.
    pass

def ver_horarios_pelicula(pelicula, fecha=None):
    # se encarga de devolver los horarios de una película según el día.
    pass

def consultar_butacas(funcion):
    # se encarga de devolver la disponibilidad de butacas en una función.
    pass

def comprar_entrada(usuario, funcion, butaca):
    # se encarga de permitir la compra de una entrada (seleccionando función y butaca).
    pass

def ver_reservas_usuario(usuario):
    # se encarga de devolver todas las reservas activas de un usuario.
    pass

def ver_historial_compras(usuario):
    # se encarga de devolver el historial completo de compras de un usuario.
    pass

def modificar_datos_usuario(usuario, datos_nuevos):
    # se encarga de permitir modificar los datos personales de un usuario.
    pass

def borrar_cuenta(usuario):
    # se encarga de eliminar la cuenta del usuario y sus datos asociados.
    pass

def buscar_peliculas(filtros):
    """
    Busca peliculas segun filtros (por ejemplo, genero o duracion menor a un valor).
    Se usa lambda y listas por comprension.
    """
    try:
        genero = filtros.get("genero", None)
        max_duracion = filtros.get("max_duracion", None)

        resultado = [
            p for p in peliculas_disponibles
            if (not genero or p["genero"].lower() == genero.lower()) and (not max_duracion or p["duracion"] <= max_duracion)
        ]

        resultado = sorted(resultado, key=lambda x: x["titulo"])

        if not resultado:
            print("No se encontraron peliculas con esos filtros.")
        else:
            print("Peliculas encontradas:")
            for p in resultado:
                print(f"- {p['titulo']} ({p['genero']}, {p['duracion']} min)")
        return resultado
    except Exception as e:
        print(f"Ocurrio un error al buscar peliculas: {e}")
        return[]

def generar_comprobante(compra):
    # se encarga de generar un comprobante de la compra con todos los datos necesarios.
    pass