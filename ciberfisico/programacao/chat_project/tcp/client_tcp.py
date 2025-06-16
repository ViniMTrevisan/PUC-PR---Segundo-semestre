import socket
import threading

HOST = '127.0.0.1'  
PORT = 12345        

def receive_messages(client):
    while True:
        message = client.recv(1024).decode('utf-8')
        if not message:
            break
        print(message, end='')

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))  

    name = input("Digite seu nome: ")
    client.send(name.encode('utf-8'))

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    while True:
        message = input()
        client.send(message.encode('utf-8'))
        if message == '/sair':
            break

    client.close()

if __name__ == "__main__":
    main()