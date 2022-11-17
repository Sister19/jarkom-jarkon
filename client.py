import lib.connection
from lib.segment import Segment
import lib.segment as segment
from lib.connection import Connection
from lib.argparser import Arguments
import lib.argparser as argument

IP_SERVER = "127.0.0.1"
PORT_SERVER = 54321
IP_CLIENT = "127.0.0.1"

class Client:
    def __init__(self):
        # Init client
        self.args = Arguments()
        self.args.add_args("port", "client port", int)
        self.args.add_args("bc_port", "broadcast port", int)
        self.args.add_args("path", "output path of file", str)
        self.client_addr = (IP_CLIENT, self.args.get_attribute("port"))
        self.server_addr = (IP_SERVER, self.args.get_attribute("bc_port"))
        self.path = self.args.get_attribute("path")
        self.connection = None

    def three_way_handshake(self):
        # Three Way Handshake, client-side
        pass

    def listen_file_transfer(self):
        # File transfer, client-side
        pass


if __name__ == '__main__':
    main = Client()
    main.three_way_handshake()
    main.listen_file_transfer()
