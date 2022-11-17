from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from .segment import Segment

class Connection:
    def __init__(self, ip, port):
        # Init UDP socket
        self.ip = ip
        self.port = port
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((ip, port))
        self.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    def send_data(self, msg : Segment, dest):
        # Send single segment into destination
        self.socket.sendto(msg, dest)

    def listen_single_segment(self) -> Segment:
        # Listen single UDP datagram within timeout and convert into segment
        response, address = self.socket.recvfrom(32768)
        data = Segment()
        data.set_from_bytes(response)
        return data, address, data.valid_checksum()

    def close_socket(self):
        # Release UDP socket
        self.socket.close()

    def set_listen_timeout(self, timeout : float):
        # Set connection timeout
        self.socket.settimeout(timeout)
        