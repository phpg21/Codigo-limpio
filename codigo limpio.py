pip install fpdf
import unittest
from unittest.mock import patch
import io
import datetime
import os
from fpdf import FPDF
import json

usuarios = {}
actividades = []

class Actividad:
    def __init__(self, fecha_hora, supervisor, descripcion, anexos, responsable, clima):
        self.fecha_hora = fecha_hora
        self.supervisor = supervisor
        self.descripcion = descripcion
        self.anexos = anexos
        self.responsable = responsable
        self.clima = clima

    def to_dict(self):
        return {
            "fecha_hora": self.fecha_hora,
            "supervisor": self.supervisor,
            "descripcion": self.descripcion,
            "anexos": self.anexos,
            "responsable": self.responsable,
            "clima": self.clima
        }

def registrar_actividad(supervisor):
    if not supervisor:
        print("Debe iniciar sesión primero.")
        return
    
    fecha_hora = input("Ingrese la fecha y hora de la actividad (YYYY-MM-DD HH:MM): ").strip()
    descripcion = input("Ingrese la descripción de la actividad: ").strip()
    anexos = input("Ingrese los anexos (imágenes o documentos): ").strip()
    responsable = input("Ingrese el responsable de la actividad: ").strip()
    clima = input("Ingrese las condiciones climáticas durante la actividad: ").strip()
    
    if not all([fecha_hora, descripcion, responsable, clima]):
        print("Todos los campos son obligatorios.")
        return
    
    datetime.datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M")
    actividad = Actividad(fecha_hora, supervisor, descripcion, anexos, responsable, clima)
    actividades.append(actividad)
    print("Actividad registrada con éxito.")

def consultar_actividades(usuario):
    if not usuario:
        print("Debe iniciar sesión primero.")
        return
    
    fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ").strip()
    fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ").strip()
    
    if not fecha_inicio or not fecha_fin:
        print("Debe ingresar ambas fechas.")
        return
    
    actividades_en_rango = []
    for actividad in actividades:
        fecha_actividad = datetime.datetime.strptime(actividad.fecha_hora, "%Y-%m-%d %H:%M").date()
        if datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d").date() <= fecha_actividad <= datetime.datetime.strptime(fecha_fin, "%Y-%m-%d").date():
            actividades_en_rango.append(actividad)
    
    if actividades_en_rango:
        for actividad in actividades_en_rango:
            print(actividad.to_dict())
    else:
        print("No se encontraron actividades en el rango de fechas especificado.")

def generar_reporte_pdf(usuario):
    if not usuario:
        print("Debe iniciar sesión primero.")
        return
    
    fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ").strip()
    fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ").strip()
    
    if not fecha_inicio or not fecha_fin:
        print("Debe ingresar ambas fechas.")
        return
    
    actividades_en_rango = []
    for actividad in actividades:
        fecha_actividad = datetime.datetime.strptime(actividad.fecha_hora, "%Y-%m-%d %H:%M").date()
        if datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d").date() <= fecha_actividad <= datetime.datetime.strptime(fecha_fin, "%Y-%m-%d").date():
            actividades_en_rango.append(actividad)
    
    if actividades_en_rango:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        for actividad in actividades_en_rango:
            pdf.cell(200, 10, txt=f"Fecha y hora: {actividad.fecha_hora}", ln=True)
            pdf.cell(200, 10, txt=f"Supervisor: {actividad.supervisor}", ln=True)
            pdf.cell(200, 10, txt=f"Descripción: {actividad.descripcion}", ln=True)
            pdf.cell(200, 10, txt=f"Responsable: {actividad.responsable}", ln=True)
            pdf.cell(200, 10, txt=f"Clima: {actividad.clima}", ln=True)
            pdf.cell(200, 10, txt="-" * 50, ln=True)
        
        pdf.output("reporte_bitacora.pdf")
        print("Reporte generado con éxito.")
    else:
        print("No se encontraron actividades en el rango de fechas especificado.")

def crear_cuenta():
    usuario = input("Ingrese un nombre de usuario: ").strip()
    if not usuario:
        print("El nombre de usuario no puede estar vacío.")
        return
    if usuario in usuarios:
        print("El usuario ya existe.")
        return
    
    contraseña = input("Ingrese una contraseña: ").strip()
    if not contraseña:
        print("La contraseña no puede estar vacía.")
        return
    
    usuarios[usuario] = contraseña
    print("Cuenta creada con éxito.")

