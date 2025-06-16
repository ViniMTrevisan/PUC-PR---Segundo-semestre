import socket
import threading

HOST = '127.0.0.1'  
PORT = 12346        

def receive_messages(client):
    while True:
        message, _ = client.recvfrom(1024)
        print(message.decode('utf-8'), end='')

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    name = input("Digite seu nome: ")
    client.sendto(name.encode('utf-8'), (HOST, PORT))

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    while True:
        message = input()
        client.sendto(message.encode('utf-8'), (HOST, PORT))
        if message == '/sair':
            break

    client.close()

if __name__ == "__main__":
    main()