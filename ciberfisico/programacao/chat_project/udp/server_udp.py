import socket

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço local
PORT = 12346        # Porta (diferente do TCP para evitar conflitos)
clients = []        # Lista para armazenar endereços dos clientes
names = []          # Lista para armazenar nomes dos clientes

def broadcast(message, sender_addr):
    # Envia a mensagem para todos os clientes, exceto o remetente
    for client in clients:
        if client != sender_addr:
            server.sendto(message, client)

def main():
    # Cria o socket UDP
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))
    print(f"Servidor UDP rodando em {HOST}:{PORT}")

    while True:
        # Recebe mensagem e endereço do cliente
        data, addr = server.recvfrom(1024)
        message = data.decode('utf-8')

        # Se o endereço não está na lista, é um novo cliente
        if addr not in clients:
            names.append(message)  # O primeiro dado é o nome
            clients.append(addr)
            broadcast(f"{message} entrou no chat.\n".encode('utf-8'), addr)
            continue

        # Verifica se é o comando /sair
        if message == '/sair':
            index = clients.index(addr)
            name = names[index]
            clients.remove(addr)
            names.remove(name)
            broadcast(f"{name} saiu do chat.\n".encode('utf-8'), addr)
        else:
            # Envia a mensagem com o nome do cliente
            index = clients.index(addr)
            name = names[index]
            broadcast(f"{name}: {message}\n".encode('utf-8'), addr)

if __name__ == "__main__":
    main()