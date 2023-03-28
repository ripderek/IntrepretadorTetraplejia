#------------------------------ Importamos las librerias ------------------------------
from cProfile import label
from tkinter import *
from pygame import mixer
from PIL import Image
from PIL import Image as Image2
from PIL import Image as Image3
from PIL import Image as Image4
from PIL import Image as Image5
from PIL import Image as Image6
from PIL import ImageTk
from PIL import ImageTk as ImageTk2
from PIL import ImageTk as ImageTk3
from PIL import ImageTk as ImageTk4
from PIL import ImageTk as ImageTk5
from PIL import ImageTk as ImageTk6
import cv2
from matplotlib.pyplot import text
import mediapipe as mp
import time
import os
import datetime

def Text_to_speech():
    global n
    mixer.init()
    ruta = "audios/audio_"+str(n)+".wav"
    #cancion=str("audios/audio_1.wav")
    cancion = str(ruta)
    mixer.music.load(cancion)
    mixer.music.set_volume(0.7)
    mixer.music.play()

def Interpretador():
    #------------------------------ Declaramos el detector --------------------------------
     detector = mp.solutions.face_detection
     dibujo = mp.solutions.drawing_utils

#------------------------------ Realizamos VideoCaptura --------------------------------
     global cap
     cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#-------------------------------Empezamos el while True --------------------------------
     with detector.FaceDetection(min_detection_confidence=0.75, model_selection=0) as rostros:
         while True:

        # Lectura de fotogramas
            ret, frame = cap.read()

        #  espejo a los frames
            frame = cv2.flip(frame,1)

        #  de color
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #  los rostros
            resultado = rostros.process(rgb)

        # Creamos listas
            listacentro = []
            listarostro = []


        #  hay rostros entramos al if
            if resultado.detections is not None:
               for rostro in resultado.detections:
                #dibujo.draw_detection(frame, rostro, dibujo.DrawingSpec(color=(0,255,0),))

                  for id, puntos in enumerate(resultado.detections):
                    #  el ancho y el alto del frame
                     al, an, c = frame.shape

                    #  el medio de la pantalla
                     global centro
                     centro = int(an / 2)

                    # Extraemos las coordenadas X e Y min
                     x = puntos.location_data.relative_bounding_box.xmin
                     y = puntos.location_data.relative_bounding_box.ymin

                    # Extraemos el ancho y el alto
                     ancho = puntos.location_data.relative_bounding_box.width
                     alto = puntos.location_data.relative_bounding_box.height

                    # Pasamos X e Y a coordenadas en pixeles
                     x, y = int(x * an), int(y * al)
                    #print("X, Y: ", x, y)

                    # Pasamos el ancho y el alto a pixeles
                     x1, y1 = int(ancho * an), int(alto * al)
                     xf, yf = x + x1, y + y1

                    # Extraemos el punto central
                     cx = (x + (x + x1)) // 2
                     cy = (y + (y + y1)) // 2

                     listacentro.append([id, cx, cy])
                     listarostro.append([x, y, x1, y1])

                    # Mostrar un punto en el centro
                     cv2.circle(frame, (cx, cy), 3, (0, 0, 255), cv2.FILLED)
                     cv2.line(frame, (cx, 0), (cx, 480), (0, 0, 255), 2)

                    # Dibujamos el rectangulo
                     cv2.rectangle(frame, (x, y), (xf, yf), (255, 255, 0),3)  # Dibujamos el rectangulo
                     cv2.putText(frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
                     global xmo
                     global ymo
                     xmo = cx
                     ymo = cy
                     print(resultado.detections[id])

                     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                     ig = Image4.fromarray(frame)
                     ig = ig.resize((300, 230), Image4.ANTIALIAS)
                     imag = ImageTk4.PhotoImage(image=ig)
                     etiq_video.configure(image=imag)
                     etiq_video.image=imag

                     direecion()
            #cv2.imshow('Camara', frame)
            t = cv2.waitKey(1)
            if t == 27:
               break
     cap.release()
     cv2.destroyAllWindows()

def direecion():
    global xmo
    global centro
    global tiempo1
    global tiempo2
    global aba
    global der
    if xmo < centro - der:
        lblmensaje.configure(text="Izquierda")
        ContadorA()
    elif xmo > centro + der:
        lblmensaje.configure(text="Derecha")
        ContadorB()
    elif ymo > centro - aba:
         lblmensaje.configure(text="Abajo")
         Text_to_speech()
         ventana.update()
    else :
        lblmensaje.configure(text="Centro")
        tiempo1 = 0
        tiempo2 = 0
    ventana.update()


def ContadorA():
    global n
    global tiempo1
    global tiempo2
    global tiemsegun

    ahora = datetime.datetime.now()

    if tiempo1 == 0:
        tiempo1 = ahora.second

    if tiempo1 != 0:
        tiempo2 = ahora.second

    if tiempo2 > tiempo1:
        if tiempo2 - tiempo1 >= tiemsegun:
            Resetiempo_Izqui()
    elif tiempo1 - tiempo2 >= tiemsegun:
        Resetiempo_Izqui()

    #lblcontador.configure(text=n)
    ventana.update()

def ContadorB():
    global n
    global tiempo1
    global tiempo2
    global tiemsegun

    ahora = datetime.datetime.now()

    if tiempo1 == 0:
        tiempo1 = ahora.second

    if tiempo1 != 0:
        tiempo2 = ahora.second

    if tiempo2 > tiempo1:
        if tiempo2 - tiempo1 >= tiemsegun:
            Resetiempo_Derecha()
    elif tiempo1 - tiempo2 >= tiemsegun:
        Resetiempo_Derecha()

    #lblcontador.configure(text=n)
    ventana.update()

def Resetiempo_Izqui():
    global n
    global tiempo1
    global tiempo2
    global n_men
    global n_mas
    n = n - 1
    if n == 0:
        n = 10
        n_mas = 1
        n_men = n - 1
    elif n == 1:
        n_men = 10
        n_mas = n + 1
    else:
        n_mas = n + 1
        n_men = n - 1
    #lblcontador.configure(text=n)
    #lblcontador_mas.configure(text=n_mas)
    #lblcontador_menos.configure(text=n_men)
    cambio_imagen()
    cambio_der()
    cambio_iz()
    ventana.update()
    tiempo1 = 0
    tiempo2 = 0

def Resetiempo_Derecha():
    global n
    global tiempo1
    global tiempo2
    global n_mas
    global n_men
    n = n + 1
    if n == 10:
        n_mas = 1
        n_men = 9
    elif n == 11:
        n = 1
        n_mas = n + 1
        n_men = 10
    else:
        n_mas = n + 1
        n_men = n-1
    #lblcontador.configure(text=n)
    #lblcontador_mas.configure(text=n_mas)
    #lblcontador_menos.configure(text=n_men)
    cambio_imagen()
    cambio_der()
    cambio_iz()
    tiempo1 = 0
    tiempo2 = 0

def cambio_imagen():
    #PARA CAMBIAR LA IMAGEN CENTRAL
    global lbl_img_c
    global ruta
    global image
    global img
    global n
    ruta = "imagenes/img_"+str(n)+".png"
    image = Image.open(ruta)
    image = image.resize((450, 500), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image)
    lbl_img_c.config(image=img)


def cambio_der():
    # PARA CAMBIAR LA IMAGEN DERECHA
    global lbl_img_d
    global ruta_der
    global image_der
    global img_der
    global n_mas
    ruta_der = "imagenes/img_"+str(n_mas)+".png"
    image_der = Image2.open(ruta_der)
    image_der = image_der.resize((280, 300), Image2.ANTIALIAS)
    img_der = ImageTk2.PhotoImage(image_der)
    lbl_img_d.config(image=img_der)
    lbl_img_d.update()
    ventana.update()

def cambio_iz():
    # PARA CAMBIAR LA IMAGEN IZQUIERDA
    global lbl_img_iz
    global ruta_iz
    global image_iz
    global img_iz
    global n_men
    ruta_iz = "imagenes/img_"+str(n_men)+".png"
    image_iz = Image3.open(ruta_iz)
    image_iz = image_iz.resize((280, 300), Image3.ANTIALIAS)
    img_iz = ImageTk3.PhotoImage(image_iz)
    lbl_img_iz.config(image=img_iz)
    lbl_img_iz.update()
    ventana.update()

def leerTmepo():
    h = open('Config/timepo.txt', 'r')

    content = h.readlines()
    global tiemsegun
    a = 0

    for line in content:

        for i in line:

            if i.isdigit() == True:
                tiemsegun = int(i)

def LeerAba():
    h = open('Config/aba.txt', 'r')

    content = h.readlines()
    global aba
    a = 0

    for line in content:

        for i in line:

            if i.isdigit() == True:
                aba = int(i)*10

def LeerDer():
    h = open('Config/dere.txt', 'r')

    content = h.readlines()
    global der
    a = 0

    for line in content:

        for i in line:

            if i.isdigit() == True:
                der = int(i)*10

n_mas = 2
tiemsegun = 0
aba = 0
der = 0
izq = 0
tiempo1 = 0
tiempo2 = 0
n_men = 10
n=1
centro=0
xmo=0
ymo=0
cap= None
ventana=Tk()
ventana.title("Interpretador")
ventana.geometry("1280x700")
ventana.configure(bg='#f2e3d5')

#IMAGEN DEL CENTRO
ruta = "imagenes/img_1.png"
image = Image.open(ruta)
image = image.resize((450, 500), Image.ANTIALIAS)
img = ImageTk.PhotoImage(image)
lbl_img_c = Label(ventana)
lbl_img_c.config(image=img)
lbl_img_c.place(x=480, y=120)


#IMAGEN DERECHA
ruta_der = "imagenes/img_2.png"
image_der = Image2.open(ruta_der)
image_der = image_der.resize((280, 300), Image2.ANTIALIAS)
img_der = ImageTk2.PhotoImage(image_der)
lbl_img_d = Label(ventana)
lbl_img_d.config(image=img_der)
lbl_img_d.place(x=1050, y=150)


#IMAGEN IZQUIERDA
ruta_iz = "imagenes/img_10.png"
image_iz = Image3.open(ruta_iz)
image_iz = image_iz.resize((280, 300), Image3.ANTIALIAS)
img_iz = ImageTk3.PhotoImage(image_iz)
lbl_img_iz = Label(ventana)
lbl_img_iz.config(image=img_iz)
lbl_img_iz.place(x=100, y=150)

#Flecha Indicadora
ruta_ind = "imagenes/ind_1.png"
image_ind = Image5.open(ruta_ind)
image_ind = image_ind.resize((240, 100), Image5.ANTIALIAS)
img_ind = ImageTk5.PhotoImage(image_ind)
lbl_img_ind = Label(ventana)
lbl_img_ind.config(image=img_ind)
lbl_img_ind.place(x=1050, y=30)

#Flecha Indicadora 2
ruta_ind1 = "imagenes/ind_2.png"
image_ind1 = Image6.open(ruta_ind1)
image_ind1 = image_ind1.resize((240, 100), Image6.ANTIALIAS)
img_ind1 = ImageTk6.PhotoImage(image_ind1)
lbl_img_ind1 = Label(ventana)
lbl_img_ind1.config(image=img_ind1)
lbl_img_ind1.place(x=140, y=30)




#PARA MOSTRAR LA WEBCAM
etiq_video = Label(ventana, bg="black")
etiq_video.place(x=1030, y=470)


#btnEmpezar = Button(ventana, text="Probar", command=Interpretador)
#btnEmpezar.grid(column=0, row=0, padx=5, pady=5, columnspan=2)



mensaje = StringVar
lblmensaje = Label(ventana, text=mensaje)
lblmensaje.grid(column=15, row=15, padx=605, pady=40, columnspan=3)
lblmensaje.config(font=("verdana",40))

##lblcontador = Label(ventana, text= n)
##lblcontador.grid(column=25, row=15, padx=5, pady=5, columnspan=3)
##lblcontador.config(font=("verdana",24))

#lblcontador_mas = Label(ventana, text= n_mas)
#lblcontador_mas.grid(column=13, row=4, padx=5, pady=5, columnspan=3)
#lblcontador_mas.config(font=("verdana",24))

#lblcontador_menos = Label(ventana, text=n_men)
#lblcontador_menos.grid(column=5, row=4, padx=5, pady=5, columnspan=3)
#lblcontador_menos.config(font=("verdana",24))


#Para inicar automaticamente el interprete
leerTmepo()
LeerAba()
LeerDer()
Interpretador()
if __name__ == '__main__':
    ventana.mainloop()


