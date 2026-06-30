from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
import sqlite3
import os
import datetime
import shutil

RUTA_RAIZ = os.path.dirname(os.path.abspath(__file__))
RUTA_DB = os.path.join(RUTA_RAIZ, "BaseDeDatos", "datos.db")
RUTA_MODELOS = os.path.join(RUTA_RAIZ, "ModelosIA")
RUTA_RESPALDOS = os.path.join(RUTA_RAIZ, "Respaldos")
RUTA_ARCHIVOS = os.path.join(RUTA_RAIZ, "Archivos")

def iniciar_bd():
    os.makedirs(os.path.dirname(RUTA_DB), exist_ok=True)
    conn = sqlite3.connect(RUTA_DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS DatosPersonales ())
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL, telefono TEXT, correo TEXT,
        direccion TEXT, fecha_registro TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def crear_respaldo():
    os.makedirs(RUTA_RESPALDOS, exist_ok=True)
    fecha = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    destino = os.path.join(RUTA_RESPALDOS, f"respaldo_{fecha}.db")
    shutil.copy2(RUTA_DB, destino)
    return destino

class GestorMasterS(MDApp):
    dialog = None
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        iniciar_bd()
        return MainScreen()
    def mostrar_dialogo(self, titulo, texto):
        if self.dialog: self.dialog.dismiss()
        self.dialog = MDDialog(title=titulo, text=texto)
        self.dialog.open()

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        layout.add_widget(MDLabel(text="SISTEMA GESTOR CON IA", halign="center", font_style="H4"))
        layout.add_widget(MDLabel(text="100% SIN INTERNET", halign="center", font_style="Caption"))
        btns = [("1. Agregar", self.agregar), ("2. Buscar", self.buscar), ("3. Respaldo", self.respaldo), ("5. Salir", self.salir)]
        for texto, func in btns:
            layout.add_widget(MDRaisedButton(text=texto, on_release=func, size_hint_x=1))
        self.add_widget(layout)
    def agregar(self, *a): MDApp.get_running_app().mostrar_dialogo("Info", "Pantalla Agregar")
    def buscar(self, *a): MDApp.get_running_app().mostrar_dialogo("Info", "Pantalla Buscar")
    def respaldo(self, *a):
        try: ruta = crear_respaldo(); MDApp.get_running_app().mostrar_dialogo("OK", f"Guardado: {ruta}")
        except Exception as e: MDApp.get_running_app().mostrar_dialogo("Error", str(e))
    def salir(self, *a): MDApp.get_running_app().stop()

if __name__ == "__main__": GestorMasterS().run()
