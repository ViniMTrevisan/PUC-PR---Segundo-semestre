import socket
import threading
import sys

# Configurações do cliente
ENDEREÇO = '127.0.0.1'
PORTA = 12345

def receber_mensagens(cliente):
    # Recebe mensagens do servidor
    while True:
        try:
            mensagem = cliente.recv(1024).decode('utf-8')
            if not mensagem:
                print("Conexão com o servidor perdida.")
                sys.exit()
            print(mensagem, end='')  # Exibe a mensagem com newline
        except:
            print("Erro ao receber mensagem. Desconectando...")
            cliente.close()
            sys.exit()

def principal():
    # Cria o socket TCP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((ENDEREÇO, PORTA))
    except:
        print("Não foi possível conectar ao servidor.")
        return

    # Envia o nome do cliente
    nome = input("Digite seu nome: ")
    cliente.send(nome.encode('utf-8'))

    # Inicia thread para receber mensagens
    thread_recebimento = threading.Thread(target=receber_mensagens, args=(cliente,))
    thread_recebimento.daemon = True  # Thread termina quando o programa sai
    thread_recebimento.start()

    # Envia mensagens
    while True:
        try:
            mensagem = input()  # Lê entrada do usuário
            if mensagem.strip() == '/sair':
                cliente.send(mensagem.encode('utf-8'))
                break
            cliente.send(f"{mensagem}\n".encode('utf-8'))  # Adiciona newline
        except:
            print("Erro ao enviar mensagem. Desconectando...")
            break

    cliente.close()

if __name__ == "__main__":
    principal()