import lib.connection
from lib.segment import Segment
import lib.segment as segment
from lib.connection import Connection
from lib.argparser import Arguments
import lib.argparser as argument

IP_SERVER = "127.0.0.1"
PORT_SERVER = 54321
IP_CLIENT = "127.0.0.1"

SYN_FLAG = 0b00000010
ACK_FLAG = 0b00010000
FIN_FLAG = 0b00000001

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
        #initialize connection
        self.connection = Connection(self.clientAddress[0], self.clientAddress[1])
        print(f"Client started at {self.connection.ip}:{self.connection.port}")
        print("[!] Initiating three way handshake...")
        self.syn_request()
        self.syn_ack()
        return self
        
    
    def send_flag(self, flag: list):
        packet_to_send = Segment()
        packet_to_send.set_flag(flag)
        self.connection.send_data(packet_to_send.get_bytes(), self.serverAddress)

    def syn_request(self):
        print(f"[!] [Handshake] Sending broadcast SYN request to port {self.serverAddress[1]}")
        self.send_flag([SYN_FLAG])

    def listen_from_server(self):
        self.connection.set_listen_timeout(100)
        response, address, valid = self.connection.listen_single_segment()
        return address, response, valid

    def syn_ack(self):
        print("[!] [Handshake] Waiting for response...")
        _, result, check = self.listen_from_server()
        if(check and result.get_flag().syn and result.get_flag().ack):
            self.send_flag([ACK_FLAG])
            print(f"[S] Getting response from {self.serverAddress[0]}:{self.serverAddress[1]}")
        else:
            print("[!] Checksum failed")
            
    def send_ack(self, req_num, address):
        ack_resp = Segment()
        ack_resp.set_flag([ACK_FLAG])
        ack_resp.set_ack_num(req_num)
        self.connection.send_data(ack_resp.get_bytes(), address)

    def listen_file_transfer(self):
        print("[!] File transfering...")
        file_data = dict()
        req_num = 0
        while True:
            response, address, check = self.connection.listen_single_segment()
            if check and address == self.serverAddress:
                if req_num == response.sequence:
                    print(f"[Segment SEQ={req_num + 1}] Received, Ack sent")
                    self.send_ack(req_num, address)
                    file_data[req_num] = response.data
                    req_num += 1
                elif response.get_flag().fin:
                    print(f"[!] Successfully received file")
                    with open(self.path, 'wb+') as file:
                        i = 0
                        keys = list(file_data)
                        loop_range = len((file_data.keys()))
                        while(i < loop_range):
                            file.write(file_data[keys[i]])
                            i+=1
                        return self
                else:
                    print(f'[Segment SEQ={req_num + 1}] Segment damaged. Ack prev sequence number.')
                    req_num = response.ackNum
            elif not check:
                print(f'[Segment SEQ={req_num + 1}] Checksum failed. Ack prev sequence number.')
            else:
                print(check, address)


    def listen(self):
        assert self.connection != None

        response, address, valid = self.connection.listen_single_segment()
        return address, response, valid

    def sendFlag(self, flags: list):
        assert self.connection != None

        packet = Segment()
        packet.set_flag(flags)
        self.connection.send_data(packet.get_bytes(), self.serverAddress)

    def close(self):
        assert self.connection != None
        self.connection.close()
        self.connection = None
        return self

if __name__ == '__main__':
    main = Client()
    main.three_way_handshake()
    main.listen_file_transfer()
