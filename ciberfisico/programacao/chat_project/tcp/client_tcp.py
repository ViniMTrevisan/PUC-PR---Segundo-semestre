import socket
import threading

# Configurações do cliente
HOST = '127.0.0.1'  # Endereço do servidor
PORT = 12345        # Porta do servidor

def receive_messages(client):
    # Recebe mensagens do servidor
    while True:
        message = client.recv(1024).decode('utf-8')
        if not message:
            break
        print(message, end='')

def main():
    # Cria o socket TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))  # Conecta ao servidor

    # Envia o nome do cliente
    name = input("Digite seu nome: ")
    client.send(name.encode('utf-8'))

    # Inicia uma thread para receber mensagens
    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    # Envia mensagens
    while True:
        message = input()
        client.send(message.encode('utf-8'))
        if message == '/sair':
            break

    client.close()

if __name__ == "__main__":
    main()