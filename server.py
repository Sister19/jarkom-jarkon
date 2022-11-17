from lib.connection import Connection
from lib.segment import Segment
from lib.argparser import Arguments
import socket
import math


SYN_FLAG = 0b00000010
ACK_FLAG = 0b00010000
FIN_FLAG = 0b00000001

class Server:
    def __init__(self):
        # Init server
        self.args = Arguments()
        self.args.add_args("port", "broadcast port", int)
        self.args.add_args("path", "path file input", str)
        self.port = self.args.get_attribute("port")
        self.connection = Connection("127.0.0.1", self.port)
        self.path = self.args.get_attribute("path")
        self.active = 1

    def countSize(self, path):
        f = open(path,"rb")
        f.seek(0,2)
        self.tot = f.tell()
        return self.tot

    def listen_for_clients(self):
        # Waiting client for connect
        self.connectionList = []
        while True:
            print(f"[!] Listening to broadcast address for clients.")
            response, address, valid = self.connection.listen_single_segment()         
            if (response.get_flag().syn and valid and not(address in self.connectionList)):
                self.connectionList.append(address)
                print(f"\n[!] Received request from ({address[0]}:{address[1]})")
                nextClient = input("[?] Listen more? (y/n) ")
                if nextClient.lower() != 'y':
                    print(f"\nClient list: ")
                    for i in range (len(self.connectionList)):
                        print(f"{i + 1}. {self.connectionList[i][0]}:{self.connectionList[i][1]}\n")
                    break


    def start_file_transfer(self):
        # Handshake & file transfer for all client
        print("[!] Commencing file transfer...")
        failed_handshake_addr = []
        for i in range(len(self.connectionList)):
            print(f"[!] [Handshake] Handshake to client {i + 1}...\n")
            print("...")
            print("(Three way handshake)")
            print("...")
            success = self.three_way_handshake(self.connectionList[i])
            if not success:
                failed_handshake_addr.append(self.connectionList[i])
            if success:
                self.file_transfer(self.connectionList[i])
                self.active += 1
        for client in failed_handshake_addr:
            self.connectionList.remove(client)


    def file_transfer(self, client_addr : tuple):
        # File transfer, server-side, Send file to 1 client
        f = open(self.path,"rb")
        f.seek(0,2)
        size = f.tell()
        Total = math.ceil(size / 32768)
        print(f"[!] [Client {self.active}] Initiating file transfer...")

        seqWindow = min(4, Total)
        seqBase = 0

        while seqBase < Total:
                for i in range(seqWindow - seqBase):
                    # send to client
                    print(f"[!] [Client {self.active}] [Num={seqBase + i + 1}] Sending segment to client...")
                    data = Segment()
                    f.seek(32756 * (seqBase + i))
                    data.set_payload(f.read(32756))
                    data.set_seq_num(seqBase + i)
                    data.set_ack_num(seqBase)
                    data.set_flag([ACK_FLAG])
                    self.connection.send_data(data.get_bytes(), client_addr)

                for i in range(seqWindow - seqBase):
                    # receive from client
                    try:
                        self.connection.socket.settimeout(0.5)
                        print(f"[!] [Client {self.active}] [Num={seqBase + i}] Sending segment to client...")
                        response, responseAddress, valid= self.connection.listen_single_segment()
                        if valid and client_addr == responseAddress and response.get_flag().ack:
                            if (response.ack_num == seqBase):
                                print(f'ACK received, new sequence base = {seqBase + 2}')
                                seqBase += 1
                                seqWindow = min(
                                    4 + seqBase, Total)
                            else:
                                print('NOT ACKED. Duplicate Ack found')
                        elif responseAddress != client_addr:
                            print('NOT ACKED. Address does not match')
                        elif not valid:
                            print('NOT ACKED. Checksum failed')
                        else:
                            print('NOT ACKED')
                    except socket.timeout:
                        print(f"[!] [Client {self.active}] [Num={seqBase + i}] [Timeout] ACK response timeout")

        print(f"[!] [Client {self.active}] [CLS] File transfer completed, initiating closing connection...")
        print(f"[!] [Client {self.active}] [FIN] Sending FIN...")
        print(f"...")
        print(f"(Closing connection)")
        print(f"...")
        data = Segment()
        packet = Segment()
        packet.set_flag([FIN_FLAG])
        self.connection.send_data(packet.get_bytes(), client_addr)


    def three_way_handshake(self, client_addr: tuple) -> bool:
       # Three way handshake, server-side, 1 client
        synack_resp = Segment()
        synack_resp.set_flag([SYN_FLAG, ACK_FLAG])
        self.connection.send_data(synack_resp.get_bytes(), client_addr)

        response, address, valid = self.connection.listen_single_segment()

        if address == client_addr and response.get_flag().ack and valid:
            return True
        else:
            print("[!] Invalid response : Client ACK handshake response invalid")
            print(f"[!] Handshake failed with {client_addr[0]}:{client_addr[1]}")
            return False


if __name__ == '__main__':
    main = Server()
    print(f"[!] Server started at localhost {main.port}")
    print(f"[!] Source file | {main.path} | {main.countSize(main.path)} bytes")
    main.listen_for_clients()
    main.start_file_transfer()
