import socket
import threading

HOST = '127.0.0.1'  
PORT = 12345        
clients = []        
names = []          

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            client.send(message)

def handle_client(conn, addr):
    name = conn.recv(1024).decode('utf-8')
    names.append(name)  
    clients.append(conn)  
    broadcast(f"{name} entrou no chat.\n".encode('utf-8'), None)

    while True:
        message = conn.recv(1024)
        if message.decode('utf-8').strip() == '/sair':
            break
        broadcast(f"{name}: {message.decode('utf-8')}".encode('utf-8'), conn)

    clients.remove(conn)
    names.remove(name)
    broadcast(f"{name} saiu do chat.\n".encode('utf-8'), None)
    conn.close()

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))  
    server.listen(5)           
    print(f"Servidor TCP rodando em {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()  
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()