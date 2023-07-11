import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import pandas as pd
import threading
import os
import hashlib as hs
import openpyxl

# configuraciones globales de la interfaz
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# funcion para centrar las ventanas de la app en la pantalla


def centrar_ventana(ventana):
    ventana.update_idletasks()  # Actualizar la ventana para obtener su tamaño correcto
    ancho_ventana = ventana.winfo_width()
    altura_ventana = ventana.winfo_height()

    # Obtener las dimensiones de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    altura_pantalla = ventana.winfo_screenheight()

    # Calcular las coordenadas para centrar la ventana
    x = (ancho_pantalla - ancho_ventana) // 2
    y = (altura_pantalla - 60 - altura_ventana) // 2

    # Establecer las coordenadas de la ventana
    ventana.geometry(f"+{x}+{y}")

# clase que crea la pantalla principal


class principal:
    # lista de opciones validas para datos sensibles que pueden ser anonimizados
    opciones_faker = ["Nombre", "Apellido", "Nombre Completo",
                      "Direccion", "Correo", "Identificacion", "Telefono"]       

    columnas_selecionadas = []  # lista de las columnas que se anonimizaran
    path = ""  # ruta de donde se extraera el archivo con la informacion
    nombres_columnas = []  # contendra las cabeceras de la hoja de calculo
    dataframe = pd.DataFrame()  # contendra la data extraida de la hoja de calculo

    def __init__(self, path):
        # creacion de la ventana principal
        self.root = ctk.CTk()
        self.root.title("Anonimizer - Grupo #3")
        self.root.geometry("600x600")
        self.root.resizable(False, False)  # no permite redimensionar
        # en caso de intentar cerrar se llamara la funcion de cerrar_anonimizer
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_anonimizer)

        # seccion de escoger archivo
        self.interfaz_escoger_archivo()

        # seccion lista de las columnas
        self.interfaz_columnas_lista()

        # seccion de anonimizacion
        self.interfaz_secion_anonimizacion()

        # comprobacion especial por si regresamos de la ventana de vista previa
        if path != "":
            self.entrada.configure(state="normal")
            self.entrada.insert(0, path)
            self.escoger_archivo()
            self.generar_checkboxes()
            self.operaciones_combobox()
            self.entrada.configure(state="disabled")

        # Bucle de ejecución
        centrar_ventana(self.root)
        self.root.mainloop()

    # prod que creara la interfaz para escoger archivo
    def interfaz_escoger_archivo(self):
        # añadimos el contenido de esta ventana
        self.marco = ctk.CTkFrame(self.root)
        self.marco.pack(padx=10, pady=10)

        # creacion de la parte de escoger el archivo
        # titulo
        ctk.CTkLabel(self.marco, text="Ruta del archivo", width=580,
                     anchor="w", padx="10").grid(row=1, column=0, columnspan=3)

        # aca ingresaremos la ruta
        self.entrada = ctk.CTkEntry(self.marco, width=380, state="disabled")
        self.entrada.grid(row=2, column=0)

        # boton para comprobar que exista el archivo
        self.boton_envio = ctk.CTkButton(
            self.marco, text="Buscar.......", command=lambda: self.abrir_archivo(), width=60)
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
        self.boton_vista_previa.grid(row=4, column=0, columnspan=3, pady="5")

    # prod que creara la interfaz para la lista de columnas
    def interfaz_columnas_lista(self):

        # marco que tendra la lista
        self.marco_columnas = ctk.CTkFrame(self.root)
        self.marco_columnas.pack(padx=10)

        # titulo de la seccion
        ctk.CTkLabel(self.marco_columnas, text="Columnas a Anonimizar", width=580,
                     anchor="w", padx="10", pady="10").pack()

        # widget que permite el sclor por si la lista supera el tamaño
        self.scrollable_frame_columnas = ctk.CTkScrollableFrame(
            self.marco_columnas, width=560, height=100, fg_color="transparent", orientation="vertical", border_width=2)
        self.scrollable_frame_columnas.pack(expand=True, padx=10, pady=10)

    # prod de la seccion donde aplicaremos la tecnica de anonimizacion
    def interfaz_secion_anonimizacion(self):        
        
        # marco principal de esta seccion
        self.marco_prin_anonimizacion = ctk.CTkFrame(self.root, width=560)
        self.marco_prin_anonimizacion.pack(padx=10, pady=10)

        self.marco_op_anonimizacion = ctk.CTkFrame(
            self.marco_prin_anonimizacion, width=560)
        self.marco_op_anonimizacion.grid(
            padx="10", row=1, column=0, columnspan=3)
        # cosas que iran dentro de este marco
        # titulo de la seccion
        ctk.CTkLabel(self.marco_prin_anonimizacion, text="Tecnica de Anonimizacion", width=580,
                     anchor="w", padx="10", pady="20").grid(row=0, column=0, columnspan=3)

        # 1. opcion Eliminacion
        self.opcion_escogida = ctk.StringVar(value=None)
        self.radiobutton_eliminacion = ctk.CTkRadioButton(self.marco_op_anonimizacion, text="Eliminar Columnas",
                                                          variable=self.opcion_escogida, value="op1", width=150, command=lambda: self.operaciones_combobox()).grid(row=1, column=0, padx="18", pady="15")

        # 2. opcion Encriptacion
        self.radiobutton_enriptacion = ctk.CTkRadioButton(self.marco_op_anonimizacion, text="Encriptar Columnas",
                                                          variable=self.opcion_escogida, value="op2", width=150, command=lambda: self.operaciones_combobox()).grid(row=1, column=1, padx="18", pady="15")

        # 3. opcion Sustitucion
        self.radiobutton_sustitucion = ctk.CTkRadioButton(self.marco_op_anonimizacion, text="Sustituir Columnas",
                                                          variable=self.opcion_escogida, value="op3", width=150, command=lambda: self.operaciones_combobox()).grid(row=1, column=2, padx="18", pady="15")

        # boton que guardara el nuevo archivo anonimizado
        self.boton_guardar_anonimizado = ctk.CTkButton(self.marco_prin_anonimizacion, text="Guardar", command=lambda: self.empezar_annimizacion(
        ), width=560, state="normal")
        self.boton_guardar_anonimizado.grid(
            row=4, column=0, columnspan=3, pady="20")
        
        #Objeto con los procedimientos que seran llamados dependiendo de cada tecnica escogida
        self.tecnicas_anonimizacion = {
            "op1": self.eliminar_columnas,
            "op2": self.encriptar_columnas,
            "op3": self.sustituir_columnas
        } 

    # prod para limpiar la ruta
    def limpiar_ruta(self):
        self.path = ""
        self.entrada.configure(state="normal")
        self.entrada.delete(0, ctk.END)
        self.entrada.configure(state="disabled")
        self.boton_vista_previa.configure(state="disabled")
        self.label_resul_archivo.configure(text="")
        self.limpiar_checkbox()

    # abrir dialogo
    def abrir_archivo(self):
        archivo = filedialog.askopenfilename(title="Buscar Archivo")
        if archivo != "" and archivo != None:
            self.limpiar_ruta()
            self.entrada.configure(state="normal")
            self.entrada.insert(0, archivo)
            self.escoger_archivo()
            self.generar_checkboxes()
            self.operaciones_combobox()
            self.entrada.configure(state="disabled")
        else:
            self.limpiar_checkbox()
            self.limpiar_ruta()
            self.label_resul_archivo.configure(
                text="No se escogio ningun archivo", text_color="red")

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
                    text="El archivo se ha escogido exitosamente", text_color="green")

                self.boton_vista_previa.configure(state="normal")
            except:
                self.nombres_columnas.clear()
                self.limpiar_ruta()
                self.label_resul_archivo.configure(
                    text="El archivo indicado no es de formato excel", text_color="red")
                self.entrada.focus()
                self.boton_vista_previa.configure(state="disabled")

    # prod que abrira la vista previa
    def abrir_vista_previa(self):
        resp = messagebox.askquestion(
            "Advertencia", "¿Seguro que desea abrir una vista previa?, tome en cuenta que eso borrara todo progreso en este formulario")

        if resp == "yes":
            self.root.destroy()
            vp = vistaPrevia(data=self.dataframe, cabeceras=self.nombres_columnas,
                             path=self.path)

    # prod para cargar los checkboxs
    def generar_checkboxes(self):
        self.limpiar_checkbox()

        for columna in self.nombres_columnas:
            frame = ctk.CTkFrame(self.scrollable_frame_columnas)
            frame.pack(fill='x', padx=10, pady=5)

            checkbox = ctk.CTkCheckBox(frame, text=columna, width=300)
            checkbox.pack(side='left')

            combobox = ctk.CTkComboBox(
                frame, values=self.opciones_faker, state="disabled", width=200)
            combobox.pack(side='left')

    # limpia los checkboxes
    def limpiar_checkbox(self):
        # de haber ya checkbox estos estan dentro de un CTkFrame por ende destruimos ese control
        for child in self.scrollable_frame_columnas.winfo_children():
            if isinstance(child, ctk.CTkFrame):
                child.destroy()

    # prod que activa o desactiva los combobx dependiendo de que radio este selecionado
    def operaciones_combobox(self):
        estado = "disabled"  # por defecto los radio desactivan los combobox

        # la opcion 3 indica que se escogio sustitucion y esto amerita activar los combobox
        if self.opcion_escogida.get() == "op3":
            estado = "readonly"

        # recorremos los hijos de nuestro frame de scroll
        for child in self.scrollable_frame_columnas.winfo_children():

            # en particular nos interesan los CTkFrame
            if isinstance(child, ctk.CTkFrame):
                # extraemos los hijos de ese CTkframe en formato de lista
                hijos = child.winfo_children()
                # solo hay dos hijos [0=Checkbox, 1=Combobox] y por ende no interesa el 1
                combobox = hijos[1]
                # cambiamos el estado dependiendo de que radio esta seleccionado
                combobox.configure(state=estado)
                # por defecto tendran selecionada la primer opcion
                combobox.set(self.opciones_faker[0])

    # prod que se llamara al intentar cerrar Anonimizer
    def cerrar_anonimizer(self):
        resp = messagebox.askquestion(
            "Advertencia", "¿Seguro que desea cerrar Anonimizer?, tome en cuenta que eso borrara todo progreso en este formulario")

        if resp == "yes":
            self.root.destroy()

    # prods para la anonimizacion
    # prod principal
    def empezar_annimizacion(self):         
             
        if self.path == "":
            messagebox.showerror(message="Selecione un archivo primero", title="Error")  
        elif not self.obtener_columnas_seleccionadas():
            messagebox.showerror(message="Selecione columnas antes de Guardar", title="Error")            
        elif self.opcion_escogida.get() == "":
            messagebox.showerror(message="Selecione una tecnica de Anonimizacion", title="Error") 
        elif not self.escoger_guardado():
            messagebox.showerror(message="Selecione una ruta valida de guardado", title="Error") 
        else :
            #si no hay errores, extraemos el prod que corresponda a la opcion escogida
            tecnica_aplicada = self.tecnicas_anonimizacion.get(self.opcion_escogida.get())
            #coremos ese procedimiento
            tecnica_aplicada()
            #messagebox.showinfo(message="Archivo guardado correctamente", title="Exito")
            
        #print(self.columnas_selecionadas)

    # prod que obtiene que columnas fueron seleccionadas
    def obtener_columnas_seleccionadas(self):
        self.columnas_selecionadas.clear()
        
        #recorremos todos los widgets hijos del frame principal de scroll
        for child in self.scrollable_frame_columnas.winfo_children():
            
            #verificamos que los hijos sean de tipo CTkFrame, ya que dentro de este widget estan los checks
            if isinstance(child, ctk.CTkFrame):
                hijos = child.winfo_children() #para cada uno extraemos la lista de hijos
                check = hijos[0] # los hijos de este Frame son [0=checkbox, 1=combobox], por ende nos interesa el 0

                if check.get() == 1: #el metodo get() retorna 1 si el checkbox esta seleccionado
                    self.columnas_selecionadas.append(check.cget("text")) #añadimos a la lista la columna, que se extrae del texto del check
            
        if len(self.columnas_selecionadas) >= 1:
            return True
        else:
            return False
    
    # prod que escoge la ruta de guardado
    def escoger_guardado(self):
        self.ruta_guardado = ""
        self.ruta_guardado = filedialog.asksaveasfilename(
            title="Guardar Archivo",
            defaultextension=".xlsx",
            filetypes=[("Archivos de Excel", ".xlsx .xls")]
        )

        if self.ruta_guardado:
            return True
        else:
            return False        

    # prod para eliminar columnas
    def eliminar_columnas(self):
        
        data_frame_eliminacion = pd.DataFrame(self.dataframe)

        for columna in self.columnas_selecionadas:
            del data_frame_eliminacion[columna]
            
        
        data_frame_eliminacion.to_excel(self.ruta_guardado, index=False) 
        messagebox.showinfo(message="El archivo se ha guardado correctamente", title="Exito") 
        
    # prod para eliminar columnas
    def encriptar_columnas(self):
        data_frame_encriptacion = pd.DataFrame(self.dataframe)
        
        for columna in self.columnas_selecionadas:
            data_frame_encriptacion[columna] = data_frame_encriptacion[columna].apply(lambda x: hs.sha256(str(x).encode()).hexdigest())
        
        data_frame_encriptacion.to_excel(self.ruta_guardado, index=False) 
        messagebox.showinfo(message="El archivo se ha guardado correctamente", title="Exito")         
        
    # prod para eliminar columnas
    def sustituir_columnas(self):
        print("sustituir")
        
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
        # invalidamos el metodo de cerrar por defecto y lo reempolazamos por la funcion de regresar al menu principal
        self.root.protocol("WM_DELETE_WINDOW", self.regresar_principal)
        self.root.title("Vista Previa - '"+self.nombre_archivo+"' - ")

        # inicializamos las variables con los parametros recibidos de la pantalla principal
        self.cabeceras = cabeceras
        self.data = data

        self.etiquetas_creadas = False

        # Iniciar el proceso de carga de datos en segundo plano
        self.cargar_datos_thread = threading.Thread(target=self.cargar_datos)
        self.cargar_datos_thread.start()

        centrar_ventana(self.root)
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
        self.scrollable_frame.pack(expand=True)

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
                self.crear_cuadro_texto(valor, i+1, j)

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
