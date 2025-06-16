import socket

# Configurações do servidor
localhost = '127.0.0.1'
PORTA = 12346
clientes = []  # Lista de localhosts dos clientes
nomes = []     # Lista de nomes dos clientes

def retransmitir(mensagem, localhost_remetente=None):
    # Envia a mensagem para todos os clientes, exceto o remetente
    for cliente in clientes:
        if cliente != localhost_remetente:
            servidor.sendto(mensagem, cliente)

def principal():
    # Cria o socket UDP
    global servidor
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((localhost, PORTA))
    print(f"Servidor UDP rodando em {localhost}:{PORTA}")

    while True:
        # Recebe mensagem e localhost do cliente
        dados, localhost = servidor.recvfrom(1024)
        mensagem = dados.decode('utf-8')

        # Se o localhost não está na lista, é um novo cliente
        if localhost not in clientes:
            nomes.append(mensagem)
            clientes.append(localhost)
            retransmitir(f"{mensagem} entrou no chat.\n".encode('utf-8'), localhost)
            continue

        # Verifica se é o comando /sair
        if mensagem.strip() == '/sair':
            índice = clientes.index(localhost)
            nome = nomes[índice]
            clientes.remove(localhost)
            nomes.remove(nome)
            retransmitir(f"{nome} saiu do chat.\n".encode('utf-8'), localhost)
        else:
            # Envia a mensagem com o nome do cliente
            índice = clientes.index(localhost)
            nome = nomes[índice]
            retransmitir(f"{nome}: {mensagem}\n".encode('utf-8'), localhost)

if __name__ == "__main__":
    principal()