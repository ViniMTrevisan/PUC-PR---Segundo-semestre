import socket

# Configurações do servidor
ENDEREÇO = '127.0.0.1'
PORTA = 12346
clientes = []  # Lista de endereços dos clientes
nomes = []     # Lista de nomes dos clientes

def retransmitir(mensagem, endereço_remetente=None):
    # Envia a mensagem para todos os clientes, exceto o remetente
    for cliente in clientes:
        if cliente != endereço_remetente:
            servidor.sendto(mensagem, cliente)

def principal():
    # Cria o socket UDP
    global servidor
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((ENDEREÇO, PORTA))
    print(f"Servidor UDP rodando em {ENDEREÇO}:{PORTA}")

    while True:
        # Recebe mensagem e endereço do cliente
        dados, endereço = servidor.recvfrom(1024)
        mensagem = dados.decode('utf-8')

        # Se o endereço não está na lista, é um novo cliente
        if endereço not in clientes:
            nomes.append(mensagem)
            clientes.append(endereço)
            retransmitir(f"{mensagem} entrou no chat.\n".encode('utf-8'), endereço)
            continue

        # Verifica se é o comando /sair
        if mensagem.strip() == '/sair':
            índice = clientes.index(endereço)
            nome = nomes[índice]
            clientes.remove(endereço)
            nomes.remove(nome)
            retransmitir(f"{nome} saiu do chat.\n".encode('utf-8'), endereço)
        else:
            # Envia a mensagem com o nome do cliente
            índice = clientes.index(endereço)
            nome = nomes[índice]
            retransmitir(f"{nome}: {mensagem}\n".encode('utf-8'), endereço)

if __name__ == "__main__":
    principal()