import socket
import threading
import sys

# Configurações do cliente
HOST = '127.0.0.1'
PORT = 12345

def receive_messages(client):
    # Recebe mensagens do servidor
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                print("Conexão com o servidor perdida.")
                sys.exit()
            print(message, end='')  # Exibe a mensagem com newline
        except:
            print("Erro ao receber mensagem. Desconectando...")
            client.close()
            sys.exit()

def main():
    # Cria o socket TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except:
        print("Não foi possível conectar ao servidor.")
        return

    # Envia o nome do cliente
    name = input("Digite seu nome: ")
    client.send(name.encode('utf-8'))

    # Inicia thread para receber mensagens
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True  # Thread termina quando o programa sai
    receive_thread.start()

    # Envia mensagens
    while True:
        try:
            message = input()  # Lê entrada do usuário
            if message.strip() == '/sair':
                client.send(message.encode('utf-8'))
                break
            client.send(f"{message}\n".encode('utf-8'))  # Adiciona newline
        except:
            print("Erro ao enviar mensagem. Desconectando...")
            break

    client.close()

if __name__ == "__main__":
    main()