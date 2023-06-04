from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import font
import subprocess
from pymongo import MongoClient

tela = Tk()

# Funções Principais
def _entrar_():
    tela.destroy()
    subprocess.run(["python", "Login.py"])

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
# Fim-centralizar

# Background
defaultPhoto = Image.open("imagens/Cadastro.png")
defaultPhotoSize = defaultPhoto.resize((1000, 638))
background = ImageTk.PhotoImage(defaultPhotoSize)
lbl_background = Label(image = background)
lbl_background.place(x=-2, y=-2)

# lbl_notificacao
lbl_notificacao = Label(text="", fg="#FF9595", bg="#202C35", borderwidth=0.5, relief="flat", font="Langar 10", justify='center')
lbl_notificacao.place(width=320, height=20, x=338, y=490)


# Função para cadastrar os dados no MongoDB
def __cadastrar_dados__():
    # Dados do formulário
    nome_completo = txt_nomeCompleto.get()
    nome_usuario = txt_nomeUsuario.get()
    email = txt_email.get()
    senha = txt_senha.get()
    csenha = txt_confirmarSenha.get()

    # Conectar ao banco de dados MongoDB
    client = MongoClient("mongodb://localhost:27017")
    db = client["libratour"]
    collection = db["Usuario"]

    if nome_completo == "Nome completo " or nome_usuario == "Nome de usuario " or email == "E-mail " or senha == "Senha" or csenha == "Confirmar senha":
        lbl_notificacao.config(text="Todos os campos precisam ser preenchidos!")
        
        # Fechar a conexão com o banco de dados
        client.close()
        return


    if senha != csenha:
        lbl_notificacao.config(text="As senhas precisam ser iguais!")
        client.close()
        return

    # Verificar se o nome de usuário já existe no banco
    if collection.find_one({"nome_usuario": nome_usuario}):
        lbl_notificacao.config(text="Este nome de usuário ja está em uso, tente outro!")

        # Fechar a conexão com o banco de dados
        client.close()
        return

    # Criar um documento com os dados do formulário
    documento = {
        "nome_completo": nome_completo,
        "nome_usuario": nome_usuario,
        "email": email,
        "senha": senha,
        "imagem-usuario" : "Padrao-perfil.png"
    }

    # Inserir o documento na coleção
    collection.insert_one(documento)

    # Verificar se os dados foram inseridos corretamente
    if collection.find_one(documento):
        print("Dados cadastrados com sucesso!")
        tela.destroy()
        user=nome_usuario
        subprocess.run(["python", "Perfil.py", user])
    else:
        lbl_notificacao.config(text="Falha ao cadastrar os dados")

    # Fechar a conexão com o banco de dados
    client.close()

    # Redefinir os campos do formulário
    restore_nomeCompleto(None)
    restore_nomeUsuario(None)
    restore_email(None)
    restore_senha(None)
    restore_confirmarSenha(None)


# txt "nomeCompleto" com interação de texto interno
def inicio_nomeCompleto(event):
    if txt_nomeCompleto.get() == "Nome completo ":
        txt_nomeCompleto.icursor(0)
def clear_nomeCompleto(event):
    if txt_nomeCompleto.get() == "Nome completo ":
        txt_nomeCompleto.delete(0, END)
        txt_nomeCompleto.icursor(0)
def restore_nomeCompleto(event):
    if txt_nomeCompleto.get() == "":
        txt_nomeCompleto.delete(0, END)
        txt_nomeCompleto.insert(0, "Nome completo ")
        txt_nomeCompleto.config(fg="#7C7C7C")
        txt_nomeCompleto.icursor(0)
def rest_apagado_nomeCompleto(event):
    if len(txt_nomeCompleto.get()) == 0:
        restore_nomeCompleto(event)

txt_nomeCompleto = Entry(borderwidth=0.5, fg="#7C7C7C", bg="white", relief="flat")
txt_nomeCompleto.place(width=210, height=31, x=395, y=265)
txt_nomeCompleto.insert(0,"Nome completo ")
txt_nomeCompleto.bind("<FocusIn>", inicio_nomeCompleto)
txt_nomeCompleto.bind("<Key>", clear_nomeCompleto)
txt_nomeCompleto.bind("<KeyRelease>", rest_apagado_nomeCompleto)
txt_nomeCompleto.bind("<FocusOut>", restore_nomeCompleto)


# txt "nomeUsuario" com interação de texto interno
def inicio_nomeUsuario(event):
    if txt_nomeUsuario.get() == "Nome de usuario ":
        txt_nomeUsuario.icursor(0)
def clear_nomeUsuario(event):
    if txt_nomeUsuario.get() == "Nome de usuario ":
        txt_nomeUsuario.delete(0, END)
        txt_nomeUsuario.icursor(0)
def restore_nomeUsuario(event):
    if txt_nomeUsuario.get() == "":
        txt_nomeUsuario.delete(0, END)
        txt_nomeUsuario.insert(0, "Nome de usuario ")
        txt_nomeUsuario.config(fg="#7C7C7C")
        txt_nomeUsuario.icursor(0)
