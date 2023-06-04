from tkinter import*
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import font
import subprocess

tela = Tk()

# Funções principais

# Fonte
font_path = "font/Langar.ttf"
langar_font = font.Font(family="Langar", size=10)
tela.option_add("*Font", langar_font)

# Centralizar
largura = 1000
altura = 638

largura_screen = tela.winfo_screenwidth()
altura_screen = tela.winfo_screenheight()

posx = largura_screen/2 - largura/2
posy = altura_screen/2 - altura/2 -35

centerx = largura_screen/2 
centery = altura_screen/2

tela.geometry("%dx%d+%d+%d" % (largura,altura,posx,posy))


# Background
defaultPhoto = Image.open("imagens/Loading.png")
defaultPhotoSize = defaultPhoto.resize((1000, 638))
background = ImageTk.PhotoImage(defaultPhotoSize)
lbl_background = Label(image = background)
lbl_background.place(x=-2, y=-2)



tela.mainloop()