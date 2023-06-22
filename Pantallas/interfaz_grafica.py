import customtkinter as ctk
import pandas as pd
from tabulate import tabulate as tab

# configuraciones globales de la interfaz
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class principal:
    # ruta de donde se extraera el archivo con la informacion
    path = ""
    nombres_columnas = []
    dataframe = pd.DataFrame()

    def __init__(self):
        # creacion de la ventana principal
        self.root = ctk.CTk()
        self.root.title("Anonimizer - Grupo #3")
        self.root.geometry("600x500")
        self.root.resizable(False, False)  # no permite redimensionar

        # añadimos el contenido de esta ventana
        self.marco = ctk.CTkFrame(self.root)
        self.marco.pack(padx=10, pady=25)

        # creacion de la parte de escoger el archivo
        # titulo
        ctk.CTkLabel(self.marco, text="Ruta del archivo", width=580,
                     anchor="w", padx="10").grid(row=0, column=0, columnspan=3)

        # aca ingresaremos la ruta
        self.entrada = ctk.CTkEntry(self.marco, width=380)
        self.entrada.grid(row=1, column=0)

        # boton para comprobar que exista el archivo
        self.boton_envio = ctk.CTkButton(
            self.marco, text="Comprobar", command=lambda: self.escoger_archivo(), width=60 )
        self.boton_envio.grid(row=1, column=1)

        # boton para comprobar que exista el archivo
        self.boton_limpiar_ruta = ctk.CTkButton(
            self.marco, text="Limpiar", command=lambda: self.limpiar_ruta(), width=60 )
        self.boton_limpiar_ruta.grid(row=1, column=2)

        # este label mostrara el resultado de la comprobacion
        self.label_resul_archivo = ctk.CTkLabel(
            self.marco, text="", text_color="green", width=580, anchor="w", padx="10")
        self.label_resul_archivo.grid(row=2, column=0, columnspan=3)

        self.boton_vista_previa = ctk.CTkButton(self.marco, text="Cargar vista previa del archivo", command=lambda: self.abrir_vista_previa(
        ), width=560, state="disabled")
        self.boton_vista_previa.grid(row=3, column=0, columnspan=3)

        ctk.CTkLabel(self.marco, text="", width=580,
                     anchor="w", padx="10").grid(row=4, column=0, columnspan=3)
        
        # Bucle de ejecución
        self.root.mainloop()

    # prod para limpiar la ruta
    def limpiar_ruta(self):
        self.entrada.delete(0, ctk.END)
    # prod para escoger el archivo

    def escoger_archivo(self):
        self.path = self.entrada.get()

        if (self.path == None or self.path == ""):
            self.label_resul_archivo.configure(
                text="Llene la ruta antes de comprobar", text_color="red")
            self.entrada.focus()
        else:
            try:
                # intentamos cargar el archivo de la ruta selecionada
                datos_excel = pd.read_excel(
                    self.path, sheet_name='NOVENO 2022', nrows=None)

                # Obtener la primera fila del DataFrame como nombres de columnas
                self.nombres_columnas = list(datos_excel.columns)

                # Crear un nuevo DataFrame con los datos del Excel
                self.dataframe = pd.DataFrame(
                    datos_excel.values, columns=self.nombres_columnas)

                print(tab(self.dataframe, headers=self.nombres_columnas))
                self.label_resul_archivo.configure(
                    text="El archivo escogido se ha encontrado exitosamente", text_color="green")

                self.boton_vista_previa.configure(state="normal")
            except:
                self.label_resul_archivo.configure(
                    text="El archivo indicado no existe o no es de formato excel", text_color="red")
                self.entrada.focus()
                self.boton_vista_previa.configure(state="disabled")

    def abrir_vista_previa(self):
        self.root.destroy()
        vp = vistaPrevia(path=self.path)


class vistaPrevia:
    
    def __init__(self, path):

        # creacion de la ventana principal
        self.root = ctk.CTk()
        self.root.title("Vista Previa - Data")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)  # no permite redimensionar

        self.root.mainloop()
