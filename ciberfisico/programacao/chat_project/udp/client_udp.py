import socket
import threading

# Configurações do cliente
HOST = '127.0.0.1'  # Endereço do servidor
PORT = 12346        # Porta do servidor

def receive_messages(client):
    # Recebe mensagens do servidor
    while True:
        message, _ = client.recvfrom(1024)
        print(message.decode('utf-8'), end='')

def main():
    # Cria o socket UDP
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Envia o nome do cliente
    name = input("Digite seu nome: ")
    client.sendto(name.encode('utf-8'), (HOST, PORT))

    # Inicia uma thread para receber mensagens
    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    # Envia mensagens
    while True:
        message = input()
        client.sendto(message.encode('utf-8'), (HOST, PORT))
        if message == '/sair':
            break

    client.close()

if __name__ == "__main__":
    main()