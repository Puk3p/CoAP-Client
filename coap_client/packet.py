import json
import struct


class CoAPPacket:
    def __init__(self, version=1, message_type=0, tkl=0, code=0, message_id=0, token=None, options=None, payload=None):
        self.version = version  # 2 bitisori
        self.message_type = message_type  # 2 bitisori
        self.tkl = tkl  # 4 biti tokenul
        self.code = code  # 8 bitisori
        self.message_id = message_id  # 16 biti
        self.token = token if token else b""  # Token (0-8 bytes)
        self.options = options if options else []  # Lista de optiuni
        self.payload = payload if payload else b""  # Payload

    def build(self):
        # header-ul
        version_type_tkl = (self.version << 6) | (self.message_type << 4) | self.tkl
        header = struct.pack("!BBH", version_type_tkl, self.code, self.message_id)

        # Token-ul
        token = self.token if self.tkl == len(self.token) else b""

        # opțiunile
        options_data = b""
        for option_delta, option_value in self.options:
            options_data += self.encode_option(option_delta, option_value)

        # adauag Payload-ul, si l fac 0xff daca e prez
        payload_marker = b"\xFF" if self.payload else b""
        payload = self.payload if self.payload else b""

        # secțiunile
        return header + token + options_data + payload_marker + payload

    def encode_option(self, delta, value):
        delta_byte = delta
        length_byte = len(value)
        return struct.pack("!BB", delta_byte, length_byte) + value

    @staticmethod
    def parse(packet):
        header = packet[:4]
        version_type_tkl, code, message_id = struct.unpack("!BBH", header)
        version = (version_type_tkl >> 6) & 0b11
        message_type = (version_type_tkl >> 4) & 0b11
        tkl = version_type_tkl & 0b1111

        # Token
        token = packet[4:4 + tkl] if tkl > 0 else b""

        # opt si payload
        options_and_payload = packet[4 + tkl:]
        options = []
        payload = b""

        if b"\xFF" in options_and_payload:
            options_part, payload = options_and_payload.split(b"\xFF", 1)
        else:
            options_part = options_and_payload

        # optiunile
        while options_part:
            delta, length = struct.unpack("!BB", options_part[:2])
            value = options_part[2:2 + length]
            options.append((delta, value))
            options_part = options_part[2 + length:]

        return CoAPPacket(version, message_type, tkl, code, message_id, token, options, payload)