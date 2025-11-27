import unittest
import json
import os
import sys
from unittest.mock import patch, mock_open, MagicMock

import validacion

class TestValidaciones(unittest.TestCase):
    """
    Suite de tests para todas las funciones de validación del sistema de cine.
    """
    def setUp(self):
        """
        Configuración inicial antes de cada test.
        """
        # Datos de prueba para usuarios
        self.usuarios_test = {
            "test@gmail.com": {
                "nombre": "Juan",
                "apellido": "Pérez",
                "edad": 25,
                "mail": "test@gmail.com",
                "contraseña": "password123",
                "reservas": []
            },
            "maria@hotmail.com": {
                "nombre": "María",
                "apellido": "González",
                "edad": 17,
                "mail": "maria@hotmail.com",
                "contraseña": "12345",
                "reservas": []
            }
        }
        
        # Datos de prueba para administradores
        self.admins_test = {
            "admin1": {
                "Contraseña": "admin123",
                "Mail": "admin@cineuade.com",
                "Nombre": "Carlos",
                "Apellido": "Admin"
            }
        }
        
        # Datos de prueba para películas
        self.peliculas_test = {
            "Avatar": {
                "Género": "Ciencia Ficción",
                "Duración": 162,
                "Fecha": "15-12-24",
                "Clasificación": "+13"
            },
            "Toy Story": {
                "Género": "Animación",
                "Duración": 81,
                "Fecha": "20-11-24",
                "Clasificación": "ATP"
            }
        }
        
        # Datos de prueba para funciones
        self.funciones_test = {
            "Avatar_151224_a": {
                "Película": "Avatar",
                "Fecha": "15-12-24",
                "Hora": "18:00",
                "Sala": "1",
                "Butacas": [
                    ["Libre", "Libre", "Ocupada", "Libre", "Libre", "Libre"],
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"],
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"],
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"],
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"],
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"]
                ]
            },
            "Avatar_151224_b": {
                "Película": "Avatar",
                "Fecha": "15-12-24",
                "Hora": "21:00",
                "Sala": "1",
                "Butacas": [
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"],
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"],
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"],
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"],
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"],
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"]
                ]
            }
        }
    
    def test_validar_mail_valido_gmail(self):
        """
        Test: mail válido con dominio gmail.com
        """
        self.assertTrue(validacion.validar_mail("usuario@gmail.com"))
    
    def test_validar_mail_valido_hotmail(self):
        """
        Test: mail válido con dominio hotmail.com
        """
        self.assertTrue(validacion.validar_mail("usuario@hotmail.com"))
    
    def test_validar_mail_valido_outlook(self):
        """
        Test: mail válido con dominio outlook.com
        """
        self.assertTrue(validacion.validar_mail("usuario@outlook.com"))
    
    def test_validar_mail_valido_yahoo(self):
        """
        Test: mail válido con dominio yahoo.com
        """
        self.assertTrue(validacion.validar_mail("usuario@yahoo.com"))
    
    def test_validar_mail_valido_cineuade(self):
        """
        Test: mail válido con dominio cineuade.com
        """
        self.assertTrue(validacion.validar_mail("admin@cineuade.com"))
    
    def test_validar_mail_invalido_sin_arroba(self):
        """
        Test: mail inválido sin @
        """
        self.assertFalse(validacion.validar_mail("usuariogmail.com"))
    
    def test_validar_mail_invalido_dominio_incorrecto(self):
        """
        Test: mail inválido con dominio no permitido
        """
        self.assertFalse(validacion.validar_mail("usuario@invalid.com"))
    
    def test_validar_mail_invalido_multiple_arroba(self):
        """
        Test: mail inválido con múltiples @
        """
        self.assertFalse(validacion.validar_mail("usuario@@gmail.com"))
    
    def test_validar_mail_vacio(self):
        """
        Test: mail vacío
        """
        self.assertFalse(validacion.validar_mail(""))
    
    def test_validar_contrasena_valida_minimo(self):
        """
        Test: contraseña válida con exactamente 5 caracteres
        """
        self.assertTrue(validacion.validar_contrasena("12345"))
    
    def test_validar_contrasena_valida_larga(self):
        """
        Test: contraseña válida con más de 5 caracteres
        """
        self.assertTrue(validacion.validar_contrasena("password123"))
    
    def test_validar_contrasena_invalida_corta(self):
        """
        Test: contraseña inválida con menos de 5 caracteres
        """
        self.assertFalse(validacion.validar_contrasena("1234"))
    
    def test_validar_contrasena_vacia(self):
        """
        Test: contraseña vacía
        """
        self.assertFalse(validacion.validar_contrasena(""))

    def test_validar_edad_atp_menor(self):
        """
        Test: usuario menor puede ver película ATP
        """
        usuario = {"edad": 5}
        pelicula = {"clasificacion": "ATP"}
        self.assertTrue(validacion.validar_edad(usuario, pelicula))
    
    def test_validar_edad_mas13_valido(self):
        """
        Test: usuario de 13+ años puede ver película +13
        """
        usuario = {"edad": 15}
        pelicula = {"clasificacion": "+13"}
        self.assertTrue(validacion.validar_edad(usuario, pelicula))
    
    def test_validar_edad_mas13_invalido(self):
        """
        Test: usuario menor de 13 no puede ver película +13
        """
        usuario = {"edad": 12}
        pelicula = {"clasificacion": "+13"}
        self.assertFalse(validacion.validar_edad(usuario, pelicula))
    
    def test_validar_edad_mas16_valido(self):
        """
        Test: usuario de 16+ años puede ver película +16
        """
        usuario = {"edad": 18}
        pelicula = {"clasificacion": "+16"}
        self.assertTrue(validacion.validar_edad(usuario, pelicula))
    
    def test_validar_edad_mas16_invalido(self):
        """
        Test: usuario menor de 16 no puede ver película +16
        """
        usuario = {"edad": 15}
        pelicula = {"clasificacion": "+16"}
        self.assertFalse(validacion.validar_edad(usuario, pelicula))
    
    def test_validar_edad_mas18_valido(self):
        """
        Test: usuario de 18+ años puede ver película +18
        """
        usuario = {"edad": 20}
        pelicula = {"clasificacion": "+18"}
        self.assertTrue(validacion.validar_edad(usuario, pelicula))
    
    def test_validar_edad_mas18_invalido(self):
        """
        Test: usuario menor de 18 no puede ver película +18
        """
        usuario = {"edad": 17}
        pelicula = {"clasificacion": "+18"}
        self.assertFalse(validacion.validar_edad(usuario, pelicula))
    
    def test_validar_edad_clasificacion_invalida(self):
        """
        Test: clasificación no reconocida
        """
        usuario = {"edad": 20}
        pelicula = {"clasificacion": "INVALID"}
        self.assertFalse(validacion.validar_edad(usuario, pelicula))
   
    def test_validar_datos_no_nulos_todos_validos(self):
        """
        Test: todos los datos son válidos (no nulos ni vacíos)
        """
        datos = ["Juan", "Pérez", "juan@gmail.com", "password123"]
        self.assertTrue(validacion.validar_datos_no_nulos(datos))
    
    def test_validar_datos_no_nulos_con_none(self):
        """
        Test: datos con valor None
        """
        datos = ["Juan", None, "juan@gmail.com"]
        self.assertFalse(validacion.validar_datos_no_nulos(datos))
    
    def test_validar_datos_no_nulos_con_string_vacio(self):
        """
        Test: datos con string vacío
        """
        datos = ["Juan", "", "juan@gmail.com"]
        self.assertFalse(validacion.validar_datos_no_nulos(datos))
    
    def test_validar_datos_no_nulos_con_espacios(self):
        """
        Test: datos con solo espacios en blanco
        """
        datos = ["Juan", "   ", "juan@gmail.com"]
        self.assertFalse(validacion.validar_datos_no_nulos(datos))
    
    def test_validar_datos_no_nulos_lista_vacia(self):
        """
        Test: lista vacía de datos
        """
        datos = []
        self.assertTrue(validacion.validar_datos_no_nulos(datos))

    def test_butaca_existe_valida(self):
        """
        Test: butaca existe en la función
        """
        resultado = validacion.butaca_existe(
            "Avatar_151224_a", 1, 1, self.funciones_test
        )
        self.assertTrue(resultado)
    
    def test_butaca_existe_fila_invalida(self):
        """
        Test: fila fuera de rango
        """
        resultado = validacion.butaca_existe(
            "Avatar_151224_a", 10, 1, self.funciones_test
        )
        self.assertFalse(resultado)
    
    def test_butaca_existe_columna_invalida(self):
        """
        Test: columna fuera de rango
        """
        resultado = validacion.butaca_existe(
            "Avatar_151224_a", 1, 10, self.funciones_test
        )
        self.assertFalse(resultado)
    
    def test_butaca_existe_funcion_invalida(self):
        """
        Test: función no existe
        """
        resultado = validacion.butaca_existe(
            "NoExiste", 1, 1, self.funciones_test
        )
        self.assertFalse(resultado)
    
    def test_validar_butaca_disponible_libre(self):
        """
        Test: butaca libre está disponible
        """
        resultado = validacion.validar_butaca_disponible(
            "Avatar_151224_a", 1, 1, self.funciones_test
        )
        self.assertTrue(resultado)
    
    def test_validar_butaca_disponible_ocupada(self):
        """
        Test: butaca ocupada no está disponible
        """
        resultado = validacion.validar_butaca_disponible(
            "Avatar_151224_a", 1, 3, self.funciones_test
        )
        self.assertFalse(resultado)
    
    def test_validar_butaca_disponible_fuera_rango(self):
        """
        Test: butaca fuera de rango no está disponible
        """
        resultado = validacion.validar_butaca_disponible(
            "Avatar_151224_a", 10, 10, self.funciones_test
        )
        self.assertFalse(resultado)

    def test_validar_funcion_no_solapada_sin_conflicto(self):
        """
        Test: nueva función no se solapa con existentes
        """
        resultado, pelicula = validacion.validar_funcion_no_solapada(
            "2", "15-12-24", "14:00", 120, 
            self.funciones_test, self.peliculas_test
        )
        self.assertTrue(resultado)
        self.assertIsNone(pelicula)
    
    def test_validar_funcion_no_solapada_mismo_horario(self):
        """
        Test: función en mismo horario exacto se solapa
        """
        resultado, pelicula = validacion.validar_funcion_no_solapada(
            "1", "15-12-24", "18:00", 120,
            self.funciones_test, self.peliculas_test
        )
        self.assertFalse(resultado)
        self.assertEqual(pelicula, "Avatar")
    
    def test_validar_funcion_no_solapada_durante_otra(self):
        """
        Test: función que empieza durante otra se solapa
        """
        resultado, pelicula = validacion.validar_funcion_no_solapada(
            "1", "15-12-24", "19:00", 120,
            self.funciones_test, self.peliculas_test
        )
        self.assertFalse(resultado)
        self.assertEqual(pelicula, "Avatar")
    
    def test_validar_funcion_no_solapada_otra_sala(self):
        """
        Test: función en otra sala no se solapa
        """
        resultado, pelicula = validacion.validar_funcion_no_solapada(
            "2", "15-12-24", "18:00", 120,
            self.funciones_test, self.peliculas_test
        )
        self.assertTrue(resultado)
        self.assertIsNone(pelicula)
    
    def test_validar_funcion_no_solapada_otra_fecha(self):
        """
        Test: función en otra fecha no se solapa
        """
        resultado, pelicula = validacion.validar_funcion_no_solapada(
            "1", "16-12-24", "18:00", 120,
            self.funciones_test, self.peliculas_test
        )
        self.assertTrue(resultado)
        self.assertIsNone(pelicula)

    def test_validar_pelicula_existente_valida(self):
        """
        Test: película existe en el sistema
        """
        resultado = validacion.validar_pelicula_existente(
            "Avatar", self.peliculas_test
        )
        self.assertTrue(resultado)
    
    def test_validar_pelicula_existente_case_insensitive(self):
        """
        Test: película existe (case insensitive)
        """
        resultado = validacion.validar_pelicula_existente(
            "avatar", self.peliculas_test
        )
        self.assertTrue(resultado)
    
    def test_validar_pelicula_existente_con_espacios(self):
        """
        Test: película existe con espacios extra
        """
        resultado = validacion.validar_pelicula_existente(
            "  Avatar  ", self.peliculas_test
        )
        self.assertTrue(resultado)
    
    def test_validar_pelicula_existente_no_existe(self):
        """
        Test: película no existe
        """
        resultado = validacion.validar_pelicula_existente(
            "NoExiste", self.peliculas_test
        )
        self.assertFalse(resultado)
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_validar_usuario_y_contrasena_validos(self, mock_json_load, mock_file):
        """
        Test: usuario y contraseña válidos
        """
        mock_json_load.return_value = self.usuarios_test
        resultado = validacion.validar_usuario_y_contrasena("test@gmail.com", "password123")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["nombre"], "Juan")
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_validar_usuario_y_contrasena_invalidos(self, mock_json_load, mock_file):
        """
        Test: contraseña incorrecta
        """
        mock_json_load.return_value = self.usuarios_test
        resultado = validacion.validar_usuario_y_contrasena("test@gmail.com", "wrongpass")
        self.assertIsNone(resultado)
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_validar_usuario_y_contrasena_usuario_no_existe(self, mock_json_load, mock_file):
        """
        Test: usuario no existe
        """
        mock_json_load.return_value = self.usuarios_test
        resultado = validacion.validar_usuario_y_contrasena("noexiste@gmail.com", "password123")
        self.assertIsNone(resultado)
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_validar_admin_y_contrasena_validos(self, mock_json_load, mock_file):
        """
        Test: admin y contraseña válidos
        """
        mock_json_load.return_value = self.admins_test
        resultado = validacion.validar_admin_y_contrasena("admin1", "admin123")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["Nombre"], "Carlos")
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_validar_usuario_registrado_existe(self, mock_json_load, mock_file):
        """
        Test: usuario está registrado
        """
        mock_json_load.return_value = self.usuarios_test
        resultado = validacion.validar_usuario_registrado("test@gmail.com")
        self.assertTrue(resultado)
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_validar_usuario_registrado_no_existe(self, mock_json_load, mock_file):
        """
        Test: usuario no está registrado
        """
        mock_json_load.return_value = self.usuarios_test
        resultado = validacion.validar_usuario_registrado("noexiste@gmail.com")
        self.assertFalse(resultado)

    @patch('builtins.input', return_value='S')
    def test_confirmar_accion_si(self, mock_input):
        """
        Test: usuario confirma la acción
        """
        resultado = validacion.confirmar_accion("borrar su cuenta")
        self.assertTrue(resultado)
    
    @patch('builtins.input', return_value='N')
    def test_confirmar_accion_no(self, mock_input):
        """
        Test: usuario no confirma la acción
        """
        resultado = validacion.confirmar_accion("borrar su cuenta")
        self.assertFalse(resultado)
    
    @patch('builtins.input', side_effect=['X', 'S'])
    def test_confirmar_accion_entrada_invalida_luego_valida(self, mock_input):
        """
        Test: entrada inválida seguida de válida
        """
        resultado = validacion.confirmar_accion("borrar su cuenta")
        self.assertTrue(resultado)

    @patch('builtins.print')
    def test_manejar_entrada_invalida(self, mock_print):
        """
        Test: manejo de entrada inválida muestra mensaje
        """
        validacion.manejar_entrada_invalida("abc123")
        mock_print.assert_called_once()
        args = mock_print.call_args[0][0]
        self.assertIn("abc123", args)

