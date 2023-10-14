import socket
import tkinter as tk
from tkinter import filedialog

# Funcao que verifica a entrada do usuario, representando o objeto que sera desenhado
def verificar_entrada():
    global mensagem
    mensagem = entrada.get()
    janela.destroy()

# Inicia o desenho
def iniciar_desenho(event):
    global desenho
    desenho = True
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.create_oval(x1, y1, x2, y2, fill="black", width=2)

# Cancela o desenho quando o botao esquerdo nao esta pressionado
def parar_desenho(event):
    global desenho
    desenho = False

# Define um ponto onde o mouse estiver pressionado
def desenhar(event):
    if desenho:
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        canvas.create_oval(x1, y1, x2, y2, fill="black", width=2)

# Limpa a janela de desenho
def limpar_desenho():
    canvas.delete("all")

# Finaliza a janela salvando a imagem
def fechar_janela():
	file_path = "image.png"
	canvas.postscript(file=file_path, colormode="color")
	root.destroy()  #Fecha a janela


# Define-se o endereço e a porta do servidor que você deseja se conectar
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12380

# Cria um socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta-se ao servidor
client_socket.connect((SERVER_HOST, SERVER_PORT))


# Cria uma janela
janela = tk.Tk()
janela.title("Palavra")

# Label de instrucao ao usuario
frase_label = tk.Label(janela, text="Escreva a palavra que representa seu desenho:")
frase_label.pack()

# Cria uma entrada de texto
entrada = tk.Entry(janela)
entrada.pack()

# Cria um botão para salvar a entrada
verificar_botao = tk.Button(janela, text="Salvar", command=verificar_entrada)
verificar_botao.pack()

# Inicializa a janela
janela.mainloop()

# Envia a palavra que representa o desenho
client_socket.send(mensagem.encode('utf-8'))

# Recebe a resposta do servidor indicando que eh possivel iniciar o desenho
response = client_socket.recv(1024)
print(response.decode('utf-8'))

# Inicializa a janela de deseho
root = tk.Tk()
root.title("Aplicativo de Desenho")
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()
desenho = False
canvas.bind("<Button-1>", iniciar_desenho)
canvas.bind("<ButtonRelease-1>", parar_desenho)
canvas.bind("<B1-Motion>", desenhar)

# Inicializa o botao de limpar tela
limpar_botao = tk.Button(root, text="Limpar Desenho", command=limpar_desenho)
limpar_botao.pack()

# Apos 10 s, finaliza-se a janela, salvando a imagem desenhada
root.after(10000, fechar_janela)
root.mainloop()

# Abre o arquivo da imagem em modo binário
with open('image.png', 'rb') as file:
    # Leia o conteúdo do arquivo
    image_data = file.read()

# Envia a imagem em blocos
client_socket.sendall(image_data)

# Fecha o socket do cliente
client_socket.close()
