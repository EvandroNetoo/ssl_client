import socket
import struct
from protobufs import ssl_vision_wrapper_pb2
from command_sender import CommandsSender


class VisionReceiver:
    UDP_IP = "224.5.23.2"
    UDP_PORT = 10020

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    mreq = struct.pack("4sl", socket.inet_aton(UDP_IP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    @classmethod
    def run(cls):
        while True:
            data, _ = cls.sock.recvfrom(2048)
            data = ssl_vision_wrapper_pb2.SSL_WrapperPacket().FromString(data)

            if data.HasField("geometry"):
                # print(data.geometry)
                ...

            if data.HasField("detection"):
                CommandsSender.update_data(data.detection)
