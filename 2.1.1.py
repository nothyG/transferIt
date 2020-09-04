import base64
import pyqrcode
import cv2
from pyzbar.pyzbar import decode, ZBarSymbol
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import time

inpt1 = ""

###mostrar qr###
def display():
  #file no debe de ser un archivo svg ####
  ##aun falta esta parte###
  pic = cv2.imread(file)
  cv2.imshow("Código Qr", pic)
  cv2.waitKey(0)

def mainView():
  win = tk.Tk()
  win.title("TransferIt")
  win.iconbitmap(default="favicon.ico")

  label1 = tk.Label(win, text="Transfer-it", font=20)
  label1.pack(padx=150,pady=10)

  btn1 = tk.Button(win, text="Enviar", command=codificar)
  btn1.pack(padx=20,pady=10)

  btn2 = tk.Button(win, text="Recibir", command=decodificar)
  btn2.pack(padx=20,pady=10)

  win.mainloop()

#info

#des = input("introduce 1 para encriptar o 2 para desencriptar ")
#des = "2"
#encoding
def codificar():
  cod = tk.Tk()
  cod.title("Enviar")

  lb1 = tk.Label(cod, text="Enviar texto", font=15)
  lb1.pack()

  global inpt1
  inpt1 = tk.Entry(cod)
  inpt1.pack(padx=30, pady=10)

  bt = tk.Button(cod, text="Ok", command=codif)
  bt.pack(pady=10, padx=10)

  cod.mainloop()

def codif():
  data = inpt1.get()
  ####PAARA  ARREGLAR!!!!!333
  #quitar  dde commentariio paara usar codificado
  #encodedBytes = base64.b64encode(data.encode("utf-8"))
  encodedBytes = data.encode("utf-8")
  Str = str(encodedBytes, "utf-8")

  url = pyqrcode.create(Str)
  global file
  file = "temporalQr"
  file = file + ".svg"
  url.svg(file, scale=8)
  display()
  print(Str)



def decodificar():
  video_capture = cv2.VideoCapture(0)
  i = 0
  while True:
    _, frame = video_capture.read()

    codes = decode(frame)

    try:
      for code in codes:
        data = code.data.decode('ascii')
        x, y, w, h = code.rect.left, code.rect.top, \
                    code.rect.width, code.rect.height
        cv2.rectangle(frame, (x,y),(x+w, y+h),(255, 0, 0), 6)
        cv2.putText(frame, "QR copiado!", (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        #print(data)

        encodedBytes = base64.b64decode(data.encode("utf-8"))
        Str = str(encodedBytes, "utf-8")
    except Exception as e:
      pass
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
      break
    try:
      if data and i == 15:
        found = tk.Tk()
        found.withdraw()
        found.clipboard_clear()
        found.clipboard_append(data)
        break
      if i < 15:
        i = i+1
    except Exception as e:
      pass

  video_capture.release()
  cv2.destroyAllWindows()

mainView()
