import customtkinter as ctk
import pandas as pd
import threading
import os

# configuraciones globales de la interfaz
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# clase que crea la pantalla principal


class principal:

    path = ""  # ruta de donde se extraera el archivo con la informacion
    nombres_columnas = []  # contendra las cabeceras de la hoja de calculo
    dataframe = pd.DataFrame()  # contendra la data extraida de la hoja de calculo

    def __init__(self, path):
        # creacion de la ventana principal
        self.root = ctk.CTk()
        self.root.title("Anonimizer - Grupo #3")
        self.root.geometry("600x500")
        self.root.resizable(False, False)  # no permite redimensionar

        #seccion de escoger archivo        
        self.interfaz_escoger_archivo()
        
        # seccion lista de las columnas
        self.interfaz_columnas_lista()

        #comprobacion especial por si regresamos de la ventana de vista previa
        if path != "":
            self.entrada.insert(0, path)
            self.escoger_archivo()
        
        # Bucle de ejecución
        self.root.mainloop()
        
    #prod que creara la interfaz para escoger archivo
    def interfaz_escoger_archivo(self):
        # añadimos el contenido de esta ventana
        self.marco = ctk.CTkFrame(self.root)
        self.marco.pack(padx=10, pady=10)

        # creacion de la parte de escoger el archivo
        # titulo
        ctk.CTkLabel(self.marco, text="Ruta del archivo", width=580,
                     anchor="w", padx="10").grid(row=1, column=0, columnspan=3)

        # aca ingresaremos la ruta
        self.entrada = ctk.CTkEntry(self.marco, width=380)
        self.entrada.grid(row=2, column=0)

        # boton para comprobar que exista el archivo
        self.boton_envio = ctk.CTkButton(
            self.marco, text="Comprobar", command=lambda: self.escoger_archivo(), width=60)
        self.boton_envio.grid(row=2, column=1)

        # boton para comprobar que exista el archivo
        self.boton_limpiar_ruta = ctk.CTkButton(
            self.marco, text="Limpiar", command=lambda: self.limpiar_ruta(), width=60)
        self.boton_limpiar_ruta.grid(row=2, column=2)

        # este label mostrara el resultado de la comprobacion
        self.label_resul_archivo = ctk.CTkLabel(
            self.marco, text="", text_color="green", width=580, anchor="w", padx="10")
        self.label_resul_archivo.grid(row=3, column=0, columnspan=3)

        # boton que mostrara la vista previa
        self.boton_vista_previa = ctk.CTkButton(self.marco, text="Cargar vista previa del archivo", command=lambda: self.abrir_vista_previa(
        ), width=560, state="disabled")
        self.boton_vista_previa.grid(row=4, column=0, columnspan=3, pady="10")

    def interfaz_columnas_lista(self):
    
        #marco que tendra la lista
        self.marco_columnas = ctk.CTkFrame(self.root)
        self.marco_columnas.pack(padx=10, pady=10)
        
        # widget que permite el sclor por si la lista supera el tamaño
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.marco_columnas, width=560, fg_color="transparent", orientation="vertical")
        self.scrollable_frame.pack( expand=True)
        
    # prod para limpiar la ruta
    def limpiar_ruta(self):
        self.entrada.delete(0, ctk.END)
        self.boton_vista_previa.configure(state="disabled")
        self.label_resul_archivo.configure(text="")
        
    # prod para escoger el archivo
    def escoger_archivo(self):
        self.path = self.entrada.get()

        if (self.path == None or self.path == ""):
            self.label_resul_archivo.configure(
                text="Llene la ruta antes de comprobar", text_color="red")
            self.entrada.focus()
            self.boton_vista_previa.configure(state="disabled")
        else:
            try:
                # intentamos cargar el archivo de la ruta selecionada
                datos_excel = pd.read_excel(
                    self.path, nrows=None)

                # Obtener la primera fila del DataFrame como nombres de columnas
                self.nombres_columnas = list(datos_excel.columns)

                # Crear un nuevo DataFrame con los datos del Excel
                self.dataframe = pd.DataFrame(
                    datos_excel.values, columns=self.nombres_columnas)

                self.label_resul_archivo.configure(
                    text="El archivo escogido se ha encontrado exitosamente", text_color="green")

                self.boton_vista_previa.configure(state="normal")                
            except:
                self.label_resul_archivo.configure(
                    text="El archivo indicado no existe o no es de formato excel", text_color="red")
                self.entrada.focus()
                self.boton_vista_previa.configure(state="disabled")

    #prod que abrira la vista previa
    def abrir_vista_previa(self):
        self.root.destroy()
        vp = vistaPrevia(data=self.dataframe, cabeceras=self.nombres_columnas,
                         path=self.path)

