from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from .segment import Segment

class Connection:
    def __init__(self, ip : str, port : int):
        # Init UDP socket
        self.ip = ip
        self.port = port
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((ip, port))
        self.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    def send_data(self, msg : Segment,  dest: tuple[str, int]):
        # Send single segment into destination
        self.socket.sendto(msg, dest)

    def listen_single_segment(self) -> Segment:
        response, address = self.socket.recvfrom(32768)
        return response, address
        # Listen single UDP datagram within timeout and convert into segment

    def close_socket(self):
        # Release UDP socket
        self.socket.close()

