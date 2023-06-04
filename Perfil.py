from tkinter import*
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import font
from pymongo import MongoClient
import subprocess
import shutil
import os
import cv2
import numpy as np


tela = Tk()

import sys
if len(sys.argv) > 1:
    user = sys.argv[1]

    client = MongoClient("mongodb://localhost:27017")
    db = client["libratour"]
    collection = db["Usuario"]

    # Verificar se o nome de usuário consta no banco
    if collection.find_one({"nome_usuario": user}):
            documento = collection.find_one({"nome_usuario": user})
            # Verifique se o documento foi encontrado
            if documento:
                idBD = documento["_id"]
                usernameBD = documento["nome_usuario"]
                nmCompletoBD = documento["nome_completo"]
                emailBD = documento["email"]
                senhaBD = documento["senha"]
                nome_arquivoBD = documento["imagem-usuario"]

                idU = idBD
                username = usernameBD
                nmCompletoU = nmCompletoBD
                emailU = emailBD
                senhaU = senhaBD
                nome_arquivo = nome_arquivoBD
                
            else:
                print("Usuário não encontrado")
            client.close()

    else: 
        client.close()
else:
    idBD = "0"
    idU = idBD
    username = "Sem usuário"
    nmCompletoU = "Não nomeado"
    emailU = "exemplo.email@gmail.com"
    senhaU = "Senha123*"


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
defaultPhoto = Image.open("imagens/Perfil.png")
defaultPhotoSize = defaultPhoto.resize((1000, 638))
background = ImageTk.PhotoImage(defaultPhotoSize)
lbl_background = Label(image = background)
lbl_background.place(x=-2, y=-2)


# Imagem Usuario
def rotate_image(image, angle):
    # Obtém as dimensões da imagem
    height, width = image.size

    # Calcula o tamanho da imagem rotacionada
    rotation_angle = np.radians(angle)
    cos_theta = abs(np.cos(rotation_angle))
    sin_theta = abs(np.sin(rotation_angle))
    new_width = int((width * cos_theta) + (height * sin_theta))
    new_height = int((width * sin_theta) + (height * cos_theta))

    # Realiza a rotação da imagem
    rotated_image = image.rotate(angle, expand=True)

    return rotated_image


def rotate_left():
    global angle
    angle -= 90
    rotated = rotate_image(original_image, angle)
    display_image(rotated)


def rotate_right():
    global angle
    angle += 90
    rotated = rotate_image(original_image, angle)
    display_image(rotated)


def display_image(image):
    # Redimensionar a imagem para as dimensões desejadas
    resized_image = image.resize((134, 134))
    
    # Criar uma nova imagem com fundo branco
    white_background = Image.new("RGB", resized_image.size, (255, 255, 255))
    white_background.paste(resized_image, (0, 0), resized_image)

    # Converter para objeto ImageTk
    image_tk = ImageTk.PhotoImage(white_background)

    # Atualizar o canvas com a nova imagem
    canvas.configure(image=image_tk)
    canvas.image = image_tk

# Carrega a imagem
# img inicial
client = MongoClient("mongodb://localhost:27017")
db = client["libratour"]
collection = db["Usuario"]

# Verificar se o nome de usuário consta no banco
if collection.find_one({"_id": idBD}):
        documento = collection.find_one({"_id": idBD})
        # Verifique se o documento foi encontrado
        if documento:
            nome_arquivoBD = documento["imagem-usuario"]
            nome_arquivo = nome_arquivoBD
            
        else:
            print("Usuário não encontrado")
        client.close()

else: 
    client.close()
if nome_arquivo == "Padrao-perfil.png":
    endImgIni= "imagens/Padrao-perfil.png"
else:
    endImgIni = "imagens-usuarios/" + nome_arquivo
image_path = endImgIni
original_image = Image.open(image_path)

# Configuração inicial
angle = 0

# Cria a janela e o canvas
canvas = Label(tela)
canvas.place(width=134, height=134, x=212, y=72)