def iniciar_sesion():
    usuario = input("Ingrese su nombre de usuario: ").strip()
    if not usuario:
        print("El nombre de usuario no puede estar vacío.")
        return None
    
    contraseña = input("Ingrese su contraseña: ").strip()
    if not contraseña:
        print("La contraseña no puede estar vacía.")
        return None

    if usuario in usuarios and usuarios[usuario] == contraseña:
        print("Inicio de sesión exitoso.")
        return usuario
    else:
        print("Usuario o contraseña incorrectos.")
        return None

def cambiar_contraseña(usuario):
    if usuario not in usuarios:
        print("Error: El usuario no está autenticado.")
        return
    contraseña_actual = input("Ingrese su contraseña actual: ")
    if usuarios[usuario] != contraseña_actual:
        print("Contraseña actual incorrecta.")
        return
    nueva_contraseña = input("Ingrese su nueva contraseña: ")
    if not nueva_contraseña.strip():
        print("La nueva contraseña no puede estar vacía.")
        return
    usuarios[usuario] = nueva_contraseña
    print("Contraseña cambiada con éxito.")

def menu():
    usuario_actual = None

    while True:
        print("\n--- Gestión de Bitácora ---")
        print("1. Crear cuenta")
        print("2. Iniciar sesión")
        print("3. Registrar actividad")
        print("4. Consultar actividades")
        print("5. Generar reporte en PDF")
        print("6. Cambiar contraseña")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_cuenta()
        elif opcion == "2":
            usuario_actual = iniciar_sesion()
        elif opcion == "3":
            if usuario_actual:
                registrar_actividad(usuario_actual)
            else:
                print("Debe iniciar sesión primero.")
        elif opcion == "4":
            if usuario_actual:
                consultar_actividades()
            else:
                print("Debe iniciar sesión primero.")
        elif opcion == "5":
            if usuario_actual:
                generar_reporte_pdf()
            else:
                print("Debe iniciar sesión primero.")
        elif opcion == "6":
            if usuario_actual:
                cambiar_contraseña(usuario_actual)
            else:
                print("Debe iniciar sesión primero.")
        elif opcion == "7":
            break
        else:
            print("Opción no válida.")

# ---------------------------
# Implementación de los 27 casos de prueba
# ---------------------------

