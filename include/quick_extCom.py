from dataclasses import dataclass

import msgpack
import socket

@dataclass
class QuickExtCom:
    def __init__(self, hostAddress='localhost', hostPort=65432, baudrate=57600, **kwargs):
        self.com = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.com.bind((hostAddress, hostPort))
        except:
            print(f"binding failed")
            return

        try:
            self.com.listen()
            print(f"listening on {hostAddress}:{port}")
        except:
            print(f"failed to listen")
            return

        try:
            self.conn, self.addr = self.com.accept()
            print(f"connection from {self.addr}")
        except:
            print(f"failed to accept connection")

        print(f"REDIS ENGAGED")
        super().__init__(**kwargs)

    def unpackVicon(self, state):
        try:
            self.unpacker = msgpack.Unpacker(raw=False)

            _chunk = self.conn.recv(2048)
            
            self.unpacker.feed(_chunk)

            for _msg in self.unpacker:
                if isinstance(msg, list) and len(_msg) > 0 and isinstance(_msg[0], dict):
                    _data = _msg[0]
                    _translation, _translation_flag = _data['translation']
                    _quaternion, _quaternion_flag = _data['quanternion']
                    _velocity = _data['velocity']

                    #unpack data here
                    state.pos = _translation
                    state.v = _velocity
                    state.q = _quaternion
        except:
            print("failed unpacking vicon data")

    