# Cria os botões de rotação
button_left = Button(tela, text="⬅", font="20", command=rotate_right, borderwidth=0, bg="white", activebackground="white")
button_left.place(x=172, y=123)
button_right = Button(tela, text="➡", font="20", command=rotate_left, borderwidth=0, bg="white", activebackground="white")
button_right.place(x=346, y=123)

# Exibe a imagem original
display_image(original_image)



# lbl "Username"
lbl_username = Label(text=username, fg="#454545", bg="white", borderwidth=0.5, relief="flat", font="Langar 20", justify='center')
lbl_username.place(width=320, height=30, x=120, y=210)

# lbl classificacao
lbl_tClassificacao = Label(text="Classificação:", fg="#454545", bg="white", borderwidth=0.5, relief="flat", font="Langar 14")
lbl_tClassificacao.place(x=130, y=276)

# txt classificacao
classificacao = "Iniciante"
txt_Classificacao = Label(text=classificacao, fg="#6A6969", bg="white", borderwidth=0.5, relief="flat", font="Langar 14")
txt_Classificacao.place(x=255, y=276)

# img config
defaultPhoto = Image.open("imagens/Config.png")
defaultPhotoSize = defaultPhoto.resize((23, 23))
config = ImageTk.PhotoImage(defaultPhotoSize)
lbl_config = Label(image = config, bg="white")
lbl_config.place(x=184, y=348)

# lbl configuracoes
lbl_configuracoes = Label(text="Configurações", fg="#454545", bg="white", borderwidth=0.5, relief="flat", font="Langar 18")
lbl_configuracoes.place(x=218, y=342)

# lbl notificacoes
lbl_notificacoes = Label(text="Notificações", fg="#454545", bg="white", borderwidth=0.5, relief="flat", font="Langar 15")
lbl_notificacoes.place(x=122, y=410)

def btn_notesq():
    global esq
    defaultPhoto = Image.open("imagens/btn_notf_esq.png")
    defaultPhotoSize = defaultPhoto.resize((64, 34))
    largura, altura = defaultPhotoSize.size
    nova_largura = largura - 2
    nova_altura = altura - 2
    nova_imagem = Image.new("RGBA", (nova_largura, nova_altura), (0, 0, 0, 0))
    nova_imagem.paste(defaultPhotoSize, (0, 0))
    esq = ImageTk.PhotoImage(nova_imagem)
    btn_notf_esq = Button(image=esq, command=btn_notdir, borderwidth=0, highlightthickness=0, relief="flat", bg="white", activebackground="white")
    btn_notf_esq.place(x=370, y=411)

def btn_notdir():
    global dir
    defaultPhoto = Image.open("imagens/btn_notf_dir.png")
    defaultPhotoSize = defaultPhoto.resize((64, 34))
    largura, altura = defaultPhotoSize.size
    nova_largura = largura - 2
    nova_altura = altura - 2
    nova_imagem = Image.new("RGBA", (nova_largura, nova_altura), (0, 0, 0, 0))
    nova_imagem.paste(defaultPhotoSize, (0, 0))
    dir = ImageTk.PhotoImage(nova_imagem)
    btn_notf_dir = Button(image=dir, command=btn_notesq, borderwidth=0, highlightthickness=0, relief="flat", bg="white", activebackground="white")
    btn_notf_dir.place(x=370, y=411)
btn_notdir()

# lbl historico de rendimento
lbl_histRend = Label(text="Histórico de Rendimento", fg="#454545", bg="white", borderwidth=0.5, relief="flat", font="Langar 19")
lbl_histRend.place(x=582, y=60)

# lbl análise de pontuação por nível
lbl_histRend = Label(text="Análise de pontuação por nível", fg="#454545", bg="white", borderwidth=0.5, relief="flat", font="Langar 15")
lbl_histRend.place(x=582, y=130)

# img grafico
defaultPhoto = Image.open("imagens/Gráfico.png")
defaultPhotoSize = defaultPhoto.resize((322, 186))
grafc = ImageTk.PhotoImage(defaultPhotoSize)
lbl_grafc = Label(image = grafc, bg="white")
lbl_grafc.place(x=545, y=162)