def rest_apagado_nomeUsuario(event):
    if len(txt_nomeUsuario.get()) == 0:
        restore_nomeUsuario(event)

txt_nomeUsuario = Entry(borderwidth=0.5, fg="#7C7C7C", bg="white", relief="flat")
txt_nomeUsuario.place(width=210, height=31, x=395, y=313)
txt_nomeUsuario.insert(0,"Nome de usuario ")
txt_nomeUsuario.bind("<FocusIn>", inicio_nomeUsuario)
txt_nomeUsuario.bind("<Key>", clear_nomeUsuario)
txt_nomeUsuario.bind("<KeyRelease>", rest_apagado_nomeUsuario)
txt_nomeUsuario.bind("<FocusOut>", restore_nomeUsuario)


# txt "email" com interação de texto interno
def inicio_email(event):
    if txt_email.get() == "E-mail ":
        txt_email.icursor(0)
def clear_email(event):
    if txt_email.get() == "E-mail ":
        txt_email.delete(0, END)
        txt_email.icursor(0)
def restore_email(event):
    if txt_email.get() == "":
        txt_email.delete(0, END)
        txt_email.insert(0, "E-mail ")
        txt_email.config(fg="#7C7C7C")
        txt_email.icursor(0)
def rest_apagado_email(event):
    if len(txt_email.get()) == 0:
        restore_email(event)

txt_email = Entry(borderwidth=0.5, fg="#7C7C7C", bg="white", relief="flat")
txt_email.place(width=210, height=31, x=395, y=360)
txt_email.insert(0,"E-mail ")
txt_email.bind("<FocusIn>", inicio_email)
txt_email.bind("<Key>", clear_email)
txt_email.bind("<KeyRelease>", rest_apagado_email)
txt_email.bind("<FocusOut>", restore_email)


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
txt_senha.place(width=210, height=31, x=395, y=408)
txt_senha.insert(0, "Senha ")
txt_senha.bind("<FocusIn>", inicio_senha)
txt_senha.bind("<Key>", clear_senha)
txt_senha.bind("<KeyRelease>", rest_apagado_senha)
txt_senha.bind("<FocusOut>", restore_senha)


# txt "confirmarSenha" com interação de texto interno
def inicio_confirmarSenha(event):
    if txt_confirmarSenha.get() == "Confirmar senha ":
        txt_confirmarSenha.icursor(0)
def clear_confirmarSenha(event):
    if txt_confirmarSenha.get() == "Confirmar senha ":
        txt_confirmarSenha.delete(0, END)
        txt_confirmarSenha.config(show="")
        txt_confirmarSenha.icursor(0)
        txt_confirmarSenha.config(fg="#5F5F5F", font=1, show="*")
def restore_confirmarSenha(event):
    if txt_confirmarSenha.get() == "":
        txt_confirmarSenha.delete(0, END)
        txt_confirmarSenha.config(fg="#7C7C7C", font="Langar 10", show="")
        txt_confirmarSenha.insert(0, "Confirmar senha ")
        txt_confirmarSenha.icursor(0)
def rest_apagado_confirmarSenha(event):
    if len(txt_confirmarSenha.get()) == 0:
        restore_confirmarSenha(event)

txt_confirmarSenha = Entry(borderwidth=0.5, fg="#7C7C7C", bg="white", relief="flat")
txt_confirmarSenha.place(width=210, height=31, x=395, y=456)
txt_confirmarSenha.insert(0, "Confirmar senha ")
txt_confirmarSenha.bind("<FocusIn>", inicio_confirmarSenha)
txt_confirmarSenha.bind("<Key>", clear_confirmarSenha)
txt_confirmarSenha.bind("<KeyRelease>", rest_apagado_confirmarSenha)
txt_confirmarSenha.bind("<FocusOut>", restore_confirmarSenha)

# lbl "Já possui uma conta?"
lbl_cadastrar = Label(text="Já possui uma conta?", fg="white", bg="#22282D")
lbl_cadastrar.place(height=20,x=410, y=563)
# btn "Entrar"
btn_cadastrar = Button(text="Entrar", command=_entrar_, fg="#88BFFF", activeforeground="#88BFFF" , bg="#22282D", borderwidth=0, highlightthickness=0, relief="flat", activebackground="#22282D")
btn_cadastrar.place(height=20,x=542, y=563)


# btn "Cadastrar"
defaultPhoto = Image.open("imagens/Botão Cadastrar.png")
defaultPhotoSize = defaultPhoto.resize((150, 48))
largura, altura = defaultPhotoSize.size
nova_largura = largura - 4
nova_altura = altura - 4
nova_imagem = Image.new("RGBA", (nova_largura, nova_altura), (0, 0, 0, 0))
nova_imagem.paste(defaultPhotoSize, (0, -1))
cadastrar = ImageTk.PhotoImage(nova_imagem)
btn_cadastrar = Button(image=cadastrar, borderwidth=0, highlightthickness=0, relief="flat", bg="#22292E", activebackground="#22292E", command=__cadastrar_dados__)
btn_cadastrar.place(x=427, y=512)

tela.mainloop()