class TestBitacora(unittest.TestCase):

    def setUp(self):
        # Reinicia las variables globales antes de cada test.
        usuarios.clear()
        actividades.clear()

    # Caso de prueba #1: Crear cuenta (usuario nuevo)
    def test_1_crear_cuenta_nuevo(self):
        inputs = ["nuevoUsuario", "pass1234"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                crear_cuenta()
                output = fake_out.getvalue()
        self.assertIn("Cuenta creada con éxito.", output)
        self.assertIn("nuevoUsuario", usuarios)
        self.assertEqual(usuarios["nuevoUsuario"], "pass1234")

    # Caso de prueba #2: Crear cuenta (usuario existente)
    def test_2_crear_cuenta_existente(self):
        usuarios["nuevoUsuario"] = "pass1234"
        inputs = ["nuevoUsuario"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                crear_cuenta()
                output = fake_out.getvalue()
        self.assertIn("El usuario ya existe.", output)

    # Caso de prueba #3: Iniciar sesión (credenciales correctas)
    def test_3_iniciar_sesion_correcta(self):
        usuarios["nuevoUsuario"] = "pass1234"
        inputs = ["nuevoUsuario", "pass1234"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                result = iniciar_sesion()
                output = fake_out.getvalue()
        self.assertIn("Inicio de sesión exitoso.", output)
        self.assertEqual(result, "nuevoUsuario")

    # Caso de prueba #4: Iniciar sesión (credenciales incorrectas)
    def test_4_iniciar_sesion_incorrecta(self):
        inputs = ["usuarioInexistente", "claveErronea"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                result = iniciar_sesion()
                output = fake_out.getvalue()
        self.assertIn("Usuario o contraseña incorrectos.", output)
        self.assertIsNone(result)

    # Caso de prueba #5: Registrar actividad (con sesión iniciada)
    def test_5_registrar_actividad_con_sesion(self):
        inputs = ["2025-03-10 10:00", "Revisión de sistemas.", "documento.pdf", "Encargado X", "Soleado"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                registrar_actividad("nuevoUsuario")
                output = fake_out.getvalue()
        self.assertIn("Actividad registrada con éxito.", output)
        self.assertEqual(len(actividades), 1)
        act = actividades[0]
        self.assertEqual(act.fecha_hora, "2025-03-10 10:00")
        self.assertEqual(act.supervisor, "nuevoUsuario")
        self.assertEqual(act.descripcion, "Revisión de sistemas.")

    # Caso de prueba #6: Registrar actividad (sin sesión iniciada)
    def test_6_registrar_actividad_sin_sesion(self):
        # Simular el menú sin haber iniciado sesión (opción 3)
        inputs = ["3", "7"]  # Elegir opción 3 y luego salir
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                menu()
                output = fake_out.getvalue()
        self.assertIn("Debe iniciar sesión primero.", output)

    # Caso de prueba #7: Consultar actividades (rango con resultados)
    def test_7_consultar_actividades_con_resultados(self):
        act = Actividad("2025-03-10 10:00", "nuevoUsuario", "Revisión de sistemas.", "documento.pdf", "Encargado X", "Soleado")
        actividades.append(act)
        inputs = ["2025-03-01", "2025-03-30"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                consultar_actividades()
                output = fake_out.getvalue()
        self.assertIn("Revisión de sistemas.", output)

    # Caso de prueba #8: Consultar actividades (rango sin resultados)
    def test_8_consultar_actividades_sin_resultados(self):
        act = Actividad("2025-03-10 10:00", "nuevoUsuario", "Revisión de sistemas.", "documento.pdf", "Encargado X", "Soleado")
        actividades.append(act)
        inputs = ["2025-04-01", "2025-04-30"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                consultar_actividades()
                output = fake_out.getvalue()
        self.assertIn("No se encontraron actividades en el rango de fechas especificado.", output)

    # Caso de prueba #9: Generar reporte en PDF (con actividades)
    def test_9_generar_reporte_pdf_con_actividades(self):
        act = Actividad("2025-03-10 10:00", "nuevoUsuario", "Revisión de sistemas.", "documento.pdf", "Encargado X", "Soleado")
        actividades.append(act)
        inputs = ["2025-03-01", "2025-03-30"]
        with patch('builtins.input', side_effect=inputs):
            with patch('fpdf.FPDF.output') as mock_output:
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    generar_reporte_pdf()
                    output = fake_out.getvalue()
        self.assertIn("Reporte generado con éxito.", output)
        mock_output.assert_called_with("reporte_bitacora.pdf")

    # Caso de prueba #10: Generar reporte en PDF (sin actividades)
    def test_10_generar_reporte_pdf_sin_actividades(self):
        inputs = ["2025-05-01", "2025-05-30"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                generar_reporte_pdf()
                output = fake_out.getvalue()
        self.assertIn("No se encontraron actividades en el rango de fechas especificado.", output)

    # Caso de prueba #11: Cambiar contraseña (contraseña actual correcta)
    def test_11_cambiar_contraseña_correcta(self):
        usuarios["nuevoUsuario"] = "pass1234"
        inputs = ["pass1234", "nuevaPass456"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                cambiar_contraseña("nuevoUsuario")
                output = fake_out.getvalue()
        self.assertIn("Contraseña cambiada con éxito.", output)
        self.assertEqual(usuarios["nuevoUsuario"], "nuevaPass456")

    # Caso de prueba #12: Cambiar contraseña (contraseña actual incorrecta)
    def test_12_cambiar_contraseña_incorrecta(self):
        usuarios["nuevoUsuario"] = "pass1234"
        inputs = ["passEquivocada"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                cambiar_contraseña("nuevoUsuario")
                output = fake_out.getvalue()
        self.assertIn("Contraseña actual incorrecta.", output)
        self.assertEqual(usuarios["nuevoUsuario"], "pass1234")

    # Caso de prueba #13: Iniciar sesión (usuario vacío)
    def test_13_iniciar_sesion_usuario_vacio(self):
        inputs = ["", "pass1234"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                result = iniciar_sesion()
                output = fake_out.getvalue()
        self.assertIn("Usuario o contraseña incorrectos.", output)
        self.assertIsNone(result)

    # Caso de prueba #14: Iniciar sesión (contraseña vacía)
    def test_14_iniciar_sesion_contraseña_vacia(self):
        usuarios["nuevoUsuario"] = "pass1234"
        inputs = ["nuevoUsuario", ""]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                result = iniciar_sesion()
                output = fake_out.getvalue()
        self.assertIn("Usuario o contraseña incorrectos.", output)
        self.assertIsNone(result)

    # Caso de prueba #15: Registrar actividad (fecha y hora en formato incorrecto)
    def test_15_registrar_actividad_formato_incorrecto(self):
        inputs = ["10-03-2025 10:00", "Revisión de redes.", "anexo.docx", "Responsable Y", "Nublado"]
        with patch('builtins.input', side_effect=inputs):
            with self.assertRaises(ValueError):
                registrar_actividad("nuevoUsuario")

    # Caso de prueba #16: Registrar actividad (fecha/hora vacía)
    def test_16_registrar_actividad_fecha_vacia(self):
        inputs = ["", "Revisión general.", "anexo.png", "Responsable Z", "Soleado"]
        with patch('builtins.input', side_effect=inputs):
            with self.assertRaises(ValueError):
                registrar_actividad("nuevoUsuario")

    # Caso de prueba #17: Registrar actividad (descripción vacía)
    def test_17_registrar_actividad_descripcion_vacia(self):
        inputs = ["2025-03-15 09:00", "", "anexo.jpg", "Encargado X", "Nublado"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                registrar_actividad("nuevoUsuario")
                output = fake_out.getvalue()
        self.assertIn("Actividad registrada con éxito.", output)
        self.assertEqual(len(actividades), 1)
        act = actividades[0]
        self.assertEqual(act.descripcion, "")

    # Caso de prueba #18: Registrar actividad (clima vacío)
    def test_18_registrar_actividad_clima_vacio(self):
        inputs = ["2025-03-16 14:30", "Mantenimiento de equipos.", "fotos.zip", "Encargado Y", ""]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                registrar_actividad("nuevoUsuario")
                output = fake_out.getvalue()
        self.assertIn("Actividad registrada con éxito.", output)
        self.assertEqual(len(actividades), 1)
        act = actividades[0]
        self.assertEqual(act.clima, "")

    # Caso de prueba #19: Consultar actividades (fecha inicio mayor a fecha fin)
    def test_19_consultar_actividades_rango_invertido(self):
        act = Actividad("2025-03-10 10:00", "nuevoUsuario", "Revisión de sistemas.", "documento.pdf", "Encargado X", "Soleado")
        actividades.append(act)
        inputs = ["2025-04-10", "2025-04-01"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                consultar_actividades()
                output = fake_out.getvalue()
        self.assertIn("No se encontraron actividades en el rango de fechas especificado.", output)

    # Caso de prueba #20: Generar reporte en PDF (fecha inicio mayor a fecha fin)
    def test_20_generar_reporte_pdf_rango_invertido(self):
        inputs = ["2025-05-10", "2025-05-01"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                generar_reporte_pdf()
                output = fake_out.getvalue()
        self.assertIn("No se encontraron actividades en el rango de fechas especificado.", output)

    # Caso de prueba #21: Cambiar contraseña (sin iniciar sesión)
    def test_21_cambiar_contraseña_sin_sesion(self):
        # Simular menú: elegir opción "6" sin haber iniciado sesión, luego salir con "7"
        inputs = ["6", "7"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                menu()
                output = fake_out.getvalue()
        self.assertIn("Debe iniciar sesión primero.", output)

    # Caso de prueba #22: Cambiar contraseña (nueva contraseña vacía)
    def test_22_cambiar_contraseña_nueva_vacia(self):
        usuarios["nuevoUsuario"] = "pass1234"
        inputs = ["pass1234", ""]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                cambiar_contraseña("nuevoUsuario")
                output = fake_out.getvalue()
        self.assertIn("Contraseña cambiada con éxito.", output)
        self.assertEqual(usuarios["nuevoUsuario"], "")

    # Caso de prueba #23: Crear cuenta (usuario vacío)
    def test_23_crear_cuenta_usuario_vacio(self):
        inputs = ["", "cualquierPass"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                crear_cuenta()
                output = fake_out.getvalue()
        self.assertIn("Cuenta creada con éxito.", output)
        self.assertIn("", usuarios)
        self.assertEqual(usuarios[""], "cualquierPass")

    # Caso de prueba #24: Crear cuenta (contraseña vacía)
    def test_24_crear_cuenta_contraseña_vacia(self):
        inputs = ["usuarioSinPass", ""]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                crear_cuenta()
                output = fake_out.getvalue()
        self.assertIn("Cuenta creada con éxito.", output)
        self.assertIn("usuarioSinPass", usuarios)
        self.assertEqual(usuarios["usuarioSinPass"], "")

    # Caso de prueba #25: Crear cuenta (caracteres especiales en el usuario)
    def test_25_crear_cuenta_caracteres_especiales(self):
        inputs = ["user!@#", "passEspecial"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                crear_cuenta()
                output = fake_out.getvalue()
        self.assertIn("Cuenta creada con éxito.", output)
        self.assertIn("user!@#", usuarios)
        self.assertEqual(usuarios["user!@#"], "passEspecial")

    # Caso de prueba #26: Registrar actividad (anexo inexistente)
    def test_26_registrar_actividad_anexo_inexistente(self):
        inputs = ["2025-03-20 11:00", "Inspección de seguridad.", "C:/ruta_invalida/foto.png", "Encargado Z", "Ventoso"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                registrar_actividad("nuevoUsuario")
                output = fake_out.getvalue()
        self.assertIn("Actividad registrada con éxito.", output)
        self.assertEqual(len(actividades), 1)
        act = actividades[0]
        self.assertEqual(act.anexos, "C:/ruta_invalida/foto.png")

    # Caso de prueba #27: Iniciar sesión (diferencia de mayúsculas/minúsculas en el usuario)
    def test_27_iniciar_sesion_diferencia_mayusculas(self):
        usuarios["nuevoUsuario"] = "pass1234"
        inputs = ["NUEVOUSUARIO", "pass1234"]
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                result = iniciar_sesion()
                output = fake_out.getvalue()
        self.assertIn("Usuario o contraseña incorrectos.", output)
        self.assertIsNone(result)

    # Caso de prueba #28 crear cuenta
    def test_crear_cuenta_nuevo(self):
        inputs = ["nuevoUsuario", "pass1234"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            crear_cuenta()
            output = fake_out.getvalue()
        self.assertIn("Cuenta creada con éxito.", output)
        self.assertIn("nuevoUsuario", usuarios)

    # Intentar registrar un usuario ya existente    
    def test_crear_cuenta_dos_veces(self):
        usuarios["supervisor1"] = "clave123"
        inputs = ["supervisor1", "otraClave"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            crear_cuenta()
            output = fake_out.getvalue()
        self.assertIn("El usuario ya existe.", output)

    # Crear cuenta sin contraseña
    def test_crear_cuenta_sin_contraseña(self):
        inputs = ["supervisor2", ""]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            crear_cuenta()
            output = fake_out.getvalue()
        self.assertIn("Cuenta creada con éxito.", output)
        
    # Iniciar sesion con credenciales correctas
    def test_iniciar_sesion_correcta(self):
        usuarios["supervisor6"] = "clave123"
        inputs = ["supervisor6", "clave123"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = iniciar_sesion()
            output = fake_out.getvalue()
        self.assertIn("Inicio de sesión exitoso.", output)
        self.assertEqual(result, "supervisor6")

    # Intentar iniciar sesión con un usuario inexistente
    def test_iniciar_sesion_usuario_inexistente(self):
        inputs = ["supervisorNoExiste", "claveCualquiera"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = iniciar_sesion()
            output = fake_out.getvalue()
        self.assertIn("Usuario o contraseña incorrectos.", output)
        self.assertIsNone(result)

    # Intentar iniciar sesión con contraseña vacía
    def test_iniciar_sesion_contraseña_vacia(self):
        usuarios["supervisor7"] = "claveSegura"
        inputs = ["supervisor7", ""]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = iniciar_sesion()
            output = fake_out.getvalue()
        self.assertIn("Usuario o contraseña incorrectos.", output)
        self.assertIsNone(result)

    # Cambiar contraseña con éxito
    def test_cambiar_contraseña_correcta(self):
        usuarios["supervisor8"] = "claveAntigua"
        inputs = ["claveAntigua", "claveNueva"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            cambiar_contraseña("supervisor8")
            output = fake_out.getvalue()
        self.assertIn("Contraseña cambiada con éxito.", output)
        self.assertEqual(usuarios["supervisor8"], "claveNueva")

    # Intentar cambiar la contraseña con la actual incorrecta
    def test_cambiar_contraseña_actual_incorrecta(self):
        usuarios["supervisor9"] = "claveCorrecta"
        inputs = ["claveIncorrecta", "nuevaClave"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            cambiar_contraseña("supervisor9")
            output = fake_out.getvalue()
        self.assertIn("Contraseña actual incorrecta.", output)
        self.assertEqual(usuarios["supervisor9"], "claveCorrecta")

    # Cambiar contraseña a una vacía
    def test_cambiar_contraseña_vacia(self):
        usuarios["supervisor10"] = "claveSegura"
        inputs = ["claveSegura", ""]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            cambiar_contraseña("supervisor10")
            output = fake_out.getvalue()
        self.assertIn("Contraseña cambiada con éxito.", output)
        self.assertEqual(usuarios["supervisor10"], "")

    # Crear cuenta con un nombre de usuario muy largo
    def test_crear_cuenta_nombre_largo(self):
        inputs = ["usuario_muy_largo_para_prueba_1234567890", "claveSegura"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            crear_cuenta()
            output = fake_out.getvalue()
        self.assertIn("Cuenta creada con éxito.", output)
        self.assertIn("usuario_muy_largo_para_prueba_1234567890", usuarios)
    
    # Crear cuenta con caracteres especiales en el usuario
    def test_crear_cuenta_caracteres_especiales(self):
        inputs = ["usuario!@#", "claveEspecial"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            crear_cuenta()
            output = fake_out.getvalue()
        self.assertIn("Cuenta creada con éxito.", output)
        self.assertIn("usuario!@#", usuarios)

    # Crear cuenta con espacios en blanco en el usuario   
    def test_crear_cuenta_espacios_en_blanco(self):
        inputs = [" ", "clave123"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            crear_cuenta()
            output = fake_out.getvalue()
        self.assertIn("Cuenta creada con éxito.", output)
        self.assertIn(" ", usuarios)

    # Intentar iniciar sesión con un usuario vacío
    def test_iniciar_sesion_usuario_vacio(self):
        inputs = ["", "clave123"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = iniciar_sesion()
            output = fake_out.getvalue()
        self.assertIn("Usuario o contraseña incorrectos.", output)
        self.assertIsNone(result)
    
    # Intentar iniciar sesión con una contraseña demasiado larga
    def test_iniciar_sesion_clave_larga(self):
        usuarios["supervisor"] = "clave123"
        inputs = ["supervisor", "clave_muy_larga_para_prueba_1234567890"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = iniciar_sesion()
            output = fake_out.getvalue()
        self.assertIn("Usuario o contraseña incorrectos.", output)
        self.assertIsNone(result)
    
    # Iniciar sesión con usuario y contraseña con caracteres especiales
    def test_iniciar_sesion_caracteres_especiales(self):
        usuarios["supervisor!"] = "clave@#123"
        inputs = ["supervisor!", "clave@#123"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = iniciar_sesion()
            output = fake_out.getvalue()
        self.assertIn("Inicio de sesión exitoso.", output)
        self.assertEqual(result, "supervisor!")

    # Cambiar contraseña con una clave demasiado larga
    def test_cambiar_contraseña_muy_larga(self):
        usuarios["supervisor11"] = "clave123"
        inputs = ["clave123", "clave_muy_larga_para_prueba_1234567890"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            cambiar_contraseña("supervisor11")
            output = fake_out.getvalue()
        self.assertIn("Contraseña cambiada con éxito.", output)
        self.assertEqual(usuarios["supervisor11"], "clave_muy_larga_para_prueba_1234567890")
    
    # Cambiar contraseña con caracteres especiales
    def test_cambiar_contraseña_caracteres_especiales(self):
        usuarios["supervisor12"] = "clave123"
        inputs = ["clave123", "@#$_nuevaClave123"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            cambiar_contraseña("supervisor12")
            output = fake_out.getvalue()
        self.assertIn("Contraseña cambiada con éxito.", output)
        self.assertEqual(usuarios["supervisor12"], "@#$_nuevaClave123")

    # Cambiar contraseña a una vacía
    def test_cambiar_contraseña_vacia(self):
        usuarios["supervisor13"] = "claveSegura"
        inputs = ["claveSegura", ""]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            cambiar_contraseña("supervisor13")
            output = fake_out.getvalue()
        self.assertIn("Contraseña cambiada con éxito.", output)
        self.assertEqual(usuarios["supervisor13"], "")

    # Intentar crear una cuenta con un usuario vacío
    def test_crear_cuenta_usuario_vacio(self):
        inputs = ["", "clave123"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            crear_cuenta()
            output = fake_out.getvalue()
        self.assertIn("El nombre de usuario no puede estar vacío.", output)
    
    # Intentar crear una cuenta con una contraseña vacía
    def test_crear_cuenta_contraseña_vacia(self):
        inputs = ["usuarioPrueba", ""]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            crear_cuenta()
            output = fake_out.getvalue()
        self.assertIn("La contraseña no puede estar vacía.", output)
    
    # Intentar crear una cuenta con un usuario ya existente
    def test_crear_cuenta_usuario_existente(self):
        usuarios["usuarioPrueba"] = "clave123"
        inputs = ["usuarioPrueba", "otraClave"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            crear_cuenta()
            output = fake_out.getvalue()
        self.assertIn("El usuario ya existe.", output)

    # Intentar iniciar sesión con un usuario vacío
    def test_iniciar_sesion_usuario_vacio(self):
        inputs = ["", "clave123"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = iniciar_sesion()
            output = fake_out.getvalue()
        self.assertIn("El nombre de usuario no puede estar vacío.", output)
        self.assertIsNone(result)
    
    # Intentar iniciar sesión con una contraseña vacía
    def test_iniciar_sesion_contraseña_vacia(self):
        usuarios["usuarioPrueba"] = "clave123"
        inputs = ["usuarioPrueba", ""]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = iniciar_sesion()
            output = fake_out.getvalue()
        self.assertIn("La contraseña no puede estar vacía.", output)
        self.assertIsNone(result)
    
    # Intentar iniciar sesión con credenciales incorrectas
    def test_iniciar_sesion_credenciales_incorrectas(self):
        usuarios["usuarioPrueba"] = "clave123"
        inputs = ["usuarioPrueba", "claveIncorrecta"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = iniciar_sesion()
            output = fake_out.getvalue()
        self.assertIn("Usuario o contraseña incorrectos.", output)
        self.assertIsNone(result)

    # Intentar cambiar la contraseña sin estar autenticado
    def test_cambiar_contraseña_usuario_no_autenticado(self):
        inputs = ["clave123", "nuevaClave"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            cambiar_contraseña("usuarioInexistente")
            output = fake_out.getvalue()
        self.assertIn("Debe iniciar sesión primero.", output)

    # Intentar cambiar la contraseña con la actual incorrecta
    def test_cambiar_contraseña_actual_incorrecta(self):
        usuarios["usuarioPrueba"] = "clave123"
        inputs = ["claveIncorrecta", "nuevaClave"]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            cambiar_contraseña("usuarioPrueba")
            output = fake_out.getvalue()
        self.assertIn("Contraseña actual incorrecta.", output)
    
    # Intentar cambiar la contraseña con una nueva vacía
    def test_cambiar_contraseña_nueva_vacia(self):
        usuarios["usuarioPrueba"] = "clave123"
        inputs = ["clave123", ""]
        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            cambiar_contraseña("usuarioPrueba")
            output = fake_out.getvalue()
        self.assertIn("La nueva contraseña no puede estar vacía.", output)


if __name__ == '__main__':
    #unittest.main(argv=[''], exit=False)
    menu()