# lbl media pontos/nivel
lbl_tMedia = Label(text="Média pontos/nível:", fg="#454545", bg="white", borderwidth=0.5, relief="flat", font="Langar 16")
lbl_tMedia.place(x=598, y=382)
# txt media
Media = "00.00"
txt_Media = Label(text=Media, fg="#6A6969", bg="white", borderwidth=0.5, relief="flat", font="Langar 14")
txt_Media.place(x=786, y=384)

# lbl pontuação total
lbl_tPTotal = Label(text="Pontuação total:", fg="#454545", bg="white", borderwidth=0.5, relief="flat", font="Langar 16")
lbl_tPTotal.place(x=612, y=446)

# txt media
pTotal = "00.00"
txt_pTotal = Label(text=pTotal, fg="#6A6969", bg="white", borderwidth=0.5, relief="flat", font="Langar 14")
txt_pTotal.place(x=774, y=448)

# btn "Voltar"
defaultPhoto = Image.open("imagens/Voltar.png")
defaultPhotoSize = defaultPhoto.resize((122, 58))
largura, altura = defaultPhotoSize.size
nova_largura = largura - 4
nova_altura = altura - 4
nova_imagem = Image.new("RGBA", (nova_largura, nova_altura), (0, 0, 0, 0))
nova_imagem.paste(defaultPhotoSize, (0, 0))
voltar = ImageTk.PhotoImage(nova_imagem)

btn_voltar = Button(image=voltar, borderwidth=0, highlightthickness=0, relief="flat", bg="#212B32", activebackground="#212B32")
btn_voltar.place(x=161, y=522)

