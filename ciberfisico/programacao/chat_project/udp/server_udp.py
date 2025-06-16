import socket

HOST = '127.0.0.1'  
PORT = 12346        
clients = []        
names = []          

def broadcast(message, sender_addr):
    for client in clients:
        if client != sender_addr:
            server.sendto(message, client)

def main():
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))
    print(f"Servidor UDP rodando em {HOST}:{PORT}")

    while True:
        data, addr = server.recvfrom(1024)
        message = data.decode('utf-8')

        if addr not in clients:
            names.append(message)  
            clients.append(addr)
            broadcast(f"{message} entrou no chat.\n".encode('utf-8'), addr)
            continue

        if message == '/sair':
            index = clients.index(addr)
            name = names[index]
            clients.remove(addr)
            names.remove(name)
            broadcast(f"{name} saiu do chat.\n".encode('utf-8'), addr)
        else:
            index = clients.index(addr)
            name = names[index]
            broadcast(f"{name}: {message}\n".encode('utf-8'), addr)

if __name__ == "__main__":
    main()