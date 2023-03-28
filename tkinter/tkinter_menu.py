from tkinter import *
class App():
    #Método constructor
    def __init__(self):
        ventana=Tk()
        ventana.title("Ventana")
        ventana.geometry("1280x720")
        ventana.configure(bg='red')
        ventana.mainloop()

#Programa principal
objeto_ventana=App()
