import PyPDF2
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os
from tkinter import ttk

def procesar_carpeta():
    carpeta_seleccionada = filedialog.askdirectory()
    if not carpeta_seleccionada:
        return

    archivos_pdf = obtener_archivos_pdf(carpeta_seleccionada)
    if not archivos_pdf:
        mostrar_mensaje("No se encontraron archivos PDF en la carpeta seleccionada.")
        return

    progress_bar["maximum"] = len(archivos_pdf)
    texto_extraido_total = ""
    for idx, pdf in enumerate(archivos_pdf, 1):
        texto_extraido = extraer_texto(pdf)
        texto_extraido_total += f"Archivo: {os.path.basename(pdf)}\n"
        texto_extraido_total += texto_extraido + "\n\n"
        progress_bar["value"] = idx
        root.update_idletasks()

    mostrar_resultado(texto_extraido_total)
    guardar_texto_en_archivo(texto_extraido_total, carpeta_seleccionada)

def obtener_archivos_pdf(carpeta):
    archivos_pdf = []
    for archivo in os.listdir(carpeta):
        ruta_absoluta = os.path.join(carpeta, archivo)
        if os.path.isfile(ruta_absoluta) and archivo.lower().endswith(".pdf"):
            archivos_pdf.append(ruta_absoluta)
    return archivos_pdf

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
    ventana_resultado.title("Texto Extraído")

    texto_scroll = scrolledtext.ScrolledText(ventana_resultado, width=60, height=20)
    texto_scroll.pack(expand=True, fill="both")
    texto_scroll.insert(tk.END, texto)
    texto_scroll.configure(state="disabled")

def guardar_texto_en_archivo(texto, carpeta):
    archivo_guardado = os.path.join(carpeta, "texto_extraido.txt")
    with open(archivo_guardado, "w", encoding="utf-8") as file:
        file.write(texto)
    mostrar_mensaje(f"El texto extraído se ha guardado en:\n{archivo_guardado}")

def mostrar_mensaje(mensaje):
    messagebox.showinfo("Mensaje", mensaje)

# Crear la ventana principal
root = tk.Tk()
root.title("PDF Text Extractor")

# Marco para la barra de progreso
marco_barra_progreso = ttk.Frame(root)
marco_barra_progreso.pack(pady=20)

# Barra de progreso
progress_bar = ttk.Progressbar(marco_barra_progreso, orient="horizontal", length=300, mode="determinate")
progress_bar.pack()

# Botón para seleccionar y procesar la carpeta
boton_procesar = tk.Button(root, text="Seleccionar Carpeta", command=procesar_carpeta)
boton_procesar.pack(pady=20)

# Iniciar el bucle de la interfaz gráfica
root.mainloop()
