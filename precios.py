import json

from clear import clear

# Variable global para almacenar los precios
precios = {
    "precio_base": 10000,  # Precio base por defecto
    "precio_3D": 7000,
    "precio_VIP": 15000,
    "descuento_estudiante": 0.20,  # 20% de descuento
    "descuento_jubilado": 0.30,    # 30% de descuento
    "descuento_niños": 0.25        # 25% de descuento (menores de 12)
}

# Variable global para almacenar promociones
promociones = {}

def cargar_precios():
    """
    Se carga los precios desde archivo
    """
    global precios
    try:
        with open("precios.txt", "r", encoding="utf-8") as f:
            precios = json.load(f)
        print("Precios cargados correctamente.")
        return True
    except FileNotFoundError:
        # Si no existe el archivo, se crea por defecto
        guardar_precios()
        print("Archivo de precios creado con valores por defecto.")
        return True
    except Exception as e:
        print(f"Error al cargar precios: {e}")
        return False


def guardar_precios():
    """
    Guarda los precios en archivo
    """
    try:
        with open("precios.txt", "w", encoding="utf-8") as f:
            json.dump(precios, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar precios: {e}")
        return False


def modificar_precio_base(nuevo_precio):
    """
    Modifica el precio base de las entradas
    """
    try:
        nuevo_precio = float(nuevo_precio)
        if nuevo_precio <= 0:
            print("El precio debe ser mayor a 0.")
            return False
        
        precios["precio_base"] = nuevo_precio
        guardar_precios()
        print(f"Precio base actualizado a: ${nuevo_precio}")
        return True
    except ValueError:
        print("Debe ingresar un número válido.")
        return False


def modificar_precio_3D(nuevo_precio):
    """
    Modifica el precio para funciones 3D
    """
    try:
        nuevo_precio = float(nuevo_precio)
        if nuevo_precio <= 0:
            print("El precio debe ser mayor a 0.")
            return False
        
        precios["precio_3D"] = nuevo_precio
        guardar_precios()
        print(f"Precio 3D actualizado a: ${nuevo_precio}")
        return True
    except ValueError:
        print("Debe ingresar un número válido.")
        return False


def modificar_precio_VIP(nuevo_precio):
    """
    Modifica el precio para salas VIP
    """
    try:
        nuevo_precio = float(nuevo_precio)
        if nuevo_precio <= 0:
            print("El precio debe ser mayor a 0.")
            return False
        
        precios["precio_VIP"] = nuevo_precio
        guardar_precios()
        print(f"Precio VIP actualizado a: ${nuevo_precio}")
        return True
    except ValueError:
        print("Debe ingresar un número válido.")
        return False


def modificar_descuento(tipo_descuento, porcentaje):
    """
    Modifica un descuento específico.
    tipo_descuento: 'estudiante', 'jubilado', 'niños'
    porcentaje: valor entre 0 y 100
    """
    try:
        porcentaje = float(porcentaje)
        if porcentaje < 0 or porcentaje > 100:
            print("El porcentaje debe estar entre 0 y 100.")
            return False
        
        descuento_decimal = porcentaje / 100
        
        if tipo_descuento == "estudiante":
            precios["descuento_estudiante"] = descuento_decimal
        elif tipo_descuento == "jubilado":
            precios["descuento_jubilado"] = descuento_decimal
        elif tipo_descuento == "niños":
            precios["descuento_niños"] = descuento_decimal
        else:
            print("Tipo de descuento no válido.")
            return False
        
        guardar_precios()
        print(f"Descuento {tipo_descuento} actualizado a: {porcentaje}%")
        return True
    except ValueError:
        print("Debe ingresar un número válido.")
        return False


def calcular_precio_entrada(tipo_entrada="normal", aplicar_descuento=None):
    """
    Calcula el precio de una entrada según el tipo y descuentos aplicables.
    
    tipo_entrada: 'normal', '3D', 'VIP'
    aplicar_descuento: None, 'estudiante', 'jubilado', 'niños'
    """
    # Obtener precio base según tipo de entrada
    if tipo_entrada == "3D":
        precio = precios["precio_3D"]
    elif tipo_entrada == "VIP":
        precio = precios["precio_VIP"]
    else:
        precio = precios["precio_base"]
    
    # Aplicar descuento si corresponde
    if aplicar_descuento == "estudiante":
        precio = precio * (1 - precios["descuento_estudiante"])
    elif aplicar_descuento == "jubilado":
        precio = precio * (1 - precios["descuento_jubilado"])
    elif aplicar_descuento == "niños":
        precio = precio * (1 - precios["descuento_niños"])
    
    return round(precio, 2)


def obtener_precio_base():
    """
    Retorna el precio a base actual
    """
    return precios["precio_base"]


def ver_lista_precios():
    """
    Muestra todos los precios y descuentos configurados
    """
    print("\n" + "="*50)
    print("    LISTA DE PRECIOS")
    print("="*50)
    print(f"Precio base (2D):        ${precios['precio_base']}")
    print(f"Precio 3D:               ${precios['precio_3D']}")
    print(f"Precio VIP:              ${precios['precio_VIP']}")
    print("\nDescuentos:")
    print(f"Estudiantes:             {precios['descuento_estudiante']*100}%")
    print(f"Jubilados:               {precios['descuento_jubilado']*100}%")
    print(f"Niños (menores de 12):   {precios['descuento_niños']*100}%")
    print("="*50)
    
    # Mostrar ejemplos de precios con descuentos
    print("\nEjemplos de precios finales:")
    print(f"Entrada normal:                ${calcular_precio_entrada('normal')}")
    print(f"Entrada normal (estudiante):   ${calcular_precio_entrada('normal', 'estudiante')}")
    print(f"Entrada 3D:                    ${calcular_precio_entrada('3D')}")
    print(f"Entrada 3D (jubilado):         ${calcular_precio_entrada('3D', 'jubilado')}")
    print(f"Entrada VIP:                   ${calcular_precio_entrada('VIP')}")
    print(f"Entrada VIP (niños):           ${calcular_precio_entrada('VIP', 'niños')}")
    print("="*50)


def cargar_promociones():
    """
    Carga las promociones desde archivo
    """
    global promociones
    try:
        with open("promociones.txt", "r", encoding="utf-8") as f:
            promociones = json.load(f)
        print("Promociones cargadas correctamente.")
        return True
    except FileNotFoundError:
        guardar_promociones()
        print("Archivo de promociones creado con valores por defecto (vacío).")
        return True
    except Exception as e:
        print(f"Error al cargar promociones: {e}")
        return False

def guardar_promociones():
    """
    Guarda las promociones en archivo
    """
    try:
        with open("promociones.txt", "w", encoding="utf-8") as f:
            json.dump(promociones, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar promociones: {e}")
        return False

def ver_promociones():
    if not promociones:
        print("No hay promociones registradas.")
    else:
        print("\nPromociones vigentes:")
        for nombre, datos in sorted(promociones.items()):
            tipo = datos.get("Tipo", "N/A")
            condicion = datos.get("Condición", "N/A")
            print(f"- {nombre}: Tipo={tipo}, Condición={condicion}")

def agregar_promocion_menu():
    nombre = input("Nombre de la promoción: ").strip()
    if not nombre:
        print("El nombre no puede estar vacío.")
        return
    if nombre in promociones:
        print("La promoción ya existe.")
        return
    tipo = input("Tipo (descuento, 2x1, etc.): ").strip()
    condicion = input("Condición (ej.: miércoles, fecha especial): ").strip()
    promociones[nombre] = {
        "Tipo": tipo,
        "Condición": condicion
    }
    if guardar_promociones():
        print("Promoción agregada correctamente.")

def eliminar_promocion_menu():
    if not promociones:
        print("No hay promociones para eliminar.")
        return
    nombre = input("Nombre de la promoción a eliminar: ").strip()
    if nombre not in promociones:
        print("La promoción indicada no existe.")
        return
    del promociones[nombre]
    if guardar_promociones():
        print("Promoción eliminada correctamente.")


def menu_gestion_precios():
    """
    Menú para gestionar precios, descuentos y promociones
    """
    cargar_precios()
    cargar_promociones()
    
    while True:
        clear()
        print("\n" + "="*50)
        print("    GESTIÓN DE PRECIOS Y PROMOCIONES")
        print("="*50)
        print("1. Ver lista de precios")
        print("2. Modificar precio base (2D)")
        print("3. Modificar precio 3D")
        print("4. Modificar precio VIP")
        print("5. Modificar descuento estudiantes")
        print("6. Modificar descuento jubilados")
        print("7. Modificar descuento niños")
        print("8. Ver promociones")
        print("9. Agregar promoción")
        print("10. Eliminar promoción")
        print("0. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            ver_lista_precios()
            input("\nPresione Enter para continuar...")
        
        elif opcion == "2":
            nuevo_precio = input("Ingrese el nuevo precio base: $")
            modificar_precio_base(nuevo_precio)
            input("\nPresione Enter para continuar...")
        
        elif opcion == "3":
            nuevo_precio = input("Ingrese el nuevo precio 3D: $")
            modificar_precio_3D(nuevo_precio)
            input("\nPresione Enter para continuar...")
        
        elif opcion == "4":
            nuevo_precio = input("Ingrese el nuevo precio VIP: $")
            modificar_precio_VIP(nuevo_precio)
            input("\nPresione Enter para continuar...")
        
        elif opcion == "5":
            porcentaje = input("Ingrese el porcentaje de descuento (0-100): ")
            modificar_descuento("estudiante", porcentaje)
            input("\nPresione Enter para continuar...")
        
        elif opcion == "6":
            porcentaje = input("Ingrese el porcentaje de descuento (0-100): ")
            modificar_descuento("jubilado", porcentaje)
            input("\nPresione Enter para continuar...")
        
        elif opcion == "7":
            porcentaje = input("Ingrese el porcentaje de descuento (0-100): ")
            modificar_descuento("niños", porcentaje)
            input("\nPresione Enter para continuar...")
        
        elif opcion == "8":
            ver_promociones()
            input("\nPresione Enter para continuar...")
        
        elif opcion == "9":
            agregar_promocion_menu()
            input("\nPresione Enter para continuar...")
        
        elif opcion == "10":
            eliminar_promocion_menu()
            input("\nPresione Enter para continuar...")
        
        elif opcion == "0":
            break
        
        else:
            print("Opción no válida.")
            input("\nPresione Enter para continuar...")


def seleccionar_tipo_entrada():
    """
    Permite al usuario seleccionar el tipo de entrada.
    Retorna el tipo seleccionado.
    """
    print("\nTipos de entrada disponibles:")
    print("1. Normal (2D)")
    print("2. 3D")
    print("3. VIP")
    
    while True:
        clear()
        opcion = input("Seleccione el tipo de entrada: ")
        if opcion == "1":
            return "normal"
        elif opcion == "2":
            return "3D"
        elif opcion == "3":
            return "VIP"
        else:
            print("Opción no válida. Intente nuevamente.")


def seleccionar_descuento():
    """
    Permite al usuario seleccionar si aplica algún descuento.
    Retorna el tipo de descuento o None.
    """
    print("\n¿Aplica algún descuento?")
    print("1. Sin descuento")
    print("2. Estudiante")
    print("3. Jubilado")
    print("4. Niño (menor de 12 años)")
    
    while True:
        clear()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            return None
        elif opcion == "2":
            return "estudiante"
        elif opcion == "3":
            return "jubilado"
        elif opcion == "4":
            return "niños"
        else:
            print("Opción no válida. Intente nuevamente.")


# Inicializar precios al cargar el módulo
cargar_precios()
cargar_promociones()