def __detalhes__():
    lbl_notificacao = Label(text="", bg="#EAEAEA", borderwidth=0.5, relief="flat", font="Langar 10", justify='center')
    lbl_notificacao.place(width=320, height=12, x=338, y=512)
    
    def __limparDetalhes__():
        for widget in widgets_detalhes:
            widget.destroy()
        defaultUploadLabel.destroy()
        txt_nmUsuario.destroy()
        txt_nmCompleto.destroy()
        txt_Email.destroy()
        txt_Senha.destroy()
        lbl_config1.destroy()
        lbl_dtlhConta.destroy()
        lbl_nmUsuario.destroy()
        lbl_nmCompleto.destroy()
        lbl_Email.destroy()
        lbl_Senha.destroy()
        btn_deletConta.destroy()
        btn_x_voltar.destroy()
        
    widgets_detalhes = []

    def __deletar__():
        client = MongoClient("mongodb://localhost:27017")
        db = client["libratour"]
        collection = db["Usuario"]
        
        collection.delete_one({"_id": idBD})
        print("Conta deletada com sucesso!")
        
        client.close()

        tela.destroy()
        subprocess.run(["python", "Login.py"])

    client = MongoClient("mongodb://localhost:27017")
    db = client["libratour"]
    collection = db["Usuario"]

    # Verificar se o nome de usuário consta no banco
    if collection.find_one({"_id": idBD}):
            documento = collection.find_one({"_id": idBD})
            # Verifique se o documento foi encontrado
            if documento:
                nome_arquivoBD = documento["imagem-usuario"]
                nome_arquivo = nome_arquivoBD
                
            else:
                print("Usuário não encontrado")
            client.close()

    else: 
        client.close()

    # img inicial
    global defaultProfilePhoto
    if nome_arquivo == "Padrao-perfil.png":
        endIni= "imagens/Padrao-perfil.png"
    else:
        endIni = "imagens-usuarios/" + nome_arquivo
    defaultPhoto = Image.open(endIni)
    defaultPhotoSize = defaultPhoto.resize((134, 134))
    defaultProfilePhoto = ImageTk.PhotoImage(defaultPhotoSize)
    client.close()
    def __Salvar__():
        global defaultUploadLabel
        # Image Upload Frame
        pasta_inicial= ""

        def escolher_imagem():
            caminho_imagem = filedialog.askopenfilename(initialdir=pasta_inicial, title="Escolha uma imagem",
                                                        filetypes=(("Arquivos de imagem", "*.jpg;*.jpeg;*.png"),
                                                                ("Todos os arquivos", "*.*")))
            imagem_pil = Image.open(caminho_imagem)
            largura, altura = imagem_pil.size
            if altura > 134 or altura < 134:
                proporcao = altura / 134
                nova_altura = int(altura / proporcao)
                imagem_pil = imagem_pil.resize((134, nova_altura))
            imagem_tk = ImageTk.PhotoImage(imagem_pil)
            lbl_imagem = Button(tela, image=imagem_tk, command=escolher_imagem, borderwidth=0,  relief="flat",)
            lbl_imagem.image = imagem_tk
            lbl_imagem.place(x=431, y=122)
            widgets_detalhes.append(lbl_imagem)
            nome_arquivo = caminho_imagem

            def mover_imagem_para_pasta(nome_arquivo, caminho_pasta_destino):
                # Verificar se o arquivo existe
                if not os.path.isfile(nome_arquivo):
                    print(f"O arquivo '{nome_arquivo}' não existe.")
                    return

                # Verificar se a pasta de destino existe
                if not os.path.isdir(caminho_pasta_destino):
                    print(f"A pasta '{caminho_pasta_destino}' não existe.")
                    return

                try:
                    global novo_caminho_arquivo
                    global novo_nome_arquivo
                    nome_arquivo_com_extensao = os.path.basename(nome_arquivo)
                    novo_nome_arquivo = str(idU) + os.path.splitext(nome_arquivo_com_extensao)[1]
                    novo_caminho_arquivo = os.path.join(caminho_pasta_destino, novo_nome_arquivo)

                    shutil.copy2(nome_arquivo, novo_caminho_arquivo)
                    print(f"Arquivo '{novo_nome_arquivo}' copiado para '{caminho_pasta_destino}'.")
                except Exception as e:
                    print(f"Ocorreu um erro ao copiar o arquivo: {str(e)}")

            def enviar():
                button_left.destroy()
                button_right.destroy()
                canvas.destroy()
                
                def rotate_image(image, angle):
                    # Realiza a rotação da imagem
                    rotated_image1 = image.rotate(angle, expand=True)

                    return rotated_image1


                def rotate_left():
                    global angle
                    angle -= 90
                    rotated1 = rotate_image(original_image1, angle)
                    display_image(rotated1)


                def rotate_right():
                    global angle
                    angle += 90
                    rotated1 = rotate_image(original_image1, angle)
                    display_image(rotated1)


                def display_image(image1):
                    # Redimensionar a imagem para as dimensões desejadas
                    resized_image1 = image1.resize((134, 134))

                    # Criar uma nova imagem com fundo branco
                    white_background = Image.new("RGB", resized_image1.size, (255, 255, 255))
                    white_background.paste(resized_image1, (0, 0), resized_image1)

                    # Converter para objeto ImageTk
                    image_tk = ImageTk.PhotoImage(white_background)

                    # Atualizar o canvas com a nova imagem
                    canvas1.configure(image=image_tk)
                    canvas1.image = image_tk

                # Carrega a imagem
                image_path1 = novo_caminho_arquivo
                original_image1 = Image.open(image_path1)

                # Configuração inicial
                angle = 0

                # Cria a janela e o canvas
                canvas1 = Label(tela)
                canvas1.place(width=134, height=134, x=212, y=72)
                canvas1.lower(lbl_config1)

                # Cria os botões de rotação
                button_left1 = Button(tela, text="⬅", font="20", command=rotate_right, borderwidth=0, bg="white", activebackground="white")
                button_left1.place(x=172, y=123)
                button_right1 = Button(tela, text="➡", font="20", command=rotate_left, borderwidth=0, bg="white", activebackground="white")
                button_right1.place(x=346, y=123)
                button_right1.lower(lbl_config1)

                # Exibe a imagem original
                display_image(original_image1)
            
            caminho_pasta_destino = "imagens-usuarios"

            mover_imagem_para_pasta(nome_arquivo, caminho_pasta_destino)

            nome_arquivo_com_extensao = os.path.basename(nome_arquivo)

            nome_arquivo_com_extensao = novo_nome_arquivo

            client = MongoClient("mongodb://localhost:27017")
            db = client["libratour"]
            collection = db["Usuario"]
            collection.update_one(
                {"_id": idBD},
                {"$set": {"imagem-usuario": nome_arquivo_com_extensao}}
            )
            client.close()
            enviar()
        
        client = MongoClient("mongodb://localhost:27017")
        db = client["libratour"]
        collection = db["Usuario"]

        # Verificar se o nome de usuário consta no banco
        if collection.find_one({"_id": idBD}):
                documento = collection.find_one({"_id": idBD})
                # Verifique se o documento foi encontrado
                if documento:
                    nome_arquivoBD = documento["imagem-usuario"]
                    nome_arquivo = nome_arquivoBD
                    
                else:
                    print("Usuário não encontrado")
                client.close()

        else: 
            client.close()
        
        if endIni == "imagens-usuarios/" + nome_arquivo or endIni == "imagens/" + nome_arquivo:
            defaultUploadLabel = Button(image = defaultProfilePhoto, command=escolher_imagem, borderwidth=0.5,  relief="flat", takefocus=False)
            defaultUploadLabel.place(width=134, height=134, x=432, y=123)
            widgets_detalhes.append(defaultUploadLabel)

        
        client = MongoClient("mongodb://localhost:27017")
        db = client["libratour"]
        collection = db["Usuario"]
        
        # Verificar se o nome de usuário consta no banco
        if collection.find_one({"_id": idBD}):
                documento = collection.find_one({"_id": idBD})
                # Verifique se o documento foi encontrado
                if documento:
                    usernameBD = documento["nome_usuario"]
                    nmCompletoBD = documento["nome_completo"]
                    emailBD = documento["email"]
                    senhaBD = documento["senha"]

                    username = usernameBD
                    nmCompletoU = nmCompletoBD
                    emailU = emailBD
                    senhaU = senhaBD
                    nome_arquivoBD = documento["imagem-usuario"]
                    nome_arquivo = nome_arquivoBD
                    

                else:
                    print("Usuário não encontrado")
                client.close()
        else: 
            print("Usuário não encontrado")
            client.close()



        def __exibirDadosPT2__():
                txt_nmUsuario.config(state="disabled")
                txt_nmCompleto.config(state="disabled")
                txt_Email.config(state="disabled")
                txt_Senha.config(state="disabled", font=1, show="*")

                # btn "Editar"
                global editar
                defaultPhoto = Image.open("imagens/Editar.png")
                defaultPhotoSize = defaultPhoto.resize((184, 62))
                largura, altura = defaultPhotoSize.size
                nova_largura = largura - 24
                nova_altura = altura - 2
                nova_imagem = Image.new("RGBA", (nova_largura, nova_altura), (0, 0, 0, 0))
                nova_imagem.paste(defaultPhotoSize, (0, 0))
                editar = ImageTk.PhotoImage(nova_imagem)
                btn_editar = Button(image=editar, command=__Editar__, borderwidth=0, highlightthickness=0, relief="flat", bg="#EAEAEA", activebackground="#EAEAEA")
                btn_editar.place(x=312, y=526)
                widgets_detalhes.append(btn_editar)
                client.close()


        def __exibirDados__():
            # Mostrar dados nao alterados
            txt_nmUsuario.delete(0, END)
            txt_nmCompleto.delete(0, END)
            txt_Email.delete(0, END)
            txt_Senha.delete(0, END)

            txt_nmUsuario.insert(0, username)
            txt_nmCompleto.insert(0, nmCompletoU)
            txt_Email.insert(0, emailU)
            txt_Senha.insert(0, senhaU)
            __exibirDadosPT2__()


        client = MongoClient("mongodb://localhost:27017")
        db = client["libratour"]
        collection = db["Usuario"]

        if txt_nmCompleto.get() == "" or txt_nmUsuario.get() == "" or txt_Email.get() == "" or txt_Senha.get() == "":
            lbl_notificacao.lift()
            widgets_detalhes.append(lbl_notificacao)
            __exibirDados__()
            
        
        elif txt_nmCompleto.get() == nmCompletoU and txt_nmUsuario.get() == username and txt_Email.get() == emailU and txt_Senha.get() == senhaU and collection.find_one({"imagem-usuario": nome_arquivo}):
            lbl_notificacao.config(text="Nada foi alterado", fg="#006BA6")
            widgets_detalhes.append(lbl_notificacao)
            lbl_notificacao.lift()
            __exibirDados__()


        elif collection.find_one({"nome_usuario": txt_nmUsuario.get()}) and txt_nmUsuario.get() != username and collection.find_one({"nome_usuario": username}):
            lbl_notificacao.config(text="Este nome de usuário ja está em uso, tente outro!", fg="#DE1818")
            widgets_detalhes.append(lbl_notificacao)
            lbl_notificacao.lift()

        else:
            collection.update_one(
                {"_id": idBD},
                {"$set": {"nome_completo": txt_nmCompleto.get(), "nome_usuario": txt_nmUsuario.get(), "email": txt_Email.get(), "senha": txt_Senha.get()}}
            )
            lbl_notificacao.config(text="Dados atualzados com sucesso!", fg="#006BA6")
            widgets_detalhes.append(lbl_notificacao)
            
            __exibirDadosPT2__()


    def __Editar__():
        txt_nmUsuario.config(state="normal")
        txt_nmCompleto.config(state="normal")
        txt_Email.config(state="normal")
        txt_Senha.config(state="normal", font="Langar 14", show="")

        # btn "Salvar"
        global salvar
        defaultPhoto = Image.open("imagens/Salvar.png")
        defaultPhotoSize = defaultPhoto.resize((184, 62))
        largura, altura = defaultPhotoSize.size
        nova_largura = largura - 24
        nova_altura = altura - 2
        nova_imagem = Image.new("RGBA", (nova_largura, nova_altura), (0, 0, 0, 0))
        nova_imagem.paste(defaultPhotoSize, (0, 0))
        salvar = ImageTk.PhotoImage(nova_imagem)
        btn_salvar = Button(image=salvar, command=__Salvar__, borderwidth=0, highlightthickness=0, relief="flat", bg="#EAEAEA", activebackground="#EAEAEA")
        btn_salvar.place(x=312, y=526)
        widgets_detalhes.append(btn_salvar)



    global config1
    defaultPhoto = Image.open("imagens/Detalhes2.png")
    defaultPhotoSize = defaultPhoto.resize((450, 564))
    config1 = ImageTk.PhotoImage(defaultPhotoSize)
    lbl_config1 = Label(image=config1, bg="black")
    lbl_config1.place(x=275, y=40)

     # lbl Detalhes da Conta
    lbl_dtlhConta = Label(text="Detalhes da Conta", fg="#454545", borderwidth=0.5, relief="flat", font="Langar 18")
    lbl_dtlhConta.place(x=400, y=57)

    # lbl_nmUsuario
    lbl_nmUsuario = Label(text="Nome de Usuário:", fg="#454545", bg="#F4F4F4", borderwidth=0.5, relief="flat", font="Langar 16")
    lbl_nmUsuario.place(x=298, y=285)

    # txt_nmUsuario
    txt_nmUsuario = Entry(fg="#6A6969", bg="#E5E5E5", borderwidth=0.5, relief="flat", font="Langar 14")
    txt_nmUsuario.place(x=490, y=287)


    # lbl_nmCompleto
    lbl_nmCompleto = Label(text="Nome Completo:", fg="#454545", bg="#F4F4F4", borderwidth=0.5, relief="flat", font="Langar 16")
    lbl_nmCompleto.place(x=298, y=345)

    # txt_nmCompleto
    txt_nmCompleto = Entry(fg="#6A6969", bg="#E5E5E5", borderwidth=0.5, relief="flat", font="Langar 14")
    txt_nmCompleto.place(x=490, y=347)


    # lbl_Email
    lbl_Email = Label(text="E-mail:", fg="#454545", bg="#F4F4F4", borderwidth=0.5, relief="flat", font="Langar 16")
    lbl_Email.place(x=298, y=406)

    # txt_Email
    txt_Email = Entry(fg="#6A6969", bg="#E5E5E5", borderwidth=0.5, relief="flat", font="Langar 14")
    txt_Email.place(x=490, y=408)


    # lbl_Senha
    lbl_Senha = Label(text="Senha:", fg="#454545", bg="#F4F4F4", borderwidth=0.5, relief="flat", font="Langar 16")
    lbl_Senha.place(x=298, y=467)


    # txt_Senha
    txt_Senha = Entry(fg="#6A6969", bg="#E5E5E5", show="*", borderwidth=0.5, relief="flat", font="Langar 14")
    txt_Senha.place(x=490, y=469)

    def __iniciarDelecao__():
        def __cancelar__():
            lbl_delCont.destroy()
            lbl_Atencao.destroy()
            btn_x_voltar1.destroy()
            txt_ctzDeletar.destroy()
            txt_nPoderaDesfzr.destroy()
            btn_cancelar.destroy()
            btn_deletConta1.destroy()
            
        global delCont
        defaultPhoto = Image.open("imagens/DelConta.png")
        defaultPhotoSize = defaultPhoto.resize((450, 200))
        delCont = ImageTk.PhotoImage(defaultPhotoSize)
        lbl_delCont = Label(image=delCont, bg="black")
        lbl_delCont.place(x=275, y=256)

        lbl_Atencao = Label(text="Atenção!", fg="#454545", borderwidth=0.5, relief="flat", font="Langar 18")
        lbl_Atencao.place(x=450, y=267)

        # btn "X2"
        global x_voltar1
        defaultPhoto = Image.open("imagens/X.png")
        defaultPhotoSize = defaultPhoto.resize((38, 38))
        largura, altura = defaultPhotoSize.size
        nova_largura = largura - 2
        nova_altura = altura - 2
        nova_imagem1 = Image.new("RGBA", (nova_largura, nova_altura), (0, 0, 0, 0))
        nova_imagem1.paste(defaultPhotoSize, (0, 0))
        x_voltar1 = ImageTk.PhotoImage(nova_imagem1)
        btn_x_voltar1 = Button(command=__cancelar__, image=x_voltar1, borderwidth=0, highlightthickness=0, relief="flat", bg="#F4F4F4", activebackground="#F4F4F4")
        btn_x_voltar1.place(x=664, y=266)

        txt_ctzDeletar = Label(text="Tem certeza de que deseja deletar sua conta?", fg="#6A6969", bg="#F4F4F4", borderwidth=0.5, relief="flat", font="Langar 12")
        txt_ctzDeletar.place(x=334, y=321)
        
        txt_nPoderaDesfzr = Label(text="Esta ação não poderá ser desfeita!", fg="#DE1818", bg="#F4F4F4", borderwidth=0.5, relief="flat", font="Langar 12")
        txt_nPoderaDesfzr.place(x=334, y=345)

        global cancelar
        defaultPhoto = Image.open("imagens/Cancelar.png")
        defaultPhotoSize = defaultPhoto.resize((195, 57))
        largura, altura = defaultPhotoSize.size
        nova_largura = largura - 2
        nova_altura = altura - 2
        nova_imagem = Image.new("RGBA", (nova_largura, nova_altura), (0, 0, 0, 0))
        nova_imagem.paste(defaultPhotoSize, (0, 0))
        cancelar = ImageTk.PhotoImage(nova_imagem)
        btn_cancelar = Button(command=__cancelar__, image=cancelar, borderwidth=0, highlightthickness=0, relief="flat", bg="#E5E5E5", activebackground="#E5E5E5")
        btn_cancelar.place(x=298, y=382)

        global deletConta1
        defaultPhoto = Image.open("imagens/DeletarConta.png")
        defaultPhotoSize = defaultPhoto.resize((224, 57))
        largura, altura = defaultPhotoSize.size
        nova_largura = largura - 2
        nova_altura = altura - 2
        nova_imagem = Image.new("RGBA", (nova_largura, nova_altura), (0, 0, 0, 0))
        nova_imagem.paste(defaultPhotoSize, (0, 0))
        deletConta1 = ImageTk.PhotoImage(nova_imagem)
        btn_deletConta1 = Button(command=__deletar__, image=deletConta1, borderwidth=0, highlightthickness=0, relief="flat", bg="#E5E5E5", activebackground="#E5E5E5")
        btn_deletConta1.place(x=482, y=382)

    # btn "Deletar conta"
    global deletConta
    defaultPhoto = Image.open("imagens/Deletar.png")
    defaultPhotoSize = defaultPhoto.resize((220, 62))
    largura, altura = defaultPhotoSize.size
    nova_largura = largura - 2
    nova_altura = altura - 2
    nova_imagem = Image.new("RGBA", (nova_largura, nova_altura), (0, 0, 0, 0))
    nova_imagem.paste(defaultPhotoSize, (0, 0))
    deletConta = ImageTk.PhotoImage(nova_imagem)
    btn_deletConta = Button(command=__iniciarDelecao__, image=deletConta, borderwidth=0, highlightthickness=0, relief="flat", bg="#EAEAEA", activebackground="#EAEAEA")
    btn_deletConta.place(x=474, y=526)
    __Salvar__()

    # btn "X"
    global x_voltar
    defaultPhoto = Image.open("imagens/X.png")
    defaultPhotoSize = defaultPhoto.resize((45, 45))
    largura, altura = defaultPhotoSize.size
    nova_largura = largura - 2
    nova_altura = altura - 2
    nova_imagem = Image.new("RGBA", (nova_largura, nova_altura), (0, 0, 0, 0))
    nova_imagem.paste(defaultPhotoSize, (0, 0))
    x_voltar = ImageTk.PhotoImage(nova_imagem)
    btn_x_voltar = Button(command=__limparDetalhes__, image=x_voltar, borderwidth=0, highlightthickness=0, relief="flat", bg="#F4F4F4", activebackground="#F4F4F4")
    btn_x_voltar.place(x=668, y=52)
    

# btn "Detalhes"
defaultPhoto = Image.open("imagens/Detalhes.png")
defaultPhotoSize = defaultPhoto.resize((346, 62))
largura, altura = defaultPhotoSize.size
nova_largura = largura - 4
nova_altura = altura - 4
nova_imagem = Image.new("RGBA", (nova_largura, nova_altura), (0, 0, 0, 0))
nova_imagem.paste(defaultPhotoSize, (0, 0))
detalhes = ImageTk.PhotoImage(nova_imagem)
btn_detalhes = Button(command=__detalhes__, image=detalhes, borderwidth=0, highlightthickness=0, relief="flat", bg="#212B32", activebackground="#212B32")
btn_detalhes.place(x=290, y=520)


def __desconectar__():
    tela.destroy()
    subprocess.run(["python", "Login.py"])


# btn "Desconectar"
defaultPhoto = Image.open("imagens/Desconectar.png")
defaultPhotoSize = defaultPhoto.resize((220, 60))
largura, altura = defaultPhotoSize.size
nova_largura = largura - 4
nova_altura = altura - 4
nova_imagem = Image.new("RGBA", (nova_largura, nova_altura), (0, 0, 0, 0))
nova_imagem.paste(defaultPhotoSize, (0, 0))
desconectar = ImageTk.PhotoImage(nova_imagem)
btn_desconectar = Button(command=__desconectar__, image=desconectar, borderwidth=0, highlightthickness=0, relief="flat", bg="#212B32", activebackground="#212B32")
btn_desconectar.place(x=642, y=522)

tela.mainloop()