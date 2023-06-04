from tkinter import*
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import font
import subprocess
from pymongo import MongoClient

tela = Tk()

# Funções principais
def _cadastrar_():
    tela.destroy()
    subprocess.run(["python", "Cadastro.py"])

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
defaultPhoto = Image.open("imagens/Log-in.png")
defaultPhotoSize = defaultPhoto.resize((1000, 638))
background = ImageTk.PhotoImage(defaultPhotoSize)
lbl_background = Label(image = background)
lbl_background.place(x=-2, y=-2)


# Função de Login
def __Login__():
    # Dados do formulário
    user = txt_user.get()
    senha = txt_senha.get()

    # Conectar ao banco de dados MongoDB
    client = MongoClient("mongodb://localhost:27017")
    db = client["libratour"]
    collection = db["Usuario"]

    # Verificar se o nome de usuário consta no banco
    if collection.find_one({"nome_usuario": user, "senha": senha}):
            tela.destroy()
            subprocess.run(["python", "Perfil.py", user])
            
    else:
        btn_entrar.place(x=446, y=416)
        btn_esqueceuSuaSenha.place(x=436, y=466)
        # lbl_notificacao
        lbl_notificacao = Label(text="", fg="#FF9595", bg="#1D3141", borderwidth=0.5, relief="flat", font="Langar 10", justify='center')
        lbl_notificacao.place(width=220, height=15, x=388, y=392)
        lbl_notificacao.config(text="Nome de usuário ou senha incorretos")

        # Fechar a conexão com o banco de dados
        client.close()
        return

    # Redefinir os campos do formulário
    restore_user(None)
    restore_senha(None)

# txt "User" com interação de texto interno
def inicio_user(event):
    if txt_user.get() == "User ":
        txt_user.icursor(0)
def clear_user(event):
    if txt_user.get() == "User ":
        txt_user.delete(0, END)
        txt_user.icursor(0)
def restore_user(event):
    if txt_user.get() == "":
        txt_user.delete(0, END)
        txt_user.insert(0, "User ")
        txt_user.config(fg="#7C7C7C")
        txt_user.icursor(0)
def rest_apagado_user(event):
    if len(txt_user.get()) == 0:
        restore_user(event)

txt_user = Entry(borderwidth=0.5, fg="#7C7C7C", bg="white", relief="flat")
txt_user.place(width=128, height=31, x=435, y=298)
txt_user.insert(0,"User ")
txt_user.bind("<FocusIn>", inicio_user)
txt_user.bind("<Key>", clear_user)
txt_user.bind("<KeyRelease>", rest_apagado_user)
txt_user.bind("<FocusOut>", restore_user)


# txt "Senha" com interação de texto interno
def inicio_senha(event):
    if txt_senha.get() == "Senha ":
        txt_senha.icursor(0)
def clear_senha(event):
    if txt_senha.get() == "Senha ":
        txt_senha.delete(0, END)
        txt_senha.config(show="")
        txt_senha.icursor(0)
        txt_senha.config(fg="#5F5F5F", font=1, show="*")
def restore_senha(event):
    if txt_senha.get() == "":
        txt_senha.delete(0, END)
        txt_senha.config(fg="#7C7C7C", font="Langar 10", show="")
        txt_senha.insert(0, "Senha ")
        txt_senha.icursor(0)
def rest_apagado_senha(event):
    if len(txt_senha.get()) == 0:
        restore_senha(event)

txt_senha = Entry(borderwidth=0.5, fg="#7C7C7C", bg="white", relief="flat")
txt_senha.place(width=128, height=31, x=435, y=351)
txt_senha.insert(0, "Senha ")
txt_senha.bind("<FocusIn>", inicio_senha)
txt_senha.bind("<Key>", clear_senha)
txt_senha.bind("<KeyRelease>", rest_apagado_senha)
txt_senha.bind("<FocusOut>", restore_senha)

# btn "Entrar"
defaultPhoto = Image.open("imagens/Botão Entrar.png")
defaultPhotoSize = defaultPhoto.resize((112, 48))
largura, altura = defaultPhotoSize.size
nova_largura = largura - 4
nova_altura = altura - 4
nova_imagem = Image.new("RGBA", (nova_largura, nova_altura), (0, 0, 0, 0))
nova_imagem.paste(defaultPhotoSize, (-1, -1))
entrar = ImageTk.PhotoImage(nova_imagem)
btn_entrar = Button(image=entrar, command=__Login__, borderwidth=0, highlightthickness=0, relief="flat", bg="#1D313F", activebackground="#1D313F")
btn_entrar.place(x=446, y=398)

# btn "Esqueceu sua senha?"
btn_esqueceuSuaSenha = Button(text="Esqueceu sua senha?", fg="white", bg="#1E2F3A", borderwidth=0, highlightthickness=0, relief="flat", activebackground="#414D56", activeforeground="white")
btn_esqueceuSuaSenha.place(height=20, x=436, y=448)

# lbl "Não possui uma conta?"
lbl_naoPossuiConta = Label(text="Não possui uma conta?", fg="white", bg="#1F2C34")
lbl_naoPossuiConta.place(height=20,x=378, y=493)

# btn "Cadastre-se aqui!"
btn_cadastreseAqui = Button(text="Cadastre-se aqui!", command=_cadastrar_, fg="#88BFFF", activeforeground="#88BFFF" , bg="#1F2C34", borderwidth=0, highlightthickness=0, relief="flat", activebackground="#1F2C34")
btn_cadastreseAqui.place(height=20,x=520, y=493)

tela.mainloop()