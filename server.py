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


    def listen_for_clients(self):
        # Waiting client for connect
        self.connectionList = []
        while True:
            response, address, valid = self.connection.listen_single_segment()         
            if (response.get_flag().syn and valid and not(address in self.connectionList)):
                self.connectionList.append(address)
                print(f"[!] Client ({address[0]}:{address[1]}) found")
                nextClient = input("[?] Listen more? (y/n) ")
                if nextClient.lower() != 'y':
                    break


    def start_file_transfer(self):
        # Handshake & file transfer for all client
        print("\n[!] Initiating three way handshake with clients...")
        failed_handshake_addr = []
        for client_addr in self.connectionList:
            print(f"[!] Sending SYN-ACK to {client_addr[0]}:{client_addr[1]}")
            success = self.three_way_handshake(client_addr)
            print(success)
            if not success:
                failed_handshake_addr.append(client_addr)
        for client in failed_handshake_addr:
            self.connectionList.remove(client)
        print("\n[!] Commencing file transfer...")
        for client_addr in self.connectionList:
            self.file_transfer(client_addr)


    def file_transfer(self, client_addr : tuple):
        # File transfer, server-side, Send file to 1 client
        f = open(self.path,"rb")
        f.seek(0,2)
        size = f.tell()
        Total = math.ceil(size / 32768)
        print(Total)
        # File transfer, server-side, Send file to 1 client
        self.connection.set_listen_timeout(100)
        print(f"[!] Sending file to {client_addr[0]}:{client_addr[1]}...")
        print(f"[!] Sending file content...")

        seqWindow = min(4, Total)
        seqBase = 0

        while seqBase < Total:
            
            for i in range(seqWindow - seqBase):
                # send to client
                Dict = {}
                Dict = dict({"sequence": seqBase + i, "ack": seqBase})
                
                print(f"[Segment SEQ={seqBase + i + 1}] Sent")
                data = Segment()
                f.seek(32756 * (seqBase + i))
                data.set_payload(f.read(32756))
                data.set_seq_num(seqBase + i)
                data.set_ack_num(seqBase)
                data.set_flag([ACK_FLAG])
                self.connection.send_data(data.get_bytes(), client_addr)

            for i in range(seqWindow - seqBase):
                try:
                    # receive from client
                    print(f"[Segment SEQ={seqBase + 1}]", end=' ')
                    response, responseAddress, valid= self.connection.listen_single_segment()
                    if valid and client_addr == responseAddress and response.get_flag().ack:
                        if (response.ack_num == seqBase):
                            print('Acked')
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
                    print(f"[!] Client {client_addr[0]}:{client_addr[1]} Timeout")

        print(f"[!] Successfully sent file to {client_addr[0]}:{client_addr[1]}")
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
            print(f"[!] Handshake success with {client_addr[0]}:{client_addr[1]}")
            return True
        else:
            print("[!] Invalid response : Client ACK handshake response invalid")
            print(f"[!] Handshake failed with {client_addr[0]}:{client_addr[1]}")
            return False


if __name__ == '__main__':
    main = Server()
    main.listen_for_clients()
    main.start_file_transfer()
