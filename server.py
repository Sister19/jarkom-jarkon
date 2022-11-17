from lib.connection import Connection
from lib.segment import Segment
import lib.segment as segment
from lib.argparser import Arguments
import lib.argparser as argument

class Server:
    def __init__(self):
        # Init server
        self.args = Arguments()
        self.args.add_args("port", "broadcast port", int)
        self.args.add_args("path", "path file input", str)
        self.port = self.args.get_attribute("port")
        self.connection = Connection("127.0.0.1", self.port)
        self.path = self.args.get_attribute("path")

    def listen_for_clients(self):
        # Waiting client for connect
        pass

    def start_file_transfer(self):
        # Handshake & file transfer for all client
        pass

    def file_transfer(self, client_addr : tuple):
        # File transfer, server-side, Send file to 1 client
        pass

    def three_way_handshake(self, client_addr: tuple) -> bool:
       # Three way handshake, server-side, 1 client
       pass


if __name__ == '__main__':
    main = Server()
    main.listen_for_clients()
    main.start_file_transfer()
