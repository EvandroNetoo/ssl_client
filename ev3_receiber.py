import socket
from protobufs import grSim_Commands_pb2


# Configurações do servidor
UDP_IP = '127.0.0.1'
UDP_PORT = 20010

# Cria o socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


while True:
    data, addr = sock.recvfrom(100000)
    print(f'Recebido de {addr}: {grSim_Commands_pb2.grSim_Commands().FromString(data).robot_commands}')