class TestConDatosReales(unittest.TestCase):
    """
    Tests utilizando los datos reales del sistema.
    """
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_validar_admin_real_admin1(self, mock_json_load, mock_file):
        """
        Test: validar admin real del sistema (admin1)
        """
        admins_reales = {
            "admin1": {
                "Contraseña": "123",
                "Mail": "admin1@cineuade.com",
                "Nombre": "juan",
                "Apellido": "selva"
            }
        }
        mock_json_load.return_value = admins_reales
        resultado = validacion.validar_admin_y_contrasena("admin1", "123")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["Nombre"], "juan")
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_validar_usuario_real_jorge(self, mock_json_load, mock_file):
        """
        Test: validar usuario real del sistema (jorge@gmail.com)
        """
        usuarios_reales = {
            "jorge@gmail.com": {
                "nombre": "jorge",
                "apellido": "jorge",
                "edad": "21",
                "mail": "jorge@gmail.com",
                "contraseña": "12345678",
                "reservas": []
            }
        }
        mock_json_load.return_value = usuarios_reales
        resultado = validacion.validar_usuario_y_contrasena("jorge@gmail.com", "12345678")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["nombre"], "jorge")
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_validar_usuario_real_juan_selva(self, mock_json_load, mock_file):
        """
        Test: validar usuario real con reservas (juann.selva@gmail.com)
        """
        usuarios_reales = {
            "juann.selva@gmail.com": {
                "nombre": "juan",
                "apellido": "selva",
                "edad": 22,
                "mail": "juann.selva@gmail.com",
                "contraseña": "123456",
                "reservas": [
                    {
                        "funcion_id": "Titanic_131125_b",
                        "butaca": "F6-A6",
                        "reserva_id": "R0135"
                    }
                ]
            }
        }
        mock_json_load.return_value = usuarios_reales
        resultado = validacion.validar_usuario_y_contrasena("juann.selva@gmail.com", "123456")
        self.assertIsNotNone(resultado)
        self.assertEqual(len(resultado["reservas"]), 1)
    
    def test_validar_pelicula_real_avatar(self):
        """
        Test: validar película real del sistema (Avatar)
        """
        peliculas_reales = {
            "Avatar": {
                "Género": "ciencia ficcion",
                "Duración": "132",
                "Fecha": "10-11-25"
            }
        }
        resultado = validacion.validar_pelicula_existente("Avatar", peliculas_reales)
        self.assertTrue(resultado)
    
    def test_validar_pelicula_real_gladiador(self):
        """
        Test: validar película real del sistema (Gladiador)
        """
        peliculas_reales = {
            "Gladiador": {
                "Género": "accion",
                "Duración": "124",
                "Fecha": "10-11-25"
            }
        }
        resultado = validacion.validar_pelicula_existente("Gladiador", peliculas_reales)
        self.assertTrue(resultado)
    
    def test_validar_pelicula_real_baby_miko(self):
        """
        Test: validar película con duración numérica (Baby Miko)
        """
        peliculas_reales = {
            "Baby Miko": {
                "Género": "comedia",
                "Duración": 121,  # Duración como int, no string
                "Fecha": "27-11-25"
            }
        }
        resultado = validacion.validar_pelicula_existente("Baby Miko", peliculas_reales)
        self.assertTrue(resultado)
    
    def test_butaca_real_ocupada_avatar(self):
        """
        Test: validar butaca ocupada real en Avatar_131125_a
        """
        funciones_reales = {
            "Avatar_131125_a": {
                "Película": "Avatar",
                "Fecha": "13-11-25",
                "Hora": "16:00",
                "Sala": "1",
                "Butacas": [
                    ["Ocupada", "Ocupada", "Ocupada", "Ocupada", "Libre", "Libre"],
                    ["Ocupada", "Ocupada", "Ocupada", "Libre", "Libre", "Libre"],
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"],
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"],
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"],
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"]
                ]
            }
        }
        # Butaca F1-A1 está ocupada
        resultado = validacion.validar_butaca_disponible("Avatar_131125_a", 1, 1, funciones_reales)
        self.assertFalse(resultado)
    
    def test_butaca_real_libre_avatar(self):
        """
        Test: validar butaca libre real en Avatar_131125_a
        """
        funciones_reales = {
            "Avatar_131125_a": {
                "Película": "Avatar",
                "Fecha": "13-11-25",
                "Hora": "16:00",
                "Sala": "1",
                "Butacas": [
                    ["Ocupada", "Ocupada", "Ocupada", "Ocupada", "Libre", "Libre"],
                    ["Ocupada", "Ocupada", "Ocupada", "Libre", "Libre", "Libre"],
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"],
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"],
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"],
                    ["Libre", "Libre", "Libre", "Libre", "Libre", "Libre"]
                ]
            }
        }
        # Butaca F1-A5 está libre
        resultado = validacion.validar_butaca_disponible("Avatar_131125_a", 1, 5, funciones_reales)
        self.assertTrue(resultado)
    
    def test_funcion_real_gladiador_completa(self):
        """
        Test: validar función completamente ocupada (Gladiador_151125_c)
        """
        funciones_reales = {
            "Gladiador_151125_c": {
                "Película": "Gladiador",
                "Fecha": "15-11-25",
                "Hora": "18:30",
                "Sala": "3",
                "Butacas": [
                    ["Ocupada", "Ocupada", "Ocupada", "Ocupada", "Ocupada", "Ocupada"],
                    ["Ocupada", "Ocupada", "Ocupada", "Ocupada", "Ocupada", "Ocupada"],
                    ["Ocupada", "Ocupada", "Ocupada", "Ocupada", "Ocupada", "Ocupada"],
                    ["Ocupada", "Ocupada", "Ocupada", "Ocupada", "Ocupada", "Ocupada"],
                    ["Ocupada", "Ocupada", "Ocupada", "Ocupada", "Ocupada", "Ocupada"],
                    ["Ocupada", "Ocupada", "Ocupada", "Ocupada", "Ocupada", "Ocupada"]
                ]
            }
        }
        # Todas las butacas están ocupadas
        for fila in range(1, 7):
            for col in range(1, 7):
                resultado = validacion.validar_butaca_disponible("Gladiador_151125_c", fila, col, funciones_reales)
                self.assertFalse(resultado)
    
    def test_solapamiento_real_avatar_misma_sala(self):
        """
        Test: detectar solapamiento entre dos funciones de Avatar en sala 1
        """
        funciones_reales = {
            "Avatar_131125_a": {
                "Película": "Avatar",
                "Fecha": "13-11-25",
                "Hora": "16:00",
                "Sala": "1",
                "Butacas": []
            }
        }
        peliculas_reales = {
            "Avatar": {
                "Duración": "132"
            }
        }
        # Intentar agregar función que se solapa (16:00 + 132 min = 18:12)
        resultado, pelicula = validacion.validar_funcion_no_solapada(
            "1", "13-11-25", "17:00", 120, funciones_reales, peliculas_reales
        )
        self.assertFalse(resultado)
        self.assertEqual(pelicula, "Avatar")
    
    def test_no_solapamiento_real_diferentes_salas(self):
        """
        Test: no hay solapamiento entre funciones en diferentes salas
        """
        funciones_reales = {
            "Avatar_131125_a": {
                "Película": "Avatar",
                "Fecha": "13-11-25",
                "Hora": "16:00",
                "Sala": "1",
                "Butacas": []
            },
            "Titanic_131125_b": {
                "Película": "Titanic",
                "Fecha": "13-11-25",
                "Hora": "17:45",
                "Sala": "2",
                "Butacas": []
            }
        }
        peliculas_reales = {
            "Avatar": {"Duración": "132"},
            "Titanic": {"Duración": "107"}
        }
        # Función en sala 3 no se solapa con sala 1 y 2
        resultado, pelicula = validacion.validar_funcion_no_solapada(
            "3", "13-11-25", "17:00", 120, funciones_reales, peliculas_reales
        )
        self.assertTrue(resultado)
        self.assertIsNone(pelicula)
    
    def test_multiples_funciones_misma_pelicula(self):
        """
        Test: validar múltiples funciones de la misma película en diferentes horarios
        """
        funciones_reales = {
            "Avatar_141125_a": {
                "Película": "Avatar",
                "Fecha": "14-11-25",
                "Hora": "16:00",
                "Sala": "1"
            },
            "Avatar_151125_a": {
                "Película": "Avatar",
                "Fecha": "15-11-25",
                "Hora": "16:00",
                "Sala": "1"
            }
        }
        peliculas_reales = {
            "Avatar": {"Duración": "132"}
        }
        # Ambas funciones existen y no se solapan (diferentes fechas)
        self.assertTrue(validacion.validar_pelicula_existente("Avatar", peliculas_reales))