# clase que crea la pantalla de las vista previa de un archivo


class vistaPrevia:
    nombre_archivo = ""
    path = ""
    def __init__(self, data, cabeceras, path):
        # obtenemos el nombre del archivo
        self.path = path
        self.nombre_archivo = os.path.basename(self.path)
        
        self.root = ctk.CTk()
        self.root.geometry("1000x650")
        self.root.resizable(False, False)
        self.root.title("Vista Previa - '"+self.nombre_archivo+"' - ")

        # inicializamos las variables con los parametros recibidos de la pantalla principal
        self.cabeceras = cabeceras
        self.data = data

        self.etiquetas_creadas = False

        # Iniciar el proceso de carga de datos en segundo plano
        self.cargar_datos_thread = threading.Thread(target=self.cargar_datos)
        self.cargar_datos_thread.start()

        self.root.mainloop()

    def cargar_datos(self):
        # Obtener las dimensiones del dataframe
        num_filas, num_columnas = self.data.shape

        # actulizamos el titulo de la ventana con la informacion del archivo seleccionado
        self.root.title(self.root.title() + "" + str(num_filas) +
                        " filas, "+str(num_columnas)+" columnas")

        # widget que permite el scroll cuando nustra vista previa sobrepasa el ancho del formulario
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.root, width=1000, height=568, fg_color="transparent", orientation="horizontal")
        self.scrollable_frame.pack( expand=True)

        # dentro de ests widget se crearan todos los widgets de la vista previa
        self._frame = ctk.CTkFrame(
            self.scrollable_frame, width=1000, height=568)
        self._frame.pack(fill='both', expand=True)
        
        self.boton_regresar = ctk.CTkButton(
            self.root, text="Regresar", command=lambda: self.regresar_principal(), width=200)
        self.boton_regresar.pack(pady="5")


        # la vista previa solo cargara maximo 20 registros
        if num_filas > 18:
            num_filas = 18

        # Crear etiquetas para las cabeceras si aún no se han creado
        if not self.etiquetas_creadas:
            for i, cabecera in enumerate(self.cabeceras):
                etiqueta = ctk.CTkLabel(self._frame, text=cabecera)
                etiqueta.grid(row=0, column=i)

        # Mostrar los datos en cuadros de texto
        for i in range(num_filas):
            for j in range(num_columnas):
                # Obtener el valor del dataframe
                valor = str(self.data.iloc[i, j])

                # Utilizar el método 'after' para que la creación de los cuadros de texto se realice en el hilo principal
                self.root.after(0, self.crear_cuadro_texto, valor, i+1, j)

        # Indicar que las etiquetas ya se han creado
        self.etiquetas_creadas = True

    # funcion que creara los cuadros de texto con el valor de celda celda de la hoja de datos
    def crear_cuadro_texto(self, valor, fila, columna):
        cuadro_texto = ctk.CTkEntry(self._frame, width=250, font=('Arial', 12))
        cuadro_texto.insert(0, valor)
        cuadro_texto.grid(row=fila, column=columna, pady=1, padx=1)
        
    def regresar_principal(self):
        self.root.destroy()
        hm = principal(path=self.path)   
