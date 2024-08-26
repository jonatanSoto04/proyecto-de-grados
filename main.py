import base64
import ctypes
from io import BytesIO
import io
import json
import tkinter as tk
from tkinter import ttk, Menu, Frame, Button, Label, StringVar, filedialog, messagebox, PhotoImage
from pyfingerprint.pyfingerprint import PyFingerprint
from PIL import Image, ImageTk

funciones = {}

# Función para iniciar el escaneo de huellas
def inicioescaner():
    try:
        # funciones de ftrScanAPI.dll
        # Capturar imagen de huella usando funciones de ftrScanAPI.dll   
        # Mostrar mensaje de éxito
        messagebox.showinfo("Resultado", "Huella escaneada correctamente.")
        # procesar la imagen capturada y mostrarla
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo escanear la huella.\n{str(e)}")
        
# Función para mostrar la imagen escaneada en el cuadro seleccionado
def mostrar_imagen(image_path, label):
    try:
        img = Image.open(image_path)
        width = label.winfo_width()
        height = label.winfo_height()
        img = img.resize((width, height), Image.LANCZOS)

        img_tk = ImageTk.PhotoImage(img)
        label.config(image=img_tk)
        label.image = img_tk  

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir la imagen: {str(e)}")
    
# Función para escanear huella rodada
def escanear_huella_rodada():
    try:
        # Inicializa
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)  
        if not f.verifyPassword():
            raise ValueError('La contraseña del escáner no es válida')

        print("Coloca tu dedo y rueda sobre el escáner...")

        # Espera a que el dedo sea detectado
        while not f.readImage():
            pass

        f.convertImage(0x01)

        print("Huella rodada escaneada con éxito.")
        messagebox.showinfo("Resultado", "Huella rodada escaneada con éxito.")

    except Exception as e:
        print(f"Error al escanear la huella rodada: {str(e)}")
        messagebox.showerror("Error", f"No se pudo escanear la huella rodada.\n{str(e)}")
    
# Función para escanear huella plana
def escanear_huella_plana():
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)  # Ajustar el puerto y configuraciones según tu escáner

        if not f.verifyPassword():
            raise ValueError('La contraseña del escáner no es válida')

        print("Coloca tu dedo plano sobre el escáner...")

        # Espera a que el dedo sea detectado
        while not f.readImage():
            pass

        f.convertImage(0x01)

        print("Huella plana escaneada con éxito.")
        messagebox.showinfo("Resultado", "Huella plana escaneada con éxito.")

    except Exception as e:
        print(f"Error al escanear la huella plana: {str(e)}")
        messagebox.showerror("Error", f"No se pudo escanear la huella plana.\n{str(e)}")
        
# Función para manejar el cambio de opción
def seleccionar_opcion(*args):
    opcion_seleccionada = opcion.get()
    if opcion_seleccionada == "Huella rodada":
        escanear_huella_rodada()
    elif opcion_seleccionada == "Huella plana":
        escanear_huella_plana()
    else:
        messagebox.showwarning("Advertencia", f"Opción '{opcion_seleccionada}' no reconocida.")

# Función para seleccionar una imagen y mostrarla en el cuadro
def seleccionar_imagen(label):
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")],
        title="Seleccionar archivo de imagen"
    )
    if file_path:
        try:
            img = Image.open(file_path)
            # Obtener imagen (label)
            width = label.winfo_width()
            height = label.winfo_height()
            img = img.resize((width, height), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)

            # Mostrar la imagen en el cuadro
            label.config(image=img)
            label.image = img # Guardar la referencia
            label.grid() 

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la imagen: {str(e)}")

# Función para crear un nuevo archivo de imagen
def nuevo_archivo():
    if selected_label is None:
        messagebox.showwarning("Advertencia", "Por favor, seleccione un cuadro de imagen primero.")
        return

    seleccionar_imagen(selected_label)