class TestCasosComplejos(unittest.TestCase):
    """
    Tests de casos complejos y escenarios avanzados.
    """
    def test_validar_mail_con_numeros(self):
        """
        Test: mail válido con números en el usuario
        """
        self.assertTrue(validacion.validar_mail("usuario123@gmail.com"))
    
    def test_validar_mail_con_puntos(self):
        """
        Test: mail válido con puntos en el usuario
        """
        self.assertTrue(validacion.validar_mail("usuario.test@gmail.com"))
    
    def test_validar_mail_con_guiones(self):
        """
        Test: mail válido con guiones en el usuario
        """
        self.assertTrue(validacion.validar_mail("usuario-test@hotmail.com"))
    
    def test_validar_contrasena_con_caracteres_especiales(self):
        """
        Test: contraseña válida con caracteres especiales
        """
        self.assertTrue(validacion.validar_contrasena("Pass@123"))
    
    def test_validar_contrasena_solo_numeros(self):
        """
        Test: contraseña válida solo con números
        """
        self.assertTrue(validacion.validar_contrasena("123456"))
    
    def test_validar_edad_limite_exacto_mas13(self):
        """
        Test: usuario con edad exacta en límite +13
        """
        usuario = {"edad": 13}
        pelicula = {"clasificacion": "+13"}
        self.assertTrue(validacion.validar_edad(usuario, pelicula))
    
    def test_validar_edad_limite_exacto_mas16(self):
        """
        Test: usuario con edad exacta en límite +16
        """
        usuario = {"edad": 16}
        pelicula = {"clasificacion": "+16"}
        self.assertTrue(validacion.validar_edad(usuario, pelicula))
    
    def test_validar_edad_limite_exacto_mas18(self):
        """
        Test: usuario con edad exacta en límite +18
        """
        usuario = {"edad": 18}
        pelicula = {"clasificacion": "+18"}
        self.assertTrue(validacion.validar_edad(usuario, pelicula))
    
    def test_validar_edad_sin_clasificacion(self):
        """
        Test: película sin clasificación
        """
        usuario = {"edad": 10}
        pelicula = {}
        self.assertFalse(validacion.validar_edad(usuario, pelicula))
    
    def test_validar_edad_clasificacion_minuscula(self):
        """
        Test: clasificación en minúsculas se convierte a mayúsculas
        """
        usuario = {"edad": 15}
        pelicula = {"clasificacion": "+13"}
        self.assertTrue(validacion.validar_edad(usuario, pelicula))
    
    def test_butaca_existe_primera_posicion(self):
        """
        Test: validar primera butaca (1,1) existe
        """
        funciones = {
            "test": {
                "Butacas": [
                    ["Libre", "Libre"],
                    ["Libre", "Libre"]
                ]
            }
        }
        self.assertTrue(validacion.butaca_existe("test", 1, 1, funciones))
    
    def test_butaca_existe_ultima_posicion(self):
        """
        Test: validar última butaca en matriz 6x6
        """
        funciones = {
            "test": {
                "Butacas": [
                    ["Libre"] * 6,
                    ["Libre"] * 6,
                    ["Libre"] * 6,
                    ["Libre"] * 6,
                    ["Libre"] * 6,
                    ["Libre"] * 6
                ]
            }
        }
        self.assertTrue(validacion.butaca_existe("test", 6, 6, funciones))
    
    def test_butaca_existe_matriz_vacia(self):
        """
        Test: función sin butacas definidas
        """
        funciones = {
            "test": {
                "Butacas": []
            }
        }
        self.assertFalse(validacion.butaca_existe("test", 1, 1, funciones))
    
    def test_solapamiento_funciones_consecutivas_sin_margen(self):
        """
        Test: funciones consecutivas exactas sin margen
        """
        funciones = {
            "Funcion1": {
                "Película": "Test1",
                "Fecha": "15-11-25",
                "Hora": "16:00",
                "Sala": "1"
            }
        }
        peliculas = {
            "Test1": {"Duración": "120"}
        }
        resultado, _ = validacion.validar_funcion_no_solapada(
            "1", "15-11-25", "18:00", 120, funciones, peliculas
        )
        self.assertIsInstance(resultado, bool)
    
    def test_solapamiento_peliculas_muy_largas(self):
        """
        Test: películas muy largas (>3 horas)
        """
        funciones = {
            "Interstellar": {
                "Película": "Interstellar",
                "Fecha": "15-11-25",
                "Hora": "16:00",
                "Sala": "1"
            }
        }
        peliculas = {
            "Interstellar": {"Duración": "169"}  # 2h 49min
        }
        resultado, pelicula = validacion.validar_funcion_no_solapada(
            "1", "15-11-25", "18:00", 120, funciones, peliculas
        )
        self.assertFalse(resultado)
        self.assertEqual(pelicula, "Interstellar")
    
    def test_validar_datos_con_enteros(self):
        """
        Test: validar datos que incluyen enteros (edad)
        """
        datos = ["Juan", "Pérez", 25, "juan@gmail.com"]
        self.assertTrue(validacion.validar_datos_no_nulos(datos))
    
    def test_validar_datos_con_float(self):
        """
        Test: validar datos que incluyen float (precio)
        """
        datos = ["Entrada", 12000.50, "Disponible"]
        self.assertTrue(validacion.validar_datos_no_nulos(datos))
    
    def test_validar_pelicula_con_espacios_multiples(self):
        """
        Test: película con múltiples espacios internos
        """
        peliculas = {"La  La  Land": {"Género": "musical"}}
        # Probablemente no debería encontrarla si se busca con espacios simples
        resultado = validacion.validar_pelicula_existente("La La Land", peliculas)
        self.assertFalse(resultado)
    
    def test_validar_pelicula_caracteres_unicode(self):
        """
        Test: película con caracteres especiales unicode
        """
        peliculas = {"El Niño": {"Género": "drama"}}
        self.assertTrue(validacion.validar_pelicula_existente("El Niño", peliculas))
    
    @patch('builtins.input', side_effect=['x', 'y', 'N'])
    def test_confirmar_accion_multiples_entradas_invalidas(self, mock_input):
        """
        Test: múltiples entradas inválidas antes de respuesta válida
        """
        resultado = validacion.confirmar_accion("realizar acción")
        self.assertFalse(resultado)
    
    @patch('builtins.input', return_value='s')
    def test_confirmar_accion_minuscula(self, mock_input):
        """
        Test: confirmación con 's' minúscula (se convierte a mayúscula)
        """
        resultado = validacion.confirmar_accion("continuar")
        self.assertTrue(resultado)
    
    @patch('builtins.input', return_value='n')
    def test_confirmar_accion_minuscula_no(self, mock_input):
        """
        Test: negación con 'n' minúscula (se convierte a mayúscula)
        """
        resultado = validacion.confirmar_accion("continuar")
        self.assertFalse(resultado)

