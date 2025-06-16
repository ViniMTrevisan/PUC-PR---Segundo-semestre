import socket
import threading
import sys

# Configurações do cliente
HOST = '127.0.0.1'
PORT = 12346

def receive_messages(client):
    # Recebe mensagens do servidor
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode('utf-8'), end='')
        except:
            print("Erro ao receber mensagem. Desconectando...")
            sys.exit()

def main():
    # Cria o socket UDP
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Envia o nome do cliente
    name = input("Digite seu nome: ")
    client.sendto(name.encode('utf-8'), (HOST, PORT))

    # Inicia thread para receber mensagens
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True
    receive_thread.start()

    # Envia mensagens
    while True:
        try:
            message = input()
            if message.strip() == '/sair':
                client.sendto(message.encode('utf-8'), (HOST, PORT))
                break
            client.sendto(f"{message}\n".encode('utf-8'), (HOST, PORT))
        except:
            print("Erro ao enviar mensagem. Desconectando...")
            break

    client.close()

if __name__ == "__main__":
    main()