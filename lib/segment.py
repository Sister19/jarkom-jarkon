import struct

# Constants 
SYN_FLAG = 0b00000010
ACK_FLAG = 0b00010000
FIN_FLAG = 0b00000001

class SegmentFlag:
    def __init__(self, flag : bytes):
        self.syn = bool(flag & SYN_FLAG)
        self.ack = bool(flag & ACK_FLAG)
        self.fin = bool(flag & FIN_FLAG)
        self.new_bytes = 0b00000000
        
    def get_flag_bytes(self) -> bytes:
        # Convert this object to flag in byte form
        if self.syn:
            self.new_bytes |= SYN_FLAG
        if self.ack:
            self.new_bytes |= ACK_FLAG
        if self.fin:
            self.new_bytes |= FIN_FLAG
        return struct.pack("B", self.new_bytes)

    # to check the flag
    def is_syn(self):
        return bool(self.new_bytes & self.syn)

    def is_ack(self):
        return bool(self.new_bytes & self.ack)

    def is_fin(self):
        return bool(self.new_bytes & self.fin)

        
class Segment:
    # -- Internal Function --
    def __init__(self):
        self.seq_num = 0
        self.ack_num = 0
        self.flag = SegmentFlag(0b00000000)
        self.checksum = 0
        self.data = b""
        # Initalize segment

    def __str__(self):
        # Optional, override this method for easier print(segmentA)
        output = ""
        output += f"Sequence number: {self.seq_num} |   Acknowledgement number: {self.ack_num}\n"
        output += f"Flags: (SYN {self.flag.syn}) (ACK {self.flag.ack}) (FIN {self.flag.fin})\n"
        output += f"Checksum: {hex(self.checksum)}  |   Valid checksum: {self.valid_checksum()}\n"
        output += f"Data payload: {len(self.data)} bytes"
        return output

    def __calculate_checksum(self) -> int:
        # Calculate checksum here, return checksum result
        checksum = 0x0000
        x = 0xFFFF
        checksum = (checksum + self.seq_num) & x
        checksum = (checksum + self.ack_num) & x
        char_flag = struct.unpack("B", self.flag.get_flag_bytes())[0]
        checksum = (checksum + char_flag) & x
        checksum = (checksum + self.checksum) & x
        for i in range(0, len(self.data), 2):
            buffer = self.data[i:i+2]
            if len(buffer) == 1:
                buffer += struct.pack("x")
            chunk = struct.unpack("H", buffer)[0]
            checksum = (checksum + chunk) & x
        checksum = x - checksum
        return checksum

    # -- Setter --        
    def set_seq_num(self, seq_num : int):
        self.seq_num = seq_num
        
    def set_ack_num(self, ack_num : int):
        self.ack_num = ack_num

    def set_payload(self, payload : bytes):
        self.data = payload

    def set_flag(self, flag_list : list):
        x = 0b00000000
        i = 0
        while(i < len(flag_list)):
            x |= flag_list[i]
            i += 1
        self.flag = SegmentFlag(x)
   
    # -- Getter --
    def get_flag(self) -> SegmentFlag:
        return self.flag

    def get_seq_num(self) -> int:
        return self.seq_num
    
    def get_ack_num(self) -> int:
        return self.ack_num

    def get_payload(self) -> bytes:
        return self.data
        
    # -- Marshalling --
    def set_from_bytes(self, src : bytes):
        # From pure bytes, unpack() and set into python variable
        self.seq_num = struct.unpack("I", src[0:4])[0] # 0, 1, 2, 3
        self.ack_num = struct.unpack("I", src[4:8])[0] # 4, 5, 6, 7
        self.flag = SegmentFlag(struct.unpack("B", src[8:9])[0]) # 8
        self.checksum = struct.unpack("H", src[10:12])[0] # 10, 11
        self.data = src[12:] # 12, dst

    def get_bytes(self) -> bytes:
        # Convert this object to pure bytes
        result = b""
        result += struct.pack("I", self.seq_num)
        result += struct.pack("I", self.ack_num)
        result += self.flag.get_flag_bytes()
        result += struct.pack("x")
        self.checksum = self.__calculate_checksum()
        result += struct.pack("H", self.checksum)
        result += self.data
        return result

    # -- Checksum --
    def valid_checksum(self) -> bool:
        # Use __calculate_checksum() and check integrity of this object
        return self.__calculate_checksum() == 0x0000