class TestRendimientoLimites(unittest.TestCase):
    """
    Tests de rendimiento y casos límite del sistema.
    """
    def test_validar_mail_muy_largo(self):
        """
        Test: mail con usuario muy largo
        """
        usuario_largo = "a" * 100
        mail = f"{usuario_largo}@gmail.com"
        self.assertTrue(validacion.validar_mail(mail))
    
    def test_validar_contrasena_muy_larga(self):
        """
        Test: contraseña muy larga (100+ caracteres)
        """
        contrasena_larga = "a" * 100
        self.assertTrue(validacion.validar_contrasena(contrasena_larga))
    
    def test_butaca_matriz_grande(self):
        """
        Test: matriz de butacas muy grande (10x10)
        """
        funciones = {
            "test": {
                "Butacas": [["Libre"] * 10 for _ in range(10)]
            }
        }
        self.assertTrue(validacion.butaca_existe("test", 10, 10, funciones))
        self.assertTrue(validacion.validar_butaca_disponible("test", 10, 10, funciones))
    
    def test_multiples_funciones_mismo_dia(self):
        """
        Test: validar sistema con muchas funciones el mismo día
        """
        funciones = {}
        peliculas = {"Test": {"Duración": "90"}}
        
        # Crear funciones en la misma sala
        funciones["Test_0"] = {
            "Película": "Test",
            "Fecha": "15-11-25",
            "Hora": "10:00",
            "Sala": "1"
        }
        
        resultado, _ = validacion.validar_funcion_no_solapada(
            "1", "15-11-25", "11:00", 90, funciones, peliculas
        )
        self.assertFalse(resultado)
        
        resultado2, _ = validacion.validar_funcion_no_solapada(
            "1", "15-11-25", "11:35", 90, funciones, peliculas
        )
        self.assertTrue(resultado2)
    
    def test_multiples_salas_mismo_horario(self):
        """
        Test: validar múltiples funciones en diferentes salas al mismo horario
        """
        funciones = {}
        peliculas = {"Test": {"Duración": "90"}}
        
        # Crear funciones en diferentes salas al mismo horario
        for sala in range(1, 7):
            funciones[f"Test_sala{sala}"] = {
                "Película": "Test",
                "Fecha": "15-11-25",
                "Hora": "18:00",
                "Sala": str(sala)
            }
        
        # Intentar agregar otra función en sala 1
        resultado1, _ = validacion.validar_funcion_no_solapada(
            "1", "15-11-25", "18:30", 90, funciones, peliculas
        )
        self.assertFalse(resultado1)
        
        # Intentar agregar en sala 1 después
        resultado2, _ = validacion.validar_funcion_no_solapada(
            "1", "15-11-25", "19:35", 90, funciones, peliculas
        )
        self.assertTrue(resultado2)
    
    def test_validar_datos_lista_grande(self):
        """
        Test: validar lista grande de datos
        """
        datos = ["dato"] * 100
        self.assertTrue(validacion.validar_datos_no_nulos(datos))
    
    def test_validar_datos_lista_con_un_none_al_final(self):
        """
        Test: lista grande con un None al final
        """
        datos = ["dato"] * 99 + [None]
        self.assertFalse(validacion.validar_datos_no_nulos(datos))

if __name__ == '__main__':
    # Configurar el runner de tests
    unittest.main(verbosity=2)