import customtkinter as ctk

#configuraciones globales de la interfaz
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class principal:
    #ruta de donde se extraera el archivo con la informacion
    path = ""   
    
    def __init__(self):
        #creacion de la ventana principal
        self.root = ctk.CTk()
        self.root.title("Anonimizer - Grupo #3")
        self.root.geometry("400x500")
        self.root.resizable(False, False) #no permite redimensionar
        
        #añadimos el contenido de esta ventana       
        self.marco = ctk.CTkFrame(self.root)
        self.marco.pack(padx=10, pady=10)
        
        #creacion de la parte de escoger el archivo
        #titulo
        ctk.CTkLabel(self.marco, text="Ruta del archivo", width=380, anchor="w", padx="10").grid(row=0, column=0, columnspan=2)
        
        #aca ingresaremos la ruta
        self.entrada = ctk.CTkEntry(self.marco, width=260)
        self.entrada.grid(row=1,column=0)
        #boton para comprobar que exista el archivo
        self.boton_envio = ctk.CTkButton(self.marco, text="Comprobar", command=lambda : self.escoger_archivo(), width=60, )
        self.boton_envio.grid(row=1, column=1)
        #este label mostrara el resultado de la comprobacion
        self.label_resul_archivo = ctk.CTkLabel(self.marco, text="", text_color="green", width=380, anchor="w", padx="10")
        self.label_resul_archivo.grid(row=2, column=0, columnspan=2)
        
        # Bucle de ejecución
        self.root.mainloop()        
    
    def escoger_archivo(self):
        self.path = self.entrada.get()
        
        if(self.path == None or self.path == ""):
            self.label_resul_archivo.configure(text="Llene la ruta antes de comprobar", text_color="red")
            self.entrada.focus();
        else:
            self.label_resul_archivo.configure(text="Archivo encontrado exitosamente", text_color="green")
            