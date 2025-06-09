import socket

print(socket.gethostbyname('google.com'))
print(socket.gethostbyname('www.pucpr.br.'))
print(socket.getfqdn('8.8.8.8'))
print(socket.gethostbyname('www.gmail.com'))
print(socket.gethostbyname_ex('www.gmail.com'))
print(socket.gethostbyname('dns.google'))
print(socket.gethostbyname_ex('dns.google'))