import socket
import threading

# Configurações do servidor
ENDEREÇO = '127.0.0.1'  # Endereço local
PORTA = 12345           # Porta para conexão
clientes = []           # Lista de conexões dos clientes
nomes = []              # Lista de nomes dos clientes

def retransmitir(mensagem, conexão_remetente=None):
    # Envia a mensagem para todos os clientes, exceto o remetente
    for cliente in clientes:
        if cliente != conexão_remetente:
            try:
                cliente.send(mensagem)
            except:
                cliente.close()
                remover_cliente(cliente)

def remover_cliente(conexão):
    # Remove um cliente da lista
    if conexão in clientes:
        índice = clientes.index(conexão)
        nome = nomes[índice]
        clientes.remove(conexão)
        nomes.remove(nome)
        retransmitir(f"{nome} saiu do chat.\n".encode('utf-8'))

def gerenciar_cliente(conexão, endereço):
    # Recebe o nome do cliente
    nome = conexão.recv(1024).decode('utf-8')
    nomes.append(nome)
    clientes.append(conexão)
    retransmitir(f"{nome} entrou no chat.\n".encode('utf-8'))  # Notifica entrada

    while True:
        # Recebe mensagens do cliente
        try:
            mensagem = conexão.recv(1024).decode('utf-8')
            if not mensagem or mensagem.strip() == '/sair':
                break
            # Adiciona newline à mensagem e retransmite
            retransmitir(f"{nome}: {mensagem}\n".encode('utf-8'), conexão)
        except:
            break
    # Remove o cliente ao desconectar
    remover_cliente(conexão)
    conexão.close()

def principal():
    # Cria o socket TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((ENDEREÇO, PORTA))
    servidor.listen(5)
    print(f"Servidor TCP rodando em {ENDEREÇO}:{PORTA}")

    while True:
        conexão, endereço = servidor.accept()
        # Inicia uma thread para cada cliente
        thread = threading.Thread(target=gerenciar_cliente, args=(conexão, endereço))
        thread.start()

if __name__ == "__main__":
    principal()