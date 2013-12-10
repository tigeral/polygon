import SocketServer
import struct


class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        print struct.unpack(">d", data[:8])

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()