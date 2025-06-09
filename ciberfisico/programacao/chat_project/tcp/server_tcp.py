import socket
import threading

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço local
PORT = 12345        # Porta para conexão
clients = []        # Lista para armazenar conexões dos clientes
names = []          # Lista para armazenar nomes dos clientes

def broadcast(message, sender_conn):
    # Envia a mensagem para todos os clientes, exceto o remetente
    for client in clients:
        if client != sender_conn:  # Não envia para o remetente
            client.send(message)

def handle_client(conn, addr):
    # Recebe o nome do cliente
    name = conn.recv(1024).decode('utf-8')
    names.append(name)  # Adiciona o nome à lista
    clients.append(conn)  # Adiciona a conexão à lista
    broadcast(f"{name} entrou no chat.\n".encode('utf-8'), None)

    while True:
        # Recebe mensagens do cliente
        message = conn.recv(1024)
        if message.decode('utf-8').strip() == '/sair':
            break
        broadcast(f"{name}: {message.decode('utf-8')}".encode('utf-8'), conn)

    # Remove o cliente ao desconectar
    clients.remove(conn)
    names.remove(name)
    broadcast(f"{name} saiu do chat.\n".encode('utf-8'), None)
    conn.close()

def main():
    # Cria o socket TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))  # Associa o socket ao endereço e porta
    server.listen(5)           # Permite até 5 conexões em espera
    print(f"Servidor TCP rodando em {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()  # Aceita nova conexão
        # Cria uma thread para gerenciar o cliente
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()