import socket
import threading

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço local
PORT = 12345        # Porta para conexão
clients = []        # Lista de conexões dos clientes
names = []          # Lista de nomes dos clientes

def broadcast(message, sender_conn=None):
    # Envia a mensagem para todos os clientes, exceto o remetente
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message)
            except:
                client.close()
                remove_client(client)

def remove_client(conn):
    # Remove um cliente da lista
    if conn in clients:
        index = clients.index(conn)
        name = names[index]
        clients.remove(conn)
        names.remove(name)
        broadcast(f"{name} saiu do chat.\n".encode('utf-8'))

def handle_client(conn, addr):
    # Recebe o nome do cliente
    name = conn.recv(1024).decode('utf-8')
    names.append(name)
    clients.append(conn)
    broadcast(f"{name} entrou no chat.\n".encode('utf-8'))  # Notifica entrada

    while True:
        # Recebe mensagens do cliente
        try:
            message = conn.recv(1024).decode('utf-8')
            if not message or message.strip() == '/sair':
                break
            # Adiciona newline à mensagem e retransmite
            broadcast(f"{name}: {message}\n".encode('utf-8'), conn)
        except:
            break
    # Remove o cliente ao desconectar
    remove_client(conn)
    conn.close()

def main():
    # Cria o socket TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Servidor TCP rodando em {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        # Inicia uma thread para cada cliente
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()