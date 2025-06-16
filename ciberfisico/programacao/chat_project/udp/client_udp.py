import socket
import threading
import sys

# Configurações do cliente
localhost = '127.0.0.1'
porta = 12346

def receber_mensagens(cliente):
    # Recebe mensagens do servidor
    while True:
        try:
            mensagem, _ = cliente.recvfrom(1024)
            print(mensagem.decode('utf-8'), end='')
        except:
            print("Erro ao receber mensagem. Desconectando...")
            sys.exit()

def principal():
    # Cria o socket UDP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Envia o nome do cliente
    nome = input("Digite seu nome: ")
    cliente.sendto(nome.encode('utf-8'), (localhost, porta))

    # Inicia thread para receber mensagens
    thread_recebimento = threading.Thread(target=receber_mensagens, args=(cliente,))
    thread_recebimento.daemon = True
    thread_recebimento.start()

    # Envia mensagens
    while True:
        try:
            mensagem = input()
            if mensagem.strip() == '/sair':
                cliente.sendto(mensagem.encode('utf-8'), (localhost, porta))
                break
            cliente.sendto(f"{mensagem}\n".encode('utf-8'), (localhost, porta))
        except:
            print("Erro ao enviar mensagem. Desconectando...")
            break

    cliente.close()

if __name__ == "__main__":
    principal()