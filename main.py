import socket
import json

# Configuracoes do servidor
UDP_IP = '172.16.41.67'
UDP_PORT = 20010

# Cria o socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(100000)
    data=json.loads(data.decode())
    print(data)
