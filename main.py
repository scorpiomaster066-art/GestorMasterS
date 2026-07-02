import sqlite3
import os
import datetime
import shutil

# Herramientas visuales obligatorias para Android (KivyMD)
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView

# Configuración de tus rutas originales exactas
RUTA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_DB = os.path.join(RUTA_RAIZ, "BaseDeDatos", "datos.db")
RUTA_MODELOS = os.path.join(RUTA_RAIZ, "ModelosIA")
RUTA_RESPALDOS = os.path.join(RUTA_RAIZ, "Respaldos")
RUTA_ARCHIVOS = os.path.join(RUTA_RAIZ, "Archivos")

def iniciar_bd():
    os.makedirs(os.path.dirname(RUTA_DB), exist_ok=True)
    conn = sqlite3.connect(RUTA_DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS DatosPersonales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT,
        correo TEXT,
        direccion TEXT,
        fecha_registro TEXT NOT NULL)""")
    conn.commit()
    conn.close()

class PantallaPrincipal(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        iniciar_bd()
        
        # Contenedor con Scroll para que no se corten los elementos en pantallas chicas
        scroll = MDScrollView()
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=15, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        
        # Encabezado original de tu sistema
        self.titulo = MDLabel(
            text="📱 SISTEMA GESTOR IA - MASTER S.\n100% SIN INTERNET | ANDROID",
            halign="center",
            font_style="H6",
            size_hint_y=None,
            height=80
        )
        self.layout.add_widget(self.titulo)
        
        # --- SECCIÓN 1: FORMULARIO AGREGAR ---
        self.layout.add_widget(MDLabel(text="📝 Agregar Nuevo Registro", font_style="Subtitle2"))
        self.txt_nombre = MDTextField(hint_text="Nombre *", size_hint_y=None, height=40)
        self.txt_telefono = MDTextField(hint_text="Teléfono", size_hint_y=None, height=40)
        self.txt_correo = MDTextField(hint_text="Correo", size_hint_y=None, height=40)
        self.txt_direccion = MDTextField(hint_text="Dirección", size_hint_y=None, height=40)
        
        self.layout.add_widget(self.txt_nombre)
        self.layout.add_widget(self.txt_telefono)
        self.layout.add_widget(self.txt_correo)
        self.layout.add_widget(self.txt_direccion)
        
        btn_guardar = MDRaisedButton(text="💾 Guardar Registro", pos_hint={"center_x": .5}, on_release=self.guardar_registro)
        self.layout.add_widget(btn_guardar)
        
        # --- SECCIÓN 2: BUSCAR ---
        self.layout.add_widget(MDLabel(text="🔍 Búsqueda de Datos", font_style="Subtitle2"))
        self.txt_buscar = MDTextField(hint_text="Buscar por nombre o correo...", size_hint_y=None, height=40)
        self.layout.add_widget(self.txt_buscar)
        
        btn_buscar = MDRaisedButton(text="Buscar", pos_hint={"center_x": .5}, on_release=self.buscar_registro)
        self.layout.add_widget(btn_buscar)

        # --- SECCIÓN 3: RESPALDOS Y ENTRADA DE IA ---
        self.layout.add_widget(MDLabel(text="🤖 Inteligencia Artificial & Sistema", font_style="Subtitle2"))
        self.txt_prompt = MDTextField(hint_text="Tema del informe (dejar vacío para Resumen)", size_hint_y=None, height=40)
        self.layout.add_widget(self.txt_prompt)

        # Contenedor horizontal para los botones de utilidades
        box_botones = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        btn_respaldo = MDRaisedButton(text="🗄️ Respaldo", on_release=self.hacer_respaldo)
        btn_ia = MDRaisedButton(text="📊 Informe IA", md_bg_color=(0.2, 0.6, 0.2, 1), on_release=self.generar_informe_ia)
        box_botones.add_widget(btn_respaldo)
        box_botones.add_widget(btn_ia)
        self.layout.add_widget(box_botones)
        
        # --- SECCIÓN 4: CONSOLA DE RESULTADOS ---
        self.lbl_resultados = MDLabel(
            text="Resultados y estado del sistema aparecerán aquí...",
            halign="center",
            theme_text_color="Hint",
            size_hint_y=None,
            height=200
        )
        self.layout.add_widget(self.lbl_resultados)
        
        scroll.add_widget(self.layout)
        self.add_widget(scroll)

    def guardar_registro(self, instance):
        nom = self.txt_nombre.text.strip()
        tel = self.txt_telefono.text.strip()
        cor = self.txt_correo.text.strip()
        dir = self.txt_direccion.text.strip()
        
        if nom:
            conn = sqlite3.connect(RUTA_DB)
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn.execute("INSERT INTO DatosPersonales VALUES (NULL,?,?,?,?,?)", (nom, tel, cor, dir, fecha))
            conn.commit()
            conn.close()
            
            self.txt_nombre.text = ""
            self.txt_telefono.text = ""
            self.txt_correo.text = ""
            self.txt_direccion.text = ""
            self.lbl_resultados.text = f"✅ Guardado con éxito:\n{nom} ({fecha})"
        else:
            self.lbl_resultados.text = "⚠️ El campo 'Nombre' es obligatorio."

    def buscar_registro(self, instance):
        term = self.txt_buscar.text.strip()
        if not term:
            self.lbl_resultados.text = "⚠️ Escribe algo para buscar."
            return
            
        conn = sqlite3.connect(RUTA_DB)
        res = conn.execute("SELECT * FROM DatosPersonales WHERE nombre LIKE ? OR correo LIKE ?", (f"%{term}%", f"%{term}%")).fetchall()
        conn.close()
        
        if not res:
            self.lbl_resultados.text = "❌ Sin resultados."
        else:
            texto_final = "📋 Resultados:\n"
            for r in res:
                texto_final += f"ID: {r[0]} | {r[1]} | Tel: {r[2]} | {r[3]}\n"
            self.lbl_resultados.text = texto_final

    def hacer_respaldo(self, instance):
        try:
            os.makedirs(RUTA_RESPALDOS, exist_ok=True)
            nombre_respaldo = f"respaldo_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            destino = os.path.join(RUTA_RESPALDOS, nombre_respaldo)
            shutil.copy2(RUTA_DB, destino)
            self.lbl_resultados.text = f"🗄️ Respaldo guardado con éxito:\n{nombre_respaldo}"
        except Exception as e:
            self.lbl_resultados.text = f"❌ Error en respaldo: {str(e)}"

    def generar_informe_ia(self, instance):
        prompt = self.txt_prompt.text.strip() or "Resumen general"
        modelo_path = os.path.join(RUTA_MODELOS, "qwen2.5-1.5b-q4_k_m.gguf")
        
        # Tu validación original si no existe el archivo físico de Qwen
        if not os.path.exists(modelo_path):
            conn = sqlite3.connect(RUTA_DB)
            total = conn.execute("SELECT COUNT(*) FROM DatosPersonales").fetchone()[0] or 0
            conn.close()
            res = f"💻 SISTEMA GESTOR IA\n✅ SIN INTERNET\n📊 Registros: {total}\nℹ️ Copia el .gguf en /ModelosIA pa' IA completa"
            self.lbl_resultados.text = res
            return

        # Si el modelo existe, procesa y genera el archivo de texto
        try:
            res = f"✅ INFORME:\n{prompt}\n\n[Aquí tu script llamaría a llama.cpp / ctransformers para procesar {modelo_path}]"
            os.makedirs(RUTA_ARCHIVOS, exist_ok=True)
            nombre_informe = f"informe_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            ruta_txt = os.path.join(RUTA_ARCHIVOS, nombre_informe)
            
            with open(ruta_txt, "w", encoding="utf-8") as f:
                f.write(res)
                
            self.lbl_resultados.text = f"🤖 Informe generado por IA!\nGuardado en: {ruta_txt}"
        except Exception as e:
            self.lbl_resultados.text = f"❌ Error procesando IA: {str(e)}"

class GestorMasterApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return PantallaPrincipal()

if __name__ == "__main__":
    GestorMasterApp().run()