def seleccionar_cuadro(event, label):
    global selected_label

    for widget in image_frame.winfo_children():
        if isinstance(widget, Frame):
            for child in widget.winfo_children():
                if isinstance(child, Label):
                    child.config(relief='solid', bd=1)

    selected_label = label
    selected_label.config(relief='solid', bd=2, highlightbackground='black')


# Registrar funciones en el diccionario
funciones['inicioescaner'] = inicioescaner
funciones['mostrar_imagen'] = mostrar_imagen
funciones['escanear_huella_rodada'] = escanear_huella_rodada
funciones['escanear_huella_plana'] =escanear_huella_plana
funciones['seleccionar_opcion'] = seleccionar_opcion
funciones['seleccionar_imagen'] = seleccionar_imagen
funciones['def nuevo_archivo'] = nuevo_archivo
funciones['seleccionar_cuadro'] = seleccionar_cuadro


def guardar_estado():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        title="Guardar estado como"
    )

    if file_path:
        try:
            estado = {
                "root": {
                    "geometry": root.geometry(),
                    "title": root.title(),
                    "grid_rows": [root.grid_rowconfigure(i)['weight'] for i in range(root.grid_size()[1])],
                    "grid_columns": [root.grid_columnconfigure(i)['weight'] for i in range(root.grid_size()[0])]
                },
                "menu": {
                    "file_menu": {
                        "items": [item.cget("label") for item in file_menu.winfo_children()]
                    }
                },
                "left_frame": {
                    "widgets": [
                        {
                            "text": button1.cget("text"),
                            "command": "inicioescaner"
                        },
                        {
                            "text": button2.cget("text"),
                            "command": str(button2.cget("command"))
                        }
                    ]
                },
                "right_frame": {
                    "widgets": []
                },
                "top_frame": {
                    "label_top": {
                        "text": label_top.cget("text"),
                        "row": label_top.grid_info()['row'],
                        "column": label_top.grid_info()['column'],
                        "padx": label_top.grid_info().get("padx", 0),
                        "pady": label_top.grid_info().get("pady", 0)
                    },
                    "dropdown": {
                        "selected_option": opcion.get(),
                        "row": dropdown.grid_info()['row'],
                        "column": dropdown.grid_info()['column'],
                        "padx": dropdown.grid_info().get("padx", 0),
                        "pady": dropdown.grid_info().get("pady", 0)
                    }
                },
                "image_frame": {
                    "frames": []
                }
            }

            for frame in image_frame.winfo_children():
                frame_info = {
                    "row": frame.grid_info()['row'],
                    "column": frame.grid_info()['column'],
                    "widgets": []
                }

                for widget in frame.winfo_children():
                    widget_info = {
                        "text": widget.cget("text"),
                        "row": widget.grid_info()['row'],
                        "column": widget.grid_info()['column']
                    }

                    if hasattr(widget, 'image') and widget.image:
                        image = widget.image
                        pil_image = ImageTk.getimage(image)
                        buffered = BytesIO()
                        pil_image.save(buffered, format="PNG")
                        image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                        widget_info["image_data"] = image_base64

                    frame_info["widgets"].append(widget_info)

                estado["image_frame"]["frames"].append(frame_info)

            with open(file_path, "w") as file:
                json.dump(estado, file, indent=4)

            messagebox.showinfo("Guardado", "El estado de la aplicación se ha guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el estado de la aplicación.\n{str(e)}")

# Función para abrir un archivo de imagen existente
def cargar_estado(file_path):
    global top_frame, dropdown, button1, button2, left_frame, right_frame, image_frame, opcion, file_menu

    try:
        with open(file_path, "r") as file:
            estado = json.load(file)

        # Limpiar los marcos existentes
        for widget in image_frame.winfo_children():
            widget.destroy()
        left_frame.destroy()
        right_frame.destroy()

        # Reconfigurar la ventana principal
        root.geometry(estado["root"]["geometry"])
        root.title(estado["root"]["title"])

        # Recrear los marcos principales
        left_frame = tk.Frame(root, bg='#dce0e6')
        right_frame = tk.Frame(root, bg='white')

        left_frame.grid(row=0, column=0, sticky='ns', padx=10, pady=10)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=20, pady=10)

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=0)
        root.grid_columnconfigure(1, weight=1)

        # Restaurar el menú
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)

        for item in estado["menu"]["file_menu"]["items"]:
            file_menu.add_command(label=item)

        # Restaurar los botones en left_frame
        button1 = tk.Button(left_frame, text=estado["left_frame"]["widgets"][0]["text"],
                            command=lambda: eval(estado["left_frame"]["widgets"][0]["command"]),
                            bg="#B4C8DC",
                            fg="black",
                            font=("Optima", 10),
                            bd=3,
                            relief="groove",
                            activebackground="#829EBA",
                            activeforeground="white")
        button1.pack(pady=10, padx=30)

        button2 = tk.Button(left_frame, text=estado["left_frame"]["widgets"][1]["text"],
                            command=lambda: eval(estado["left_frame"]["widgets"][1]["command"]),
                            bg="#B4C8DC",
                            fg="black",
                            font=("Optima", 10),
                            bd=3,
                            relief="groove",
                            activebackground="#829EBA",
                            activeforeground="white")
        button2.pack(pady=20, padx=30)

        # Restaurar el top_frame
        top_frame = tk.Frame(right_frame, bg="#909eb8")
        top_frame.pack(fill='x', padx=10, pady=10)

        label_top = tk.Label(
            top_frame,
            text=estado["top_frame"]["label_top"]["text"],
            font=("Optima", 10),
            fg="black",
            bg="#9FBBD6",
            width=15,
            height=1
        )
        label_top.grid(row=estado["top_frame"]["label_top"]["row"],
                       column=estado["top_frame"]["label_top"]["column"],
                       padx=estado["top_frame"]["label_top"].get("padx", 0),
                       pady=estado["top_frame"]["label_top"].get("pady", 0))

        # Restaurar dropdown
        opcion.set(estado["top_frame"]["dropdown"]["selected_option"])
        dropdown = ttk.OptionMenu(
            top_frame,
            opcion,
            opcion.get(),
            "Huella rodada",
            "Huella plana",
            command=seleccionar_opcion
        )
        dropdown.grid(row=estado["top_frame"]["dropdown"]["row"],
                      column=estado["top_frame"]["dropdown"]["column"],
                      padx=estado["top_frame"]["dropdown"].get("padx", 0),
                      pady=estado["top_frame"]["dropdown"].get("pady", 0))

        # Restaurar image_frame
        image_frame = tk.Frame(right_frame, bg='white')
        image_frame.pack(fill='both', expand=True, padx=20, pady=20)

        for frame_info in estado["image_frame"]["frames"]:
            row = frame_info["row"]
            column = frame_info["column"]

            new_frame = tk.Frame(image_frame, bg='white')
            new_frame.grid(row=row, column=column, padx=5, pady=10, sticky='nsew')

            for widget_info in frame_info["widgets"]:
                text = widget_info.get("text", "")
                row = widget_info.get("row", 0)
                column = widget_info.get("column", 0)

                if "image_data" in widget_info:
                    image_data = widget_info["image_data"]
                    image = Image.open(io.BytesIO(base64.b64decode(image_data)))
                    photo = ImageTk.PhotoImage(image)
                    label = tk.Label(new_frame, image=photo, text=text)
                    label.image = photo  # Almacenar referencia a la imagen para evitar garbage collection
                    label.grid(row=row, column=column, sticky="nsew")
                else:
                    label = tk.Label(new_frame, text=text)
                    label.grid(row=row, column=column, sticky="nsew")

        # Configurar el grid del image_frame
        for i in range(2):
            image_frame.grid_rowconfigure(i, weight=1)
        for j in range(5):
            image_frame.grid_columnconfigure(j, weight=1)

        # Configurar el grid de cada cuadro de imagen
        for frame in image_frame.winfo_children():
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

    except Exception as e:
        print(f"Error al cargar el estado: {e}")


# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz Lectura de huellas")
root.geometry("800x600")


# Configurar el grid del root
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Crear el menú
menubar = Menu(root)
root.config(menu=menubar)

file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Archivo", menu=file_menu)
file_menu.add_command(label="Nuevo", command=nuevo_archivo)
file_menu.add_command(label="Abrir", command=lambda: cargar_estado(filedialog.askopenfilename()))
file_menu.add_command(label="Guardar", command=guardar_estado)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=root.quit)

# Crear los marcos principales
left_frame = Frame(root, bg='#dce0e6')
right_frame = Frame(root, bg='white')

# Configurar el grid de los marcos principales
right_frame.grid(row=0, column=1, sticky='nsew', padx=20, pady=10)
left_frame.grid(row=0, column=0, sticky='ns', padx=10, pady=10)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)

# Agregar los botones al marco izquierdo
button1 = Button(left_frame, text="Iniciar escaneo", command=inicioescaner,
                 bg="#B4C8DC", 
                 fg="black",   
                 font=("Optima", 10), 
                 bd=3,         
                 relief="groove", 
                 activebackground="#829EBA", 
                 activeforeground="white")
button1.pack(pady=10, padx=30)

button2 = Button(left_frame, text="Guardar BD",
                 bg="#B4C8DC", 
                 fg="black",   
                 font=("Optima", 10), 
                 bd=3,         
                 relief="groove", 
                 activebackground="#829EBA", 
                 activeforeground="white")
button2.pack(pady=20, padx=30)

# Marco superior de la parte derecha
top_frame = Frame(right_frame, bg="#909eb8")
top_frame.pack(fill='x', padx=10, pady=10)

label_top = Label(
    top_frame,
    text="Modelo del escáner",
    font=("Optima", 10),  # Cambia la fuente y el tamaño
    fg="black",  # Color del texto
    bg="#9FBBD6",  # Color de fondo
    width=15,  # Ancho del widget
    height=1   # Altura del widget
)
label_top.grid(row=0, column=0, padx=20)


# Menú desplegable
opcion = StringVar()
opcion.set("Huella rodada")
dropdown = ttk.OptionMenu(top_frame, opcion, opcion.get(), "Huella rodada", "Huella plana", command=seleccionar_opcion)
dropdown.grid(row=0, column=2, padx=10)

# Estilo
style = ttk.Style()
style.configure('TMenubutton', arrowcolor="black")

# Crear un marco 
image_frame = Frame(right_frame, bg='white')
image_frame.pack(fill='both', expand=True, padx=20, pady=20)

# Crear 2 filas de 5 cuadros de imágenes cada una
selected_label = None  
for i in range(2):
    for j in range(5):
        frame = Frame(image_frame, bg='white')
        frame.grid(row=i, column=j, padx=5, pady=10, sticky='nsew')

        label = Label(frame, text=f"Img {i*5+j+1}", bg='#ced6e4', width=15, height=10, relief='solid', bd=0)
        label.grid(row=0, column=0, sticky='nsew')  

        label.bind("<Button-1>", lambda event, lbl=label: seleccionar_cuadro(event, lbl))

        text1 = Label(frame, text="Texto 1")
        text1.grid(row=1, column=0, pady=(5, 2))  

        text2 = Label(frame, text="Texto 2")
        text2.grid(row=2, column=0, pady=(2, 5))  

# Configurar el grid del image_frame
for i in range(2):
    image_frame.grid_rowconfigure(i, weight=1)
for j in range(5):
    image_frame.grid_columnconfigure(j, weight=1)

# Configurar el grid de cada cuadro de imagen
for frame in image_frame.winfo_children():
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

root.mainloop()
root.update_idletasks()
root.update()

