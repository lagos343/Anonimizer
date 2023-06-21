import customtkinter as ctk

#configuraciones globales de la interfaz
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class principal:   
    
    def __init__(self):
        #creacion de la ventana principal
        self.root = ctk.CTk()
        self.root.title("Anonimizer - Grupo #3")
        self.root.geometry("400x500")
        self.root.resizable(False, False) #no permite redimensionar
        
        #añadimos el contenido de esta ventana
        # Botón
        ctk.CTkButton(self.root, text="Boton", command=self.prueba).pack(pady=10)
        
        # Bucle de ejecución
        self.root.mainloop()
        
    def prueba(self):        
        print("TRABAJANDO PAPA")
        