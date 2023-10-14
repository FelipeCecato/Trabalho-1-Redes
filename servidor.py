import socket
import tkinter as tk
from tkinter import Entry, Button, Label
from PIL import Image
from PIL import ImageTk
import threading
import os
from tkinter import Toplevel

# Função para lidar com um cliente
def handle_client(client_socket):

    # Função para verificar a tentativa
    def verificar_tentativa(palavra_correta, entry):
        tentativa = entry.get()
        if tentativa == palavra_correta:
            resultado.config(text="Parabéns! Você acertou!")
        else:
            resultado.config(text="Tente novamente.")
    # Estado do jogo
    estado = 0

    #variaveis para o jogo:
    thread_num = threading.current_thread().name  # Obtém o nome da thread (um número)
    image_filename = f"imagem{thread_num}.png"  # Nome da imagem baseado no número da thread

    # Loop principal
    while True:
        if estado == 0: # Aberto para conexões
            print(f"Conexão recebida de jogador: {client_socket.getpeername()}")

            # Receba dados do cliente
            data = client_socket.recv(1024)
            palavra_correta = data.decode('utf-8')

            # Envie uma resposta de volta ao cliente
            response = "Jogo iniciado! Hora de desenhar!"
            client_socket.send(response.encode('utf-8'))

            estado = 1 # Muda de estado
        elif estado == 1: # Esperando para receber a imagem

            # Escreve os bytes recebidos no arquivo de imagem
            with open(image_filename, 'wb') as file:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    file.write(data)

            # Cria janela para abrir a imagem
            root = tk.Tk()
            root.title("Imagem Gerada")

            # Abre o arquivo
            image = Image.open(image_filename)
            photo = ImageTk.PhotoImage(image)

            # Adiciona um label
            label = Label(root, image=photo)
            label.pack()
            
            # Adiciona a entrada do texto com a tentativa do usuario
            entry = Entry(root, width=20)
            entry.pack()

            # Botao de verificacao
            verificar_button = Button(root, text="Verificar", command=lambda: verificar_tentativa(palavra_correta, entry))
            verificar_button.pack()

            # Mostra o resultado da tentativa no label
            resultado = Label(root, text="")
            resultado.pack()

            # Abre a janela
            root.mainloop()

            estado = 2 # Agora o usuario já está respondendo
    client_socket.close()

# Defina o endereço e a porta em que o servidor irá escutar
HOST = '127.0.0.1'
PORT = 12380

# Crie um socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Faça o servidor escutar no endereço e porta especificados
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Servidor escutando em {HOST}:{PORT}")
estado = 0
palavra_correta = ""

# Contador para gerar nomes únicos de threads
thread_counter = 0

while True:
    # Aceita conexões de clientes
    client_socket, client_address = server_socket.accept()
    print(f"Conexão recebida de jogador: {client_address}")

    # Cria e incia thread
    thread_counter += 1
    thread_name = str(thread_counter)
    client_handler = threading.Thread(target=handle_client, args=(client_socket,), name=thread_name)
    client_handler.start()
