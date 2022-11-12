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
        self.newBytes = 0b00000000
        
    def get_flag_bytes(self) -> bytes:
        
        if self.syn:
            self.newBytes |= SYN_FLAG
        if self.ack:
            self.newBytes |= ACK_FLAG
        if self.fin:
            self.newBytes |= FIN_FLAG
        return struct.pack("B", self.newBytes)
            
        # Convert this object to flag in byte form
        
class Segment:
    # -- Internal Function --
    def __init__(self):
        self.sequence = 0
        self.ackNum = 0
        self.flag = SegmentFlag(0b00000000)
        self.chksum = 0
        self.data = b""
        # Initalize segment

    def __str__(self):
        # Optional, override this method for easier print(segmentA)
        output = ""
        output += f"{'Sequence number':24} | {self.sequence}\n"
        output += f"{'Acknowledgement number':24} | {self.ackNum}\n"
        output += f"{'Flags':24} | (SYN {self.flag.syn}) (ACK {self.flag.ack}) (FIN {self.flag.fin})\n"
        output += f"{'Checksum':24} | {hex(self.chksum)}\n"
        output += f"{'Valid checksum':24} | {self.valid_checksum()}\n"
        output += f"{'Data payload':24} | {len(self.data)} Bytes"
        return output

    def __calculate_checksum(self) -> int:
        # Calculate checksum here, return checksum result
        checksum = 0x0000
        x = 0xFFFF

        checksum = (checksum + self.sequence) & x
        checksum = (checksum + self.ackNum) & x
        char_flag =  struct.unpack("B", self.flag.get_flag_bytes())[0]
        checksum = (checksum + char_flag) & x
        checksum = (checksum + self.chksum) & x
        for i in range(0, len(self.data), 2):
            buffer         = self.data[i:i+2]
            if len(buffer) == 1:
                buffer += struct.pack("x")
            chunk         = struct.unpack("H", buffer)[0]
            checksum = (checksum + chunk) & x
        checksum = x - checksum
        return checksum


    # -- Setter --
    def set_header(self, header : dict):
        self.sequence = header["sequence"]
        self.ackNum = header["ack"]

    def set_payload(self, payload : bytes):
        self.data = payload

    def set_flag(self, flag_list : list):
        x = 0b00000000
        for i in range(len(flag_list)):
            x |= flag_list[i]
        self.flag     = SegmentFlag(x)


    # -- Getter --
    def get_flag(self) -> SegmentFlag:
        return self.flag

    def get_header(self) -> dict:
        return {"sequence" : self.sequence, "ack" : self.ackNum}

    def get_payload(self) -> bytes:
        return self.data
        


    # -- Marshalling --
    def set_from_bytes(self, src : bytes):
        self.sequence = struct.unpack("I", src[0:4])[0] # 0, 1, 2, 3
        self.ackNum = struct.unpack("I", src[4:8])[0] # 4, 5, 6, 7
        self.flag = SegmentFlag(struct.unpack("B", src[8:9])[0]) # 8
        self.chksum = struct.unpack("H", src[10:12])[0] # 10, 11
        self.data = src[12:] # 12, dst
        # From pure bytes, unpack() and set into python variable

    def get_bytes(self) -> bytes:
        result = b""
        result += struct.pack("I", self.sequence)
        result += struct.pack("I", self.sequence)
        result += struct.pack("B", self.flag.get_flag_bytes())
        result += struct.pack("x")
        result += struct.pack("H", self.chksum())
        return result
        # Convert this object to pure bytes


    # -- Checksum --
    def valid_checksum(self) -> bool:
        # Use __calculate_checksum() and check integrity of this object
        return self.__calculate_checksum() == 0x0000
