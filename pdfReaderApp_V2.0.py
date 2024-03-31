import PyPDF2
import tkinter as tk
from tkinter import filedialog, scrolledtext
import gettext

# Configuración de gettext para cargar las traducciones
locale = "en_US"  # Puedes cambiar a "es_ES" para español
lang = gettext.translation("pdf_text_extractor_gui", localedir="locales", languages=[locale])
lang.install()

def _(s):
    return lang.gettext(s)

def procesar_pdf():
    file_path = filedialog.askopenfilename(filetypes=[(_("PDF files"), "*.pdf")])
    if not file_path:
        return

    texto_extraido = extraer_texto(file_path)
    mostrar_resultado(texto_extraido)

def extraer_texto(pdf_path):
    texto = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            texto += page.extract_text()
    return texto

def mostrar_resultado(texto):
    ventana_resultado = tk.Toplevel(root)
    ventana_resultado.title(_("Extracted Text"))

    texto_scroll = scrolledtext.ScrolledText(ventana_resultado, width=60, height=20)
    texto_scroll.pack(expand=True, fill="both")
    texto_scroll.insert(tk.END, texto)
    texto_scroll.configure(state="disabled")

# Crear la ventana principal
root = tk.Tk()
root.title(_("PDF Text Extractor"))

# Botón para seleccionar y procesar el PDF
boton_procesar = tk.Button(root, text=_("Select PDF"), command=procesar_pdf)
boton_procesar.pack(pady=20)

# Iniciar el bucle de la interfaz gráfica
root.mainloop